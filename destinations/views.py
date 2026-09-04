from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

import json
from math import radians, sin, cos, sqrt, atan2

from trips.models import Trip
from .forms import DestinationForm
from .models import Destination
from .services import GeoapifyService



def calculate_distance(lat1, lon1, lat2, lon2):

    if not all([
        lat1,
        lon1,
        lat2,
        lon2
    ]):
        return None


    earth_radius = 6371


    lat1 = radians(lat1)
    lon1 = radians(lon1)

    lat2 = radians(lat2)
    lon2 = radians(lon2)


    dlat = lat2 - lat1
    dlon = lon2 - lon1


    a = (
        sin(dlat / 2) ** 2
        +
        cos(lat1)
        *
        cos(lat2)
        *
        sin(dlon / 2) ** 2
    )


    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )


    return round(
        earth_radius * c,
        2
    )



def calculate_travel_time(distance):

    if not distance:
        return ""


    hours = round(
        distance / 50,
        1
    )

    return f"{hours} hrs"





@login_required
def search_destinations(request):

    query = request.GET.get(
        "q",
        ""
    ).strip()


    places = GeoapifyService.search_places(
        query
    )


    return JsonResponse(
        places,
        safe=False
    )





@login_required
def reorder_destinations(request, trip_id):

    trip = get_object_or_404(
        Trip,
        id=trip_id,
        user=request.user,
    )


    if request.method != "POST":

        return JsonResponse(
            {
                "success":False
            },
            status=405
        )


    data = json.loads(
        request.body
    )


    order = data.get(
        "order",
        []
    )


    with transaction.atomic():

        Destination.objects.filter(
            trip=trip
        ).update(
            order=F("order") + 1000
        )


        for index, destination_id in enumerate(
            order,
            start=1
        ):

            Destination.objects.filter(
                id=destination_id,
                trip=trip,
            ).update(
                order=index
            )


    return JsonResponse(
        {
            "success":True
        }
    )





@login_required
def destination_list(request, trip_id):

    trip = get_object_or_404(
        Trip,
        id=trip_id,
        user=request.user,
    )


    destinations = (
        Destination.objects
        .filter(
            trip=trip
        )
        .order_by(
            "order"
        )
    )


    return render(
        request,
        "destinations/list.html",
        {
            "trip":trip,
            "destinations":destinations,
        },
    )





@login_required
def add_destination(request, trip_id):

    trip = get_object_or_404(
        Trip,
        id=trip_id,
        user=request.user,
    )


    if request.method == "POST":

        form = DestinationForm(
            request.POST
        )


        if form.is_valid():

            destination = form.save(
                commit=False
            )


            destination.trip = trip



            location = GeoapifyService.get_location(
                destination.city
            )


            if location:

                destination.state = location.get(
                    "state",
                    ""
                )

                destination.country = location.get(
                    "country",
                    ""
                )

                destination.latitude = location.get(
                    "latitude"
                )

                destination.longitude = location.get(
                    "longitude"
                )



            previous_destination = (
                Destination.objects
                .filter(
                    trip=trip
                )
                .order_by(
                    "-order"
                )
                .first()
            )



            if previous_destination:

                distance = calculate_distance(

                    previous_destination.latitude,

                    previous_destination.longitude,

                    destination.latitude,

                    destination.longitude

                )

            else:

                distance = calculate_distance(

                    trip.source_latitude,

                    trip.source_longitude,

                    destination.latitude,

                    destination.longitude

                )



            destination.distance_from_previous = distance

            destination.travel_time_from_previous = (
                calculate_travel_time(distance)
            )


            destination.save()



            messages.success(
                request,
                "Destination added successfully!"
            )


            return redirect(
                "destinations:destination_list",
                trip_id=trip.id,
            )


    else:

        form = DestinationForm()



    return render(
        request,
        "destinations/add.html",
        {
            "trip":trip,
            "form":form,
        },
    )


@login_required
def destination_builder(request, trip_id):

    trip = get_object_or_404(
        Trip,
        id=trip_id,
        user=request.user,
    )


    if request.method == "POST":

        cities = request.POST.getlist(
            "destinations[]"
        )


        previous_destination = (
            Destination.objects
            .filter(
                trip=trip
            )
            .order_by(
                "-order"
            )
            .first()
        )


        for city in cities:


            city = city.strip()


            if not city:
                continue



            destination = Destination(
                trip=trip,
                city=city
            )



            location = GeoapifyService.get_location(
                city
            )


            if location:

                destination.state = location.get(
                    "state",
                    ""
                )

                destination.country = location.get(
                    "country",
                    ""
                )

                destination.latitude = location.get(
                    "latitude"
                )

                destination.longitude = location.get(
                    "longitude"
                )



            if previous_destination:


                distance = calculate_distance(

                    previous_destination.latitude,

                    previous_destination.longitude,

                    destination.latitude,

                    destination.longitude

                )


            else:


                distance = calculate_distance(

                    trip.source_latitude,

                    trip.source_longitude,

                    destination.latitude,

                    destination.longitude

                )



            destination.distance_from_previous = distance


            destination.travel_time_from_previous = (
                calculate_travel_time(distance)
            )


            destination.save()


            previous_destination = destination



        messages.success(
            request,
            "All destinations added successfully!"
        )


        return redirect(
            "destinations:destination_list",
            trip_id=trip.id,
        )



    return render(
        request,
        "destinations/builder.html",
        {
            "trip":trip
        },
    )





@login_required
def edit_destination(request, id):

    destination = get_object_or_404(
        Destination,
        id=id,
        trip__user=request.user,
    )


    trip = destination.trip



    if request.method == "POST":

        form = DestinationForm(
            request.POST,
            instance=destination,
        )


        if form.is_valid():

            destination = form.save(
                commit=False
            )


            previous_destination = (
                Destination.objects
                .filter(
                    trip=trip
                )
                .exclude(
                    id=destination.id
                )
                .order_by(
                    "-order"
                )
                .first()
            )


            if previous_destination:

                distance = calculate_distance(

                    previous_destination.latitude,

                    previous_destination.longitude,

                    destination.latitude,

                    destination.longitude

                )

            else:

                distance = calculate_distance(

                    trip.source_latitude,

                    trip.source_longitude,

                    destination.latitude,

                    destination.longitude

                )


            destination.distance_from_previous = distance

            destination.travel_time_from_previous = (
                calculate_travel_time(distance)
            )


            destination.save()



            messages.success(
                request,
                "Destination updated successfully!"
            )


            return redirect(
                "destinations:destination_list",
                trip.id,
            )


    else:

        form = DestinationForm(
            instance=destination
        )


    return render(
        request,
        "destinations/edit.html",
        {
            "destination":destination,
            "form":form,
        },
    )





@login_required
def delete_destination(request, id):

    destination = get_object_or_404(
        Destination,
        id=id,
        trip__user=request.user,
    )


    trip = destination.trip


    if request.method == "POST":

        deleted_order = destination.order


        destination.delete()


        remaining = (
            Destination.objects
            .filter(
                trip=trip,
                order__gt=deleted_order,
            )
            .order_by(
                "order"
            )
        )


        for item in remaining:

            item.order -= 1

            item.save(
                update_fields=[
                    "order"
                ]
            )


        messages.success(
            request,
            "Destination deleted successfully!"
        )


        return redirect(
            "destinations:destination_list",
            trip_id=trip.id,
        )


    return render(
        request,
        "destinations/delete.html",
        {
            "destination":destination,
        },
    )





@login_required
def trip_map(request, trip_id):

    trip = get_object_or_404(
        Trip,
        id=trip_id,
        user=request.user,
    )


    destinations = (
        Destination.objects
        .filter(trip=trip)
        .order_by("order")
    )


    route_coordinates = []


    # SOURCE POINT

    if trip.source_latitude and trip.source_longitude:

        route_coordinates.append(
            [
                float(trip.source_longitude),
                float(trip.source_latitude)
            ]
        )


    # DESTINATIONS

    for destination in destinations:

        if destination.latitude and destination.longitude:

            route_coordinates.append(
                [
                    float(destination.longitude),
                    float(destination.latitude)
                ]
            )


    # RETURN TO SOURCE

    if trip.source_latitude and trip.source_longitude:

        route_coordinates.append(
            [
                float(trip.source_longitude),
                float(trip.source_latitude)
            ]
        )


    geometry = {
        "coordinates": route_coordinates
    }


    return render(
        request,
        "destinations/map.html",
        {
            "trip": trip,
            "destinations": destinations,
            "geometry": geometry,
        }
    )









