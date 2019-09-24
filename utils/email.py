from flask import current_app
from flask_mail import Message, Mail


def send_email(to, subject, template):
    mail = Mail(current_app)
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_SENDER']
    )
    mail.send(msg)
