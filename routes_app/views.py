from django.contrib import messages 
from django.contrib.auth.decorators import login_required 
from django.db import transaction 
from django.db.models import F 
from django.shortcuts import get_object_or_404, redirect, render 
from destinations.models import Destination 
from routes_app.services import OSRMService
from trips.models import Trip


@login_required
def route_map(request, trip_id):

    trip = get_object_or_404(
        Trip,
        id=trip_id,
        user=request.user,
    )


    destinations = list(
        Destination.objects.filter(
            trip=trip
        ).order_by(
            "order",
            "city"
        )
    )


    # Add source as first point
    if (
        trip.source_latitude is not None
        and trip.source_longitude is not None
    ):

        source = Destination(
            trip=trip,
            city=trip.source_city,
            state=trip.source_state,
            country=trip.source_country,
            latitude=trip.source_latitude,
            longitude=trip.source_longitude,
            order=0,
        )

        source.is_source = True

        destinations.insert(
            0,
            source
        )


    for destination in destinations:

        if not hasattr(destination, "is_source"):

            destination.is_source = False



    if len(destinations) < 2:

        messages.warning(
            request,
            "Add a starting location and at least one destination.",
        )

        return redirect(
            "destinations:destination_list",
            trip_id=trip.id,
        )


    missing = [
        destination.city
        for destination in destinations
        if destination.latitude is None
        or destination.longitude is None
    ]


    if missing:

        messages.error(
            request,
            "Some locations do not have valid coordinates.",
        )

        return redirect(
            "destinations:destination_list",
            trip_id=trip.id,
        )


    result = OSRMService.optimize_route(
        destinations
    )


    if not result:

        messages.error(
            request,
            "Unable to optimize the route.",
        )

        return redirect(
            "destinations:destination_list",
            trip_id=trip.id,
        )


    try:

        trip_data = result["trips"][0]

        waypoints = result["waypoints"]


    except (KeyError, IndexError):

        messages.error(
            request,
            "Invalid route received from OSRM.",
        )

        return redirect(
            "destinations:destination_list",
            trip_id=trip.id,
        )



    optimized_destinations = [None] * len(destinations)


    for destination, waypoint in zip(
        destinations,
        waypoints
    ):

        index = waypoint.get(
            "waypoint_index"
        )

        if index is not None:

            optimized_destinations[index] = destination



    optimized_destinations = [
        destination
        for destination in optimized_destinations
        if destination is not None
    ]



    geometry = trip_data.get(
        "geometry"
    )


    if geometry is None:

        geometry = {
            "coordinates": []
        }



    context = {

        "trip": trip,

        "destinations": optimized_destinations,

        "geometry": geometry,

        "distance": round(
            trip_data.get(
                "distance",
                0
            ) / 1000,
            2,
        ),

        "duration": round(
            trip_data.get(
                "duration",
                0
            ) / 3600,
            2,
        ),

        "optimized": True,

    }


    return render(
        request,
        "routes/route_map.html",
        context,
    )