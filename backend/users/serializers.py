from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "password"]

    def validate_password(self, value):
        user = User(
            email=self.initial_data.get("email"),
            username=self.initial_data.get("username"),
        )
        validate_password(value, user=user)
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
        )


class EmailNormalizingTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email_field = self.username_field
        if email_field in attrs and attrs[email_field]:
            attrs[email_field] = User.objects.normalize_email(
                attrs[email_field]
            ).lower()
        return super().validate(attrs)
