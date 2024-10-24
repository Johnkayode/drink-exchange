
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_field
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework.exceptions import PermissionDenied

from api.apps.base.utils import build_url


class AccountAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        if isinstance(email, str):
            return email.lower().strip()
        return email
    
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance
        """
        data = form.cleaned_data
    
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        phone_number: PhoneNumber = data.get("phone_number")
        account_type = data.get("account_type")

        if email:
            user_email(user, email)
        if phone_number:
            user_field(user, "phone_number", phone_number.as_e164)

        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        if account_type:
            user_field(user, "account_type", account_type)
       
        if "password" in data:
            user.set_password(data["password"])
        else:
            user.set_unusable_password()

        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()

        return user

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url.
        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        return build_url(
            settings.FRONTEND_URL, 
            settings.FRONTEND_EMAIL_VERIFICATION_URL,
            key=emailconfirmation.key,
        )
    
    def respond_user_inactive(self, request, user):
        return PermissionDenied(
            detail="Your account is inactive. Please contact support for assistance", 
            code="permission_denied"
        )

    def respond_email_verification_sent(self, request, user):
        """Override all-auth's email_verification_sent template view
        """
        ...

