from fastapi import BackgroundTasks
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema

mail_conf = ConnectionConfig(
    MAIL_USERNAME = "0bf90ad61c32a2",
    MAIL_PASSWORD = "28dad5cf82ff30",
    MAIL_FROM = "x@test.org",
    MAIL_PORT = 2525,
    MAIL_SERVER = "smtp.mailtrap.io",
    MAIL_TLS = False,
    MAIL_SSL = False,
    USE_CREDENTIALS = True
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

    await fast_mail.send_message(msg)
    



