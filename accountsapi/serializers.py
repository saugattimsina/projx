from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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
        ]


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )
    email = serializers.EmailField()  # Add the "email" field here

    class Meta:
        model = User
        fields = [
            "username",
            "name",
            "image",
            "telegram_id",
            "email",
            "password",
            "confirm_password",
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
                    "message": {"email": "This email is already registered."},
                    "success": False,
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
        user = User.objects.create_user(
            validated_data["username"], password=password, email=validated_data["email"]
        )
        user.image = validated_data["image"]
        user.name = validated_data["name"]
        user.telegram_id = validated_data["telegram_id"]
        user.is_client = True

        # Save the user instance with custom fields
        user.save()

        return user
