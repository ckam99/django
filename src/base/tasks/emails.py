from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings
from base.backends import ModelHelper
from celery import shared_task


@shared_task(bind=True)
def send_confirmation_mail(self, email: str):
    message = get_template("mails/confirm_email.html").render({
        'email': email,
        'code': ModelHelper.create_confirmation_code(email)
    })
    mail = EmailMessage(
        subject="Confirmation",
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
        reply_to=None,
    )
    mail.content_subtype = "html"
    mail.send()
    return 'Email successfuly to {}'.format(email)
