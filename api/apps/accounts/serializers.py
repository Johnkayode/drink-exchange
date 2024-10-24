import logging
import typing
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.translation import gettext as _, gettext_lazy as __
from dj_rest_auth.registration import (
    serializers as dj_rest_auth_registration_serializers
)
from dj_rest_auth.serializers import ( 
    TokenSerializer as DjRestAuthTokenSerializer,
    LoginSerializer as DJRestLoginSerializer,
    PasswordResetSerializer as DJPasswordResetSerializer,
    PasswordResetConfirmSerializer as DJPasswordResetConfirmSerializer
)
from phonenumber_field.phonenumber import PhoneNumber
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework import serializers, exceptions
from api.apps.accounts.models import AccountType, Business
from api.apps.accounts.forms import CustomResetPasswordForm, CustomSetPasswordForm

if typing.TYPE_CHECKING:
    from api.apps.accounts.models import User


logger = logging.getLogger(__name__)
UserModel = get_user_model()


class BusinessRegisterSerializer(dj_rest_auth_registration_serializers.RegisterSerializer):
    username = None
    password1 = None
    password2 = None
  
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    business_name = serializers.CharField(required=True)
    phone_number = PhoneNumberField(required=False)
    account_type = serializers.HiddenField(default=AccountType.COMPANY_ADMIN)
    password = serializers.CharField(write_only=True, required=True)
 
    def validate_username(self, username):
        pass

    def validate_email(self, email: str):
        email_exists: bool = UserModel.objects.filter(email=email).exists()
        if email_exists:
            raise serializers.ValidationError(
                "A user with this email already exists", "invalid"
            )
        return email
    
    def validate_phone_number(self, phone_number: PhoneNumber):
        phone_exists: bool = UserModel.objects.filter(phone_number=phone_number.as_e164).exists()
        if phone_exists:
            raise serializers.ValidationError(
                "A user with this phone number already exists", "invalid"
            )
        return phone_number


    def get_cleaned_data(self):
        return {
            "email": self.validated_data.get("email", ""),
            "first_name": self.validated_data.get("first_name"),
            "last_name": self.validated_data.get("last_name", ""),
            "phone_number": self.validated_data.get("phone_number", ""),
            "account_type": self.validated_data.get("account_type"),
            "password": self.validated_data.get("password", ""),
        }

    def custom_signup(self, request, user):
        # create business
        user: "User"
        with transaction.atomic():
            business = Business.objects.create(
                name=self.validated_data.get("business_name"),
                email=self.validated_data.get("email")
            )
            user.business = business
            user.save(update_fields=["business"])
    


class TokenSerializer(DjRestAuthTokenSerializer):
    class Meta(DjRestAuthTokenSerializer.Meta):
        fields = ('digest', 'token_key')


class LoginSerializer(DJRestLoginSerializer):
    username = None
    email = serializers.EmailField(label=__("email"), write_only=True, required=False)
    # phone_number = PhoneNumberField(required=False)
    
    def validate_email_verification_status(self, user: "User"):
        try:
            return super().validate_email_verification_status(user)
        except exceptions.ValidationError as e:
            raise exceptions.ValidationError(
                _("Please verify your email."), code="email_not_verified"
            )

    def validate_email(self, email: str) -> str:
        if email:
            return email.lower()
        return email
    
    def validate(self, attrs):
        username: str = attrs.get("username")
        email: str = attrs.get("email")
        password: str = attrs.get("password")

        user: "User" = self.get_auth_user(username, email, password)

        if not user:
            msg = _("Unable to log in with provided credentials.")
            raise exceptions.ValidationError(msg)

        # Did we get back an active user?
        self.validate_auth_user_status(user)

        # superuser bypass
        if not user.is_superuser:
            # If required, is the email verified?
            self.validate_email_verification_status(user)

        attrs["user"] = user
        return attrs   


class PasswordResetSerializer(DJPasswordResetSerializer):
    @property
    def password_reset_form_class(self):
        return CustomResetPasswordForm
    

class PasswordResetConfirmSerializer(DJPasswordResetConfirmSerializer):
    set_password_form_class = CustomSetPasswordForm
