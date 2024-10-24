from django.contrib.auth import views as django_auth_views
from django.urls import path, re_path

from allauth.account import views as allauth_views
from dj_rest_auth import views as dj_rest_auth_views
from dj_rest_auth.registration import views as dj_rest_auth_registration_views

from api.apps.accounts import views


urlpatterns = [
    path("register/business/", views.BusinessRegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("logout-all/", views.LogoutAllView.as_view(), name="logout_all"),
    # path('client/login/google/', views.GoogleLoginView.as_view(), name='client_login_google'),
    path("verify-email/", views.VerifyEmailView.as_view(), name="verify_email"),
    path(
        "verify-email/resend/",
        dj_rest_auth_registration_views.ResendEmailVerificationView.as_view(),
        name="rest_resend_email",
    ),
    path(
        "password/reset/",
        dj_rest_auth_views.PasswordResetView.as_view(),
        name="rest_password_reset",
    ),
    path(
        "password/reset/confirm/",
        dj_rest_auth_views.PasswordResetConfirmView.as_view(),
        name="rest_password_reset_confirm",
    ),
    path(
        "password/change/",
        dj_rest_auth_views.PasswordChangeView.as_view(),
        name="rest_password_change",
    ),

    ## Adding these urls to prevent allauth from breaking
    path(
        "reset/<uidb64>/<token>/",
        django_auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        allauth_views.password_reset_from_key,
        name="account_reset_password_from_key",
    ),
 
]