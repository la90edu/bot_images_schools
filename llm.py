from openai import OpenAI
client = OpenAI()

def summerize_conversation(conversation):
 prompt = (
    f"אתה משחק תפקיד של חבר ומנטור לתלמיד או תלמידה בתיכון. "
    f"\nאתה מקבל רשימה של שיחה שהתנהלה בינך לבין התלמיד/ה במסגרת תוכנית ההייטק הלאומית, שמטרתה לקרב תלמידים לעולם ההייטק ולעודד אותם להשתלב בתחום כשיגדלו. "
    f"\nעליך לסכם את השיחה בצורה חיובית ומעודדת, ולפנות ישירות אל התלמיד/ה בגוף שני כדי ליצור תחושת חיבור ואישית. "
    f"התגובה שלך צריכה להיות עד 3-4 משפטים בלבד, בעברית בלבד, תוך שימוש בשפה נעימה, מנומסת ומותאמת לגיל התלמידים, וללא אזכור של נושאים רגישים כמו אלימות או מיניות. "
    f"\nזוהי השיחה: {conversation}"
) 
 response = client.chat.completions.create(
 model="gpt-4o",
 messages=[{"role":"user","content":prompt}]
 )
 return response.choices[0].message.content.strip()



# response=summerize_conversation("היי מה שלומך , הכל בסדר, איזה חיה את אוהבת , אני אוהבת כלבים")
# print(response)


def how_do_you_feel(conversation):
 prompt = (
    f"אתה משחק תפקיד של חבר ומנטור לתלמיד או תלמידה בתיכון. "
    f"\nאתה מקבל רשימה של שיחה שהתנהלה בינך לבין התלמיד/ה במסגרת תוכנית ההייטק הלאומית, שמטרתה לקרב תלמידים לעולם ההייטק ולעודד אותם להשתלב בתחום כשיגדלו. "
    f"אני שולחת את השיחה. תן פידבק חיובי ומעודד לשאלה האחרונה שתגרום לתלמיד להמשיך לשוחח"
    f"התגובה שלך צריכה להיות עד 3-4 משפטים בלבד, בעברית בלבד, תוך שימוש בשפה נעימה, מנומסת ומותאמת לגיל התלמידים, וללא אזכור של נושאים רגישים כמו אלימות או מיניות. "
    f"\nזוהי השיחה: {conversation}"
) 
 response = client.chat.completions.create(
 model="gpt-4o",
 messages=[{"role":"user","content":prompt}]
 )
 return response.choices[0].message.content.strip()