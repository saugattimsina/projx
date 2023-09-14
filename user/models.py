from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField,BooleanField,TextField,FileField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import uuid

class User(AbstractUser):


    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    # first_name = None  # type: ignore
    # last_name = None  # type: ignore
    # address = TextField(max_length=255,blank=True)
    image = FileField(upload_to='uploads/%Y/%m/%d/',null=True, blank=True)
    # cell_number_1 = CharField(max_length=13, blank=True)
    # cell_number_2 = CharField(max_length=13, blank=True)
    # home_number = CharField(max_length=13, blank=True)
    user_uuid =models.UUIDField(default=uuid.uuid4)
    is_staff = BooleanField(default=False)
    # is_agent = BooleanField(default=False)
    is_client = BooleanField(default=False)
    telegram_id = models.IntegerField(blank=True)
    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
