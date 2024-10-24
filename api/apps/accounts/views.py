import logging
import typing
from django.contrib.auth import login
from django.core import exceptions as django_exceptions
from django.utils.translation import gettext as _

from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration import views as dj_rest_auth_registration_views
from knox.views import (
    LoginView as KnoxLoginView,
    LogoutView as KnoxLogoutView,
    LogoutAllView as KnoxLogoutAllView,
)
from rest_framework import response, status, permissions, generics, exceptions
from api.apps.accounts.serializers import BusinessRegisterSerializer, LoginSerializer
if typing.TYPE_CHECKING:
    from api.apps.accounts.models import User


class BusinessRegisterView(dj_rest_auth_registration_views.RegisterView):
    serializer_class = BusinessRegisterSerializer

    def perform_create(self, serializer) -> "User":
        user: "User" = serializer.save(self.request)
        complete_signup(
            self.request._request,
            user,
            allauth_settings.EMAIL_VERIFICATION,
            None,
        )
        return user

    def get_response_data(self, user: "User") -> typing.Dict[str, str]:
        return {"detail": _("Registration Successful. Verify your account.")}
    

class VerifyEmailView(dj_rest_auth_registration_views.VerifyEmailView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs["key"] = serializer.validated_data["key"]
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return response.Response(
            {"detail": _("ok"), "email": confirmation.email_address.email},
            status=status.HTTP_200_OK,
        )


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    throttle_scope = "login"
    serializer_class = LoginSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {"request": self.request, "format": self.format_kwarg, "view": self}

    def post(self, request, format=None):
        serializer = self.serializer_class(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class LogoutView(KnoxLogoutView):
    def post(self, request, format=None):
        return super().post(request, format=None)


class LogoutAllView(KnoxLogoutAllView):
    """
    Log the user out of all sessions
    I.E. deletes all auth tokens for the user
    """

    def post(self, request, format=None):
        return super().post(request, format=None)