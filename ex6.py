
import streamlit as st
import base64
from pathlib import Path
from questions2 import questions  # ייבוא השאלות מקובץ חיצוני
import time
import gd
import llm
import pathlib
from PIL import Image
import time_1 as ti
from schools import School_Type
import schools


# פונקציה להמרת תמונה ל-base64
def img_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# המרת התמונה ל-base64
try:
    img_base64 = img_to_base64("mop_logo.jpg")
    avatar_img = f"data:image/jpeg;base64,{img_base64}"
except Exception as e:
    avatar_img = ""

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;700&display=swap');
    
    .main-title {
        font-family: 'Rubik', sans-serif;
        font-size: 36px;
        font-weight: 700;
        color: #1E88E5;
        text-align: right;
        padding: 20px 0;
        direction: rtl;
    }
    
    .chat-message {
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        display: flex;
        flex-direction: row;
        width: fit-content;
        max-width: 80%;
    }
    
    .user-message {
        background: #E3F2FD;
        border-radius: 15px;
        margin-left: 0;
        margin-right: auto;
        direction: rtl;
    }
    
    .bot-message {
        margin-left: auto;
        margin-right: 0;
        direction: rtl;
        display: flex;
        align-items: center;  /* מיישר את התוכן אנכית במרכז */
    }
    
    .message-text {
        font-family: 'Rubik', sans-serif;
        font-size: 16px;
        margin: 0;
    }
    
    .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-left: 10px;
        object-fit: cover;
    }
    
    .message-content {
        display: flex;
        flex-direction: column;
    }
    
    .timestamp {
        font-size: 12px;
        color: #666;
        margin-top: 4px;
    }
    
    .stButton button {
    direction: rtl;
    text-align: right;
    background-color: rgb(0, 110, 184, 0.8);
    border: 1px solid rgba(250, 250, 250, 0);
    color: white;
    padding: 0.5em 1em;
    border-radius: 8px;
    font-size: 1em;
    cursor: pointer;
    text-align: center;
    display: inline-block;
    text-decoration: none;
}

.stButton button:hover{
    background-color: rgb(0, 110, 184);
    color: white;
    border: 1px solid rgb(38, 39, 48);
}


.stTextInput input {
    background-color: rgb(165, 221, 234); 
    color: black; 
    border: 1px solid rgba(0, 110, 184, 0.8); /
    padding: 10px; 
}

/* יישור טקסט בתוך selectbox */
.stSelectbox div[role="combobox"] {
    direction: rtl;
    text-align: right;
    }

/* יישור Selectbox לימין */
.stSelectbox div[role="combobox"] {
    direction: rtl;
    text-align: right;
}

/* יישור כפתור "אישור" לימין */
.stButton {
    display: flex;
    justify-content: flex-end;
}
/* יישור אפשרויות בתוך selectbox */
.stSelectbox div[role="listbox"] {
    direction: rtl;
    text-align: right;
}

    </style>
    """,
    unsafe_allow_html=True
)
def display_bot_image(image_path):
    img_base64 = img_to_base64(image_path)
    # הוספת התמונה להיסטוריית השיחה
    st.session_state.messages.append({
        "role": "assistant",
        "content": None,  # אין טקסט במקרה הזה
        "type": "image",
        "url": image_path
    })
    # הצגת התמונה
    st.image(image_path)
    # st.markdown(f"""
    # <div class="chat-message bot-message">
    #     <div class="message-content">
    #         <img src="data:image/jpeg;base64,{img_base64}" style="max-width: 100%; border-radius: 15px;" />
    #     </div>
    # </div>
    # """, unsafe_allow_html=True)
    # עדכון השאלה הנוכחית
    st.session_state.current_question += 1
    # אתחול מחדש של האפליקציה
    st.rerun()

