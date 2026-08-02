from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path(
    "forgot-password/",
    auth_views.PasswordResetView.as_view(
    template_name="accounts/password_reset.html",
    email_template_name="emails/password_reset_email.txt",
    html_email_template_name="emails/password_reset_email.html",
    success_url="/forgot-password/sent/"
    ),
    name="password_reset",
),
path(
    "activate/<uuid:token>/",
    views.activate_account,
    name="activate"
),

path(
    "forgot-password/sent/",
    auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_sent.html"
    ),
    name="password_reset_done",
),


path(
    "reset-password/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html",
    ),
    name="password_reset_confirm",
),


path(
    "reset-password/complete/",
    auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"
    ),
    name="password_reset_complete",
),
]