from django.urls import path
from . import views

app_name = "destinations"


urlpatterns = [

    path(
        "search/",
        views.search_destinations,
        name="search_destinations",
    ),

    path(
        "<uuid:trip_id>/",
        views.destination_list,
        name="destination_list",
    ),

    path(
        "<uuid:trip_id>/add/",
        views.add_destination,
        name="add_destination",
    ),

    path(
        "<uuid:trip_id>/reorder/",
        views.reorder_destinations,
        name="reorder_destinations",
    ),

    path(
        "<uuid:id>/edit/",
        views.edit_destination,
        name="edit_destination",
    ),

    path(
        "<uuid:id>/delete/",
        views.delete_destination,
        name="delete_destination",
    ),

    path(
        "<uuid:trip_id>/map/",
        views.trip_map,
        name="trip_map",
    ),
    path(
    "<uuid:trip_id>/builder/",
    views.destination_builder,
    name="destination_builder"
    ),
]