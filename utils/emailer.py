"""Sends Emails"""

import os
import certifi
import sendgrid
from dotenv import load_dotenv
from sendgrid.helpers.mail import Mail, Email, To, Content

load_dotenv(override=True)
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

# to resolve SSL certificate error while sending email
os.environ["SSL_CERT_FILE"] = certifi.where()


def send_email(
    sender_email: str,
    recipient_email: str,
    subject: str,
    body: str,
    content_type: str = "text/plain",
):
    """Send email utility function"""

    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    from_email = Email(sender_email)
    to_email = To(recipient_email)
    content = Content(content_type, body)
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.client.mail.send.post(request_body=mail)

    print("Email Response", response.status_code)

    return response.status_code
