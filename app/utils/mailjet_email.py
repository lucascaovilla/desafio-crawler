import os
from mailjet_rest import Client

def send_email(to_email, subject, content):
    api_key = os.getenv('MAILJET_API_KEY')
    api_secret = os.getenv('MAILJET_API_SECRET')

    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    data = {
        'Messages': [
            {
                "From": {
                    "Email": os.getenv('MAILJET_FROM_EMAIL'),
                    "Name": os.getenv('MAILJET_NAME')
                },
                "To": [
                    {
                        "Email": to_email,
                        "Name": "Recipient"
                    }
                ],
                "Subject": subject,
                "TextPart": content
            }
        ]
    }

    try:
        result = mailjet.send.create(data=data)
        print(f"Email sent: {result.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")
