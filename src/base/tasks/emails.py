from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings


def send_confirmation_mail(email: str):
    message = get_template("mails/confirm_email.html").render({
        'email': email
    })
    mail = EmailMessage(
        subject="Confirmation",
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
        reply_to=None,
    )
    mail.content_subtype = "html"
    return mail.send()
