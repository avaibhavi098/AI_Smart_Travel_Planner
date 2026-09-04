from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [

    path("admin/", admin.site.urls),

    path("", include("accounts.urls")),


    path(
    "forgot-password/",
    auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html",
        email_template_name="registration/password_reset_email.html",
        html_email_template_name="registration/password_reset_email.html",
        subject_template_name="registration/password_reset_subject.txt",
    ),
    name="password_reset",
),

    path(
        "forgot-password/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_sent.html"
        ),
        name="password_reset_done",
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),


    path(
        "trips/",
        include(("trips.urls", "trips"), namespace="trips"),
    ),

    path(
        "destinations/",
        include("destinations.urls", namespace="destinations")
    ),

    path(
        "routes/",
        include("routes_app.urls"),
    ),

    path(
        "ai/",
        include(("ai.urls", "ai"), namespace="ai"),
    ),

    path(
        "assistant/",
        include("assistant_ai.urls"),
    ),
   
]


handler400 = "config.views.error_400"

handler403 = "config.views.error_403"

handler404 = "config.views.error_404"

handler500 = "config.views.error_500"
