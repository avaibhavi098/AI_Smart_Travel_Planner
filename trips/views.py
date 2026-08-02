from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from destinations.services import GeoapifyService
from destinations.models import Destination
from .forms import TripForm
from .models import Trip
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ai.models import AIItinerary
from .forms import TripForm
from .models import Trip
# from .services import GeoapifyService
from .email_service import PreferenceEmailService


@login_required
def trip_list(request):

    trips = (
        Trip.objects.filter(user=request.user)
        .order_by("-created_at")
    )

    return render(
        request,
        "trips/trip_list.html",
        {
            "trips": trips,
        },
    )





@login_required
def create_trip(request):

    if request.method == "POST":

        form = TripForm(request.POST)


        if form.is_valid():

            trip = form.save(commit=False)


            trip.user = request.user


            # SOURCE LOCATION DATA

            source_state = request.POST.get(
                "source_state"
            )

            source_country = request.POST.get(
                "source_country"
            )

            source_latitude = request.POST.get(
                "source_latitude"
            )

            source_longitude = request.POST.get(
                "source_longitude"
            )


            # Use selected location data first

            if source_state:

                trip.source_state = source_state


            if source_country:

                trip.source_country = source_country


            if source_latitude:

                trip.source_latitude = source_latitude


            if source_longitude:

                trip.source_longitude = source_longitude



            # If coordinates not available,
            # fetch from Geoapify

            if not source_latitude or not source_longitude:


                location = GeoapifyService.get_location(
                    trip.source_city
                )


                if location:


                    trip.source_state = (
                        location.get("state","")
                    )


                    trip.source_country = (
                        location.get("country","")
                    )


                    trip.source_latitude = (
                        location.get("lat")
                    )


                    trip.source_longitude = (
                        location.get("lon")
                    )



            trip.save()

            PreferenceEmailService.send_preference_mail(
                request.user,
                trip
            )

            return redirect(
                "trips:trip_detail",
                id=trip.id
            )


    else:

        form = TripForm()



    return render(
        request,
        "trips/create_trip.html",
        {
            "form":form
        }
    )



@login_required
def trip_detail(request, id):

    trip = get_object_or_404(
        Trip,
        pk=id,
        user=request.user,
    )

    destinations = (
        Destination.objects.filter(trip=trip)
        .order_by("order", "city")
    )

    return render(
        request,
        "trips/trip_detail.html",
        {
            "trip": trip,
            "destinations": destinations,
            "destination_count": destinations.count(),
        },
    )


@login_required
def edit_trip(request, id):

    trip = get_object_or_404(
        Trip,
        pk=id,
        user=request.user,
    )


    if request.method == "POST":


        old_values = {

            "source_city": trip.source_city,
            "budget": trip.budget,
            "transport": trip.transport,
            "travel_style": trip.travel_style,
            "food_preference": trip.food_preference,
            "start_date": trip.start_date,
            "end_date": trip.end_date,
            "travelers": trip.travelers,
            "interests": trip.interests,

        }



        form = TripForm(
            request.POST,
            instance=trip,
        )



        if form.is_valid():


            trip = form.save(
                commit=False
            )



            if trip.source_city:


                location = GeoapifyService.get_location(
                    trip.source_city
                )


                if location:


                    trip.source_city = location.get(
                        "city",
                        trip.source_city
                    )


                    trip.source_state = location.get(
                        "state",
                        ""
                    )


                    trip.source_country = location.get(
                        "country",
                        ""
                    )


                    trip.source_latitude = location.get(
                        "latitude"
                    )


                    trip.source_longitude = location.get(
                        "longitude"
                    )



            trip.save()



            new_values = {

                "source_city": trip.source_city,
                "budget": trip.budget,
                "transport": trip.transport,
                "travel_style": trip.travel_style,
                "food_preference": trip.food_preference,
                "start_date": trip.start_date,
                "end_date": trip.end_date,
                "travelers": trip.travelers,
                "interests": trip.interests,

            }



            trip_changed = (
                old_values != new_values
            )



            if trip_changed:


                if hasattr(trip, "itinerary"):


                    messages.warning(
                        request,
                        "Your trip details changed. Your AI itinerary may be outdated. Please regenerate your itinerary."
                    )


                else:


                    messages.success(
                        request,
                        "Trip updated successfully!"
                    )


            else:


                messages.success(
                    request,
                    "Trip updated successfully!"
                )



            return redirect(
                "trips:trip_detail",
                id=trip.id
            )



    else:


        form = TripForm(
            instance=trip
        )



    return render(
        request,
        "trips/edit_trip.html",
        {
            "form": form,
            "trip": trip,
        },
    )



@login_required
def delete_trip(request, id):

    trip = get_object_or_404(
        Trip,
        pk=id,
        user=request.user,
    )

    if request.method == "POST":

        trip.delete()

        messages.success(
            request,
            "Trip deleted successfully!"
        )

        return redirect("trips:trip_list")

    return render(
        request,
        "trips/delete_trip.html",
        {
            "trip": trip,
        },
    )