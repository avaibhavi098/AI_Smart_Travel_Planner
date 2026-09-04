from django.urls import path
from . import views
app_name = "trips"
urlpatterns = [

    path(
        "",
        views.trip_list,
        name="trip_list"
    ),

    path(
        "create/",
        views.create_trip,
        name="create_trip"
    ),

    path(
        "<uuid:id>/",
        views.trip_detail,
        name="trip_detail"
    ),

    path(
        "<uuid:id>/edit/",
        views.edit_trip,
        name="edit_trip"
    ),

    path(
        "<uuid:id>/delete/",
        views.delete_trip,
        name="delete_trip"
    ),
]