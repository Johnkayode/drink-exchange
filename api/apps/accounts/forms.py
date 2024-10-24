import typing

from django.conf import settings

from django.contrib.auth.forms import SetPasswordForm

from allauth.account.forms import (
    ResetPasswordForm,
    default_token_generator,
)
from allauth.account.utils import (
    user_pk_to_url_str,
)
from allauth.account.adapter import get_adapter
from api.apps.base.utils import build_url

if typing.TYPE_CHECKING:
    from api.apps.accounts.models import User


class CustomResetPasswordForm(ResetPasswordForm):
    def _send_unknown_account_mail(self, request, email):
        return

    def _send_password_reset_mail(self, request, email, users, **kwargs):
        token_generator = kwargs.get("token_generator", default_token_generator)
        user: "User"
        
        for user in users:
            temp_key = token_generator.make_token(user)

            # send the password reset email
            uidb36 = user_pk_to_url_str(user)
            url = build_url(
                settings.FRONTEND_URL,
                settings.FRONTEND_RESET_PASSWORD_URL,
                uid=uidb36,
                token=temp_key
            )
            context = {
                "full_name": user.full_name,
                "password_reset_url": url,
                "request": request,
            }
            get_adapter().send_mail("account/email/password_reset_key", email, context)


class CustomSetPasswordForm(SetPasswordForm):
    def save(self, commit=True):
        self.user: "User"
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        self.user.password_change_required = False
        if commit:
            self.user.save()
        return self.user
