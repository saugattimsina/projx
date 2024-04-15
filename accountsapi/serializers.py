from datetime import datetime, timezone
from io import BytesIO

import pyotp
import qrcode

from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token

from user.models import UserKey


from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from subscription.models import UserSubcription
from binarytree.models import MLMRank, UserRank
import ccxt
from .utils import generate_otp, send_otp_email

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
        user = authenticate(
            username=attrs.get("username"),
            password=attrs.get("password"),
        )
        if user is None:
            raise exceptions.AuthenticationFailed("Invalid login details.")
        else:
            attrs["user_object"] = user
        return super().validate(attrs)

    def create(self, validated_data):
        user = validated_data.get("user_object")
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
    referal = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "username",
            "name",
            # "image",
            # "telegram_id",
            "email",
            "password",
            "confirm_password",
            "referal",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        # Check passwords match
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password": ["Passwords must match."]})

        # Password strength validation
        try:
            validate_password(data["password"])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        # Email uniqueness validation
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError(
                {"email": ["This email is already registered."]}
            )

        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        try:
            refered = User.objects.get(username=validated_data["referal"])
        except Exception as e:
            raise serializers.ValidationError("unknown referal")
        validated_data.pop("referal", None)
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.is_client = True
        user.refered = refered
        user.full_clean()  # This will run all model-level validations
        user.save()
        return user


class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)
    user_uid = serializers.CharField(required=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(user_uuid=attrs["user_uid"])
        except User.DoesNotExist:
            raise serializers.ValidationError("user uid is invalid")

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

    def create(self, validated_data):
        user = validated_data.get("user")
        token = Token.objects.get(user=user)
        user.login_otp_used = True
        user.save(update_fields=["login_otp_used"])
        key = UserKey.objects.filter(user=user).exists()
        subscription = UserSubcription.objects.filter(user=user)
        if subscription.exists():
            subscription = subscription.last()
            sub = {}
            # sub["subscription_id"] = subscription.id
            sub["subscription_type"] = subscription.plan.package_name
            # sub["subscription_start_date"] = subscription.start_date
            sub["package_type"] = subscription.plan.package_type
            sub["subscription_end_date"] = subscription.end_date
        else:
            sub = {}

        rank = UserRank.objects.get(user=user)
        user_rank = rank.rank.rank_name

        return {
            "token": token.key,
            "user": {
                "user_id": user.id,
                "username": user.username,
                "image": user.image.path if user.image else None,
                "is_client": user.is_client,
                "key": key,
                "user_rank": user_rank,
                "package": sub,
            },
        }


class UserBinancyAPIKey(serializers.ModelSerializer):
    def validate(self, data):
        api_key = data.get("api_key")
        api_secret = data.get("api_secret")
        print(api_key)
        print(api_secret)
        exchange = ccxt.binance(
            {
                "apiKey": api_key,
                "secret": api_secret,
                "options": {"defaultType": "future"},
            }
        )
        exchange.set_sandbox_mode(True)
        try:
            # Fetch account information (e.g., balances)
            account_info = exchange.fetchBalance()
            print(account_info)
            return data

        except ccxt.NetworkError as e:
            print("network_error")
            raise Exception("Network error")
        except ccxt.ExchangeError as e:
            print("exchange_error")
            print(e)
            raise Exception("Invalid API key or secret")

    class Meta:
        model = UserKey
        fields = ["api_key", "api_secret"]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return user

    def save(self):
        user = self.validated_data["email"]
        otp = generate_otp()
        send_otp_email(user=user, otp=otp)
        user.email_otp = otp
        user.save()


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    uid = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            uid = attrs["uid"]
            print(uid)
            user = User.objects.get(user_uuid=uid)
            if user.email_otp != attrs["token"]:
                raise Exception()
        except User.DoesNotExist:
            raise Exception("Invalid UID")
        except:
            raise Exception("Invalid Token")
        validate_password(attrs["password"], user=user)
        attrs["user"] = user
        return attrs

    def save(self):
        password = self.validated_data["password"]
        user = self.validated_data["user"]
        user.set_password(password)
        user.email_otp = None
        user.save()
