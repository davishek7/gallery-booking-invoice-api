import asyncio
from ..signals.send_email_signal import send_email_signal
from ..utils.mail import send_email_async


@send_email_signal.connect
def handle_send_mail(
    sender, subject: str, recipients: list, template_name: str, context: dict = None
):
    """Runs the email sending task in the background."""
    asyncio.create_task(send_email_async(subject, recipients, template_name, context))
