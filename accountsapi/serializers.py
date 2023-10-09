from datetime import datetime, timezone
from io import BytesIO

import pyotp
import qrcode

from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token


from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "user_uuid",
            "name",
            "image",
            "is_staff",
            "is_client",
            "telegram_id",
            "qr_code",
        ]


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs: dict):
        print(attrs.get("username"))
        print(attrs.get("password"))
        user = authenticate(
            # request=self.context.get("request"),
            username=attrs.get("username"),
            password=attrs.get("password"),
        )
        print(user)
        if user is None:
            raise exceptions.AuthenticationFailed("Invalid login details.")
        else:
            attrs["user_object"] = user
        return super().validate(attrs)

    def create(self, validated_data: dict):
        user: User = validated_data.get("user_object")
        print(user)
        totp = pyotp.TOTP(user.otp_base32).now()
        user.login_otp = totp
        user.otp_created_at = datetime.now(timezone.utc)
        user.login_otp_used = False
        user.save(update_fields=["login_otp", "otp_created_at", "login_otp_used"])
        return user


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = [
            "username",
            "name",
            "image",
            # "telegram_id",
            "email",
            "password",
            "confirm_password",
            "refered",
        ]
        extra_kwargs = {"password": {"write_only": True}, "image": {"required": True}}

    def validate_image(self, value):
        # Check if the uploaded image is greater than 2 MB (2 * 1024 * 1024 bytes)
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError(_("Image size should not exceed 2 MB."))
        return value

    def validate_password(self, value):
        # Use Django's built-in password validation to check password strength
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                {
                    "email": "This email is already registered.",
                }
            )
        return value

    def create(self, validated_data):
        password = validated_data["password"]
        password2 = validated_data["confirm_password"]
        if password != password2:
            raise serializers.ValidationError(
                {
                    "message": {"password": "Passwords must match."},
                    "success": False,
                }
            )

        email = validated_data["email"]
        self.validate_email(email)

        # Create the user instance without custom fields
        user = User(username=validated_data["username"], email=validated_data["email"])
        user.image = validated_data["image"]
        user.name = validated_data["name"]
        user.set_password(password)
        # user.telegram_id = validated_data["telegram_id"]
        print(validated_data["refered"])
        user.refered = validated_data["refered"]
        # print(refered)
        user.is_client = True
        # Save the user instance with custom fields
        user.save()

        return user


class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)
    user_id = serializers.IntegerField(required=True)

    def validate(self, attrs: dict):
        user: User = User.objects.filter(id=attrs.get("user_id")).first()
        if not user:
            raise serializers.ValidationError("user id is wrong")

        if attrs.get("otp") != user.login_otp or not user.is_valid_otp():
            totp = pyotp.TOTP(user.otp_base32).now()
            user.login_otp = totp
            user.otp_created_at = datetime.now(timezone.utc)
            user.login_otp_used = False
            user.save(update_fields=["login_otp", "otp_created_at", "login_otp_used"])

            if attrs.get("otp") != user.login_otp:
                raise serializers.ValidationError("OTP is wrong")
            else:
                raise serializers.ValidationError("OTP is wrong")
        attrs["user"] = user
        return super().validate(attrs)

    def create(self, validated_data: dict):
        user: User = validated_data.get("user")
        token = Token.objects.get(user=user)
        user.login_otp_used = True
        user.save(update_fields=["login_otp_used"])
        return {
            "token": token.key,
            "user": {
                "user_id": user.id,
                "username": user.username,
                "image": user.image.path,
                "is_client": user.is_client,
            },
        }
