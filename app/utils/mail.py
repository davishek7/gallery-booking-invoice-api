from fastapi_mail import MessageSchema, FastMail  # type: ignore
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from typing import List
from ..configs.mail import conf


templates = Jinja2Templates(directory="app/templates")


async def send_email_async(
    subject: str, recipients: List[EmailStr], template_name: str, context: dict = None
):
    html_content = templates.get_template(template_name).render(**(context or {}))

    message = MessageSchema(
        subject=subject, recipients=recipients, body=html_content, subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
