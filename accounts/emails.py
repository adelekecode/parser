import requests
import os


key = os.getenv("email_key")




def user_sk_mail(user):

    requests.post(

        url="https://api.useplunk.com/v1/send",

        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"

        },

        json={
            "to": user.email,
            "subject": "PARSER SECRET KEY",
            "body": f"""
            <html> <body> <p>Dear Dev,</p>

<p>You have inititated the creation of your Parser Secret Key.
 which would be used as your authorization token.</p>

<p>Here is your secret key: {str(user.sk).capitalize()}</p>
<p>Protect your secret key</p>

<p>Best regards,</p>
<p>AdelekeCode.</p> 
</body> </html>
            """
        }
    )