def display_bot_video(video_path):
    st.video(video_path)
    st.session_state.messages.append({
        "role": "assistant",
        "type": "video",
        "url": video_path
    })
     # עדכון השאלה הנוכחית
    st.session_state.current_question += 1
    st.rerun()
    
def start_counting_time():
                st.session_state.is_counting_time=True
                ti.begin()
                
    
def stop_counting_time():
                st.session_state.is_counting_time=False
                response_time_count=ti.end()
                st.session_state.user_data.append(response_time_count)

    

def display_user_message(text):
    st.markdown(f"""
    <div class="chat-message user-message">
        <div class="message-content">
            <p class="message-text">{text}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_bot_message_with_typing_effect(text, typing_speed=0.05):
    """
    מציג הודעה מהבוט עם אפקט הקלדה
    
    :param text: הטקסט להצגה
    :param typing_speed: מהירות ההקלדה (בשניות בין תווים)
    """

    placeholder = st.empty()
    displayed_text = ""
    
    for char in text:
        displayed_text += char
        placeholder.markdown(f"""
        <div class="chat-message bot-message">
            <div class="message-content">
                <p class="message-text">{displayed_text}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(typing_speed)
    
    # # החלפת הטקסט הסופי עם עיצוב קבוע
    # st.markdown(f"""
    # <div class="chat-message bot-message">
    #     <div class="message-content">
    #         <p class="message-text">{text}</p>
    #     </div>
    # </div>
    # """, unsafe_allow_html=True)

# החלפת display_bot_message בקוד הקיים
# def display_bot_message(text):
#     display_bot_message_with_typing_effect(text)
    
def display_bot_message(text):
    st.markdown(f"""
    <div class="chat-message bot-message">
        <div class="message-content">
            <p class="message-text">{text}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
st.logo("logo1.jpg",
         size="large")
 
#questions functions
def show_closed_question(question, options, feedbacks):
    time.sleep(0.5)  # הוספת השהיה של 0.5 שניות
    display_bot_message(question)

    # יצירת כפתורים לבחירת תשובה
    cols = st.columns(len(options))
    for i, option in enumerate(options):
        if cols[i].button(option, key=f"{st.session_state.current_question}_{option}"):
            # הוספת השאלה והתשובה להיסטוריה
            st.session_state.messages.append({"role": "assistant", "content": question})
            st.session_state.messages.append({"role": "user", "content": option})

            # שמירת התשובה של המשתמש במשתנה user_data
            st.session_state.user_data.append(option)
            
            # הוספת הפידבק
            st.session_state.messages.append({"role": "assistant", "content": feedbacks[i]})
            st.session_state.current_question += 1
            st.rerun()

def show_closed_grade_question(question, options,feedbacks, session_state_answer):
    time.sleep(0.5)  # הוספת השהיה של 0.5 שניות
    display_bot_message(question)
    # יצירת כפתורים לבחירת תשובה
    cols = st.columns(len(options))
    for i, option in enumerate(options):
        if cols[i].button(option, key=f"{st.session_state.current_question}_{option}"):
            # הוספת השאלה והתשובה להיסטוריה
            st.session_state.messages.append({"role": "assistant", "content": question})
            st.session_state.messages.append({"role": "user", "content": option})

            # שמירת התשובה של המשתמש במשתנה user_data
            st.session_state.user_data.append(option)
            # שמירת הכיתה במשתשנה בsession_state
            grade=session_state_answer[i]
            st.session_state.grade=grade
            
            # הוספת הפידבק
            st.session_state.messages.append({"role": "assistant", "content": feedbacks[i]})
            st.session_state.current_question += 1
            st.rerun()

    
    
# פונקציה להצגת שאלה פתוחה
def show_open_question(question, feedback):
    # הצגת השאלה הפתוחה מהבוט
    time.sleep(0.5)  # הוספת השהיה של 0.5 שניות

    display_bot_message(question)
  #old#  with st.chat_message("assistant"):
   #old#     st.markdown(question)

# פונקציה להצגת היסטוריית השיחה
def show_chat_history():
     for message in st.session_state.messages:
        if message["role"] == "assistant":
            if message.get("type") == "image":  # הודעה מסוג תמונה
                st.image(message['url'])
                # st.markdown(f"""
                # <div class="chat-message bot-message">
                #     <div class="message-content">
                #         <img src="{message['url']}" style="max-width: 100%; border-radius: 15px;" />
                #     </div>
                # </div>
                # """, unsafe_allow_html=True)
            elif message.get("type") == "video":  # הודעה מסוג וידאו
                st.video(message['url'])
            else:  # הודעת טקסט רגילה
                display_bot_message(message["content"])
        elif message["role"] == "user":  # הודעת משתמש
            display_user_message(message["content"])

    # for message in st.session_state.messages:
    #     if (message["role"]=="assistant"):
    #         display_bot_message(message["content"])
    #     if (message["role"]=="user"):
    #         display_user_message(message["content"])
       

# פונקציה להצגת תיבת הקלט הקבועה בתחתית
def display_input_box(disabled):
    user_input = st.chat_input("הכנס את התשובה שלך כאן", disabled=disabled)
    
    if user_input:
        # אם המשתמש מקליד לאחר סיום השאלות, נוסיף להיסטוריה בלבד
        if st.session_state.current_question >= len(questions):
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "assistant", "content": "תודה! השיחה הסתיימה, אבל אני כאן לשמוע אם יש עוד משהו שתרצה לשתף."})
        # אם המשתמש מקליד תשובה לשאלה פתוחה
        elif not disabled:
            # הוספת התשובה להיסטוריה
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # שמירת התשובה של המשתמש במשתנה user_data
            st.session_state.user_data.append(user_input)

            # טיפול בשאלה הפתוחה או החזרה לשאלה הסגורה
            if st.session_state.current_question < len(questions):
                current_q = questions[st.session_state.current_question]

                # אם זו שאלה פתוחה, השאלה תטופל כאן
                if current_q["type"] == "open":
                    st.session_state.messages.append({"role": "assistant", "content": current_q["feedback"]})
                    st.session_state.current_question += 1
                # אם זו שאלה סגורה, השאלה תוצג מחדש כדי שהמשתמש יבחר באחת האפשרויות
                elif current_q["type"] == "closed":
                    st.session_state.messages.append({"role": "assistant", "content": current_q["question"]})
            
        st.rerun()

def show_selectbox_schools_question(question, feedbacks):
    # הצגת השאלה
    display_bot_message(question)

    # קבלת סוגי בתי הספר
    school_type = schools.School_Type.to_School_Type(st.session_state.grade)
    options = schools.return_schools_list(school_type)

    # יצירת Selectbox עבור הבחירה
    selected_option = st.selectbox(
        "",
        options,
        key=f"{st.session_state.current_question}_selectbox",
        index=None,
        placeholder="שם בית הספר שלך...",
    )

    # לחצן אישור לבחירת התשובה
    if st.button("אישור", key=f"{st.session_state.current_question}_confirm"):
        # הוספת השאלה והתשובה להיסטוריה
        st.session_state.messages.append({"role": "assistant", "content": question})
        st.session_state.messages.append({"role": "user", "content": selected_option})

        # שמירת התשובה של המשתמש במשתנה user_data
        st.session_state.user_data.append(selected_option)

        # הוספת הפידבק לפי הבחירה
        feedback_index = options.index(selected_option)
        st.session_state.messages.append({"role": "assistant", "content": feedbacks})
        st.session_state.current_question += 1
        st.rerun()
        
# פונקציה להצגת שאלה מסוג selectbox
# def show_selectbox_schools_question(question, feedbacks):
#      # הצגת השאלה
#     #old#st.markdown(question)
#     display_bot_message(question)

#     school_type= schools.School_Type.to_School_Type(st.session_state.grade)#School_Type[st.session_state.grade]#School_Type.SCHOOL_10
#     options=schools.return_schools_list(school_type)
#     # יצירת Selectbox עבור הבחירה
#     selected_option = st.selectbox("", options, key=f"{st.session_state.current_question}_selectbox",
#                                    index=None,
#                                    placeholder="שם בית הספר שלך...",)



#     # לחצן אישור לבחירת התשובה
#     if st.button("אישור", key=f"{st.session_state.current_question}_confirm"):
#         # הוספת השאלה והתשובה להיסטוריה
#         st.session_state.messages.append({"role": "assistant", "content": question})
#         st.session_state.messages.append({"role": "user", "content": selected_option})

#         # שמירת התשובה של המשתמש במשתנה user_data
#         st.session_state.user_data.append(selected_option)

#         # הוספת הפידבק לפי הבחירה
#         feedback_index = options.index(selected_option)
#         st.session_state.messages.append({"role": "assistant", "content": feedbacks})
#         st.session_state.current_question += 1
#         st.rerun()
    
# כותרת
st.markdown('<h1 class="main-title">מבט לרגע</h1>', unsafe_allow_html=True)
# אתחול משתני session_state במידת הצורך
if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.current_question = 0
        st.session_state.finished = False
        st.session_state.user_data = []  # אתחול המשתנה לאחסון התשובות
        st.session_state.is_counting_time= False 
        st.session_state.grade=[]

        # הוספת משפט פתיחה
        opening_message = """
        שלום, אני ביטי הבוט של תוכנית ההייטק הלאומית. נעים מאוד!
        אני כאן כדי לשמוע על הרצון והמוטיבציה שלך להשתלב בעתיד בתפקידים שונים בתעשיית ההייטק.
        נתחיל מכמה שאלות בסיסיות.
        """
        st.session_state.messages.append({"role": "assistant", "content": opening_message})

    # הצגת היסטוריית השיחה
show_chat_history()

#checks if it counting time - stop time
if (st.session_state.is_counting_time==True):
                stop_counting_time()

    # הצגת השאלה הנוכחית (אם עדיין לא סיימנו את כל השאלות)
if not st.session_state.finished:
        if st.session_state.current_question < len(questions):
            current_q = questions[st.session_state.current_question]
            if current_q["type"] == "open":
                show_open_question(current_q["question"], current_q["feedback"])
                display_input_box(disabled=False)  # הפעלת תיבת ה-input
            elif current_q["type"] == "closed":
                show_closed_question(current_q["question"], current_q["options"], current_q["feedbacks"])
                display_input_box(disabled=True)  # השבתת תיבת ה-input
            elif current_q["type"] == "selectbox_schools":
                show_selectbox_schools_question(current_q["question"], current_q["feedbacks"])
                display_input_box(disabled=True)  # השבתת תיבת ה-input
            elif current_q["type"] == "image":
                display_bot_image(current_q["url"])
                display_input_box(disabled=True)  # השבתת תיבת ה-input
            elif current_q["type"] == "video":
                display_bot_video(current_q["url"])
                display_input_box(disabled=True)  # השבתת תיבת ה-input
            elif current_q["type"] == "closed_grade":
                show_closed_grade_question(current_q["question"], current_q["options"],current_q["feedbacks"], current_q["session_state_answer"])
                display_input_box(disabled=True)  # השבתת תיבת ה-input
                
            if current_q["time_count"] == "yes":
                start_counting_time()
                
        else:
            st.session_state.finished = True

            
            summary_message = llm.summerize_conversation(st.session_state.messages)
            
            display_bot_message(summary_message)
            
            st.session_state.messages.append({"role": "assistant", "content": summary_message})

            # השבתת תיבת ה-input בסיום השיחה
            display_input_box(disabled=True)

            user_data = st.session_state.user_data
            gd.add_row_to_sheet(user_data)
        
