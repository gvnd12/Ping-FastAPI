import base64
import uuid
from fastapi import UploadFile
from passlib.context import CryptContext
from random import Random
from app.core.config import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
import aiosmtplib
from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.tools.common_types import EmailType

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def send_email(mail_type: EmailType, **kwargs):
    context = {}
    if mail_type == EmailType.INVITATION:
        context["email_template"] = "email.html"
        context["subject"] = "Welcome to Ping"

    elif mail_type == EmailType.RESET_PASSWORD:
        context.update(
            {
                "email_template": "reset_password_email.html",
                "subject": "Reset Your Password – Ping",
            }
        )

    await send_invitation_email(
        kwargs["receiver_email"], kwargs.get("name", ""), context
    )


async def send_invitation_email(receiver_email: str, name: str, context: dict) -> str:
    """Send invitation email to the given receiver email with the given tenant name."""

    templates = Jinja2Templates(directory=Path(__file__).parent / "template")
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT
    from_address = settings.FROM_ADDRESS
    password = settings.EMAIL_PASSWORD

    name = name.capitalize()
    subject = context.get("subject", "")
    html_content = templates.TemplateResponse(
        context.get("email_template", ""),
        {
            "request": Request,
            "name": name,
        },
    )
    rendered_body = html_content.body.decode("utf-8")

    message = MIMEMultipart()
    message["From"] = f"Ping<{from_address}>"
    message["To"] = f"{name}<{receiver_email}>"
    message["Subject"] = subject
    message.attach(MIMEText(rendered_body, "html"))

    try:
        await aiosmtplib.send(
            message,
            hostname=smtp_server,
            port=smtp_port,
            username=from_address,
            password=password,
            start_tls=True,
        )

    except Exception as e:
        raise Exception(f"Error sending email: {e}") from e

    return "Success"


async def generate_user_code(name: str):
    random_num = str(Random().randint(a=1000, b=9999))
    random_name = name[0:4].upper()
    user_code = random_name + random_num
    return user_code


def generate_uuid_id():
    return str(uuid.uuid4().hex)


async def to_base64(file: UploadFile):
    file = await file.read()
    b64_img = base64.b64encode(file).decode("utf-8")
    return b64_img


async def password_hash(password: str):
    return pwd_context.hash(secret=password)


async def verify_password(plain_pass: str, hashed_pass: str):
    return pwd_context.verify(secret=plain_pass, hash=hashed_pass)
