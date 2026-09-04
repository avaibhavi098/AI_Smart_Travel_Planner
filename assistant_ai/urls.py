from django.urls import path

from . import views


app_name = "assistant_ai"


urlpatterns = [

    path(
        "<uuid:trip_id>/",
        views.chat_page,
        name="chat_page",
    ),

    path(
        "<uuid:trip_id>/send/",
        views.send_message,
        name="send_message",
    ),

    path(
        "<uuid:trip_id>/history/",
        views.chat_history,
        name="chat_history",
    ),

]