from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, BooleanField, TextField, FileField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

import uuid


class User(AbstractUser):
    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    # first_name = None  # type: ignore
    # last_name = None  # type: ignore
    # address = TextField(max_length=255,blank=True)
    image = FileField(upload_to="uploads/%Y/%m/%d/", null=True, blank=True)
    # cell_number_1 = CharField(max_length=13, blank=True)
    # cell_number_2 = CharField(max_length=13, blank=True)
    # home_number = CharField(max_length=13, blank=True)
    user_uuid = models.UUIDField(default=uuid.uuid4)
    is_staff = BooleanField(default=False)
    # is_agent = BooleanField(default=False)
    is_client = BooleanField(default=False)
    telegram_id = models.IntegerField(null=True, blank=True)
    referal_code = models.CharField(max_length=255, null=True, blank=True)
    refered = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    is_suscribed = models.BooleanField(default=False, null=True, blank=True)
    # is_active = models.BooleanField(default=False,null=True,blank=True)
    # is_first_month = models.BooleanField(default=True,null=True,blank=True)
    referal_code = models.CharField(max_length=255, null=True, blank=True)
    refered = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    otpauth_url = models.CharField(max_length=225, blank=True, null=True)
    otp_base32 = models.CharField(max_length=255, null=True, blank=True)
    qr_code = models.ImageField(upload_to="qrcode/", blank=True, null=True)
    login_otp = models.CharField(max_length=255, null=True, blank=True)
    login_otp_used = models.BooleanField(default=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    is_first_month = models.BooleanField(default=True)
    is_connected_to_authunticator = models.BooleanField(default=False)

    def is_valid_otp(self):
        lifespan_in_seconds = 40
        now = datetime.now(timezone.utc)
        time_diff = now - self.otp_created_at
        time_diff = time_diff.total_seconds()
        if time_diff >= lifespan_in_seconds or self.login_otp_used:
            return False
        return True

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class UserKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.api_key[0:5] + "****************"
