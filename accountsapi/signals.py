from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from datetime import datetime
from django.utils import timezone

from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string

import pyotp
import qrcode


@receiver(post_save, sender=get_user_model())
def assign_group_to_user(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def create_auth_qr_for_user(sender, instance, created, **kwargs):
    if created:
        user = instance
        email = user.email
        otp_base32 = pyotp.random_base32()
        otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
            name=email.lower(), issuer_name="projx"
        )
        stream = BytesIO()
        image = qrcode.make(f"{otp_auth_url}")
        image.save(stream)
        user.qr_code = ContentFile(
            stream.getvalue(), name=f"qr{get_random_string(10)}.png"
        )
        user.otp_base32 = otp_base32
        user.otpauth_url = otp_auth_url
        totp = pyotp.TOTP(user.otp_base32).now()
        user.login_otp = totp
        user.otp_created_at = datetime.now(timezone.utc)
        user.login_otp_used = False
        user.save()
