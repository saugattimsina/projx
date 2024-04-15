import random
import string
from django.core.mail import send_mail
from projx.settings import FRONTEND_URL, EMAIL_HOST_USER
from templated_email import send_templated_mail


def generate_otp(length=20):
    characters = string.digits + string.ascii_letters
    otp = "".join(random.choice(characters) for _ in range(length))
    return otp


def send_otp_email(user, otp):
    from_email = EMAIL_HOST_USER
    recipient_list = [user.email]
    template = "password_reset"
    reset_link = f"{FRONTEND_URL}/reset-password/{user.user_uuid}/{otp}"
    send_templated_mail(
        template_name=template,
        recipient_list=recipient_list,
        from_email=from_email,
        context={
            "reset_link": reset_link,
        },
    )
