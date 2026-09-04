from django.urls import path
from . import views

app_name = "ai"

urlpatterns = [

    path(
        "<uuid:trip_id>/generate/",
        views.generate_itinerary,
        name="generate_itinerary",
    ),

    path(
        "<uuid:trip_id>/regenerate/",
        views.regenerate_itinerary,
        name="regenerate_itinerary",
    ),
    path(
    "<uuid:trip_id>/send-email/",
    views.send_itinerary_email,
    name="send_itinerary_email",
    ),


]