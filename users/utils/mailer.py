import os

from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from fastapi_mail.errors import ConnectionErrors

mail_conf = ConnectionConfig(
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME"),
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD"),
    MAIL_FROM = os.environ.get("MAIL_FROM"),
    MAIL_PORT = int(os.environ.get("MAIL_PORT")),
    MAIL_SERVER = os.environ.get("MAIL_SERVER"),
    MAIL_TLS = bool(os.environ.get("MAIL_TLS")),
    MAIL_SSL = bool(os.environ.get("MAIL_SSL")),
    USE_CREDENTIALS = bool(os.environ.get("MAIL_USE_CREDENTIALS"))
)

fast_mail = FastMail(mail_conf)


async def send_token(email, token):
    template = f"""
    <p> Enter {token} to  complete registration</p>
    """
    print(email, template)
    msg = MessageSchema(
        subject="Complete registration",
        recipients=[email,],  # List of recipients, as many as you can pass 
        body=template,
        subtype="html"
    )
    try:
        await fast_mail.send_message(msg)
    except ConnectionErrors as e:
        print("CANNOT SEND MAIL", ", ".join(e.args))

    



