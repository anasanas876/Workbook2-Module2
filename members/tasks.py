from django.tasks import task
from django.core.mail import send_mail
from django.conf import settings
@task
def send_welcome_email(email):
    send_mail(
        subject="Welcome to Project Management System ",
        message="This email confirms that you have successfully signed up ",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email]
    )


