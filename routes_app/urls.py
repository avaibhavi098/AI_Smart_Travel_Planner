from django.urls import path
from . import views

app_name = "routes"


urlpatterns = [

    path(
        "<uuid:trip_id>/",
        views.route_map,
        name="route_map",
    ),

]