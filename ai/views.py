from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from markdown import markdown

from trips.models import Trip
from destinations.models import Destination

from .models import AIItinerary
from .services import AIItineraryService
from .email_service import ItineraryEmailService



def get_ordered_destinations(trip):

    destinations = list(

        Destination.objects
        .filter(
            trip=trip
        )
        .order_by(
            "order"
        )

    )

    return destinations





@login_required
def generate_itinerary(request, trip_id):

    trip = get_object_or_404(

        Trip,

        id=trip_id,

        user=request.user

    )


    destinations = get_ordered_destinations(
        trip
    )



    existing_itinerary = (

        AIItinerary.objects
        .filter(
            trip=trip
        )
        .first()

    )



    if existing_itinerary:


        itinerary = markdown(

            existing_itinerary.content

        )


    else:


        generated_itinerary = (

            AIItineraryService.generate_itinerary(

                trip,

                destinations

            )

        )



        AIItinerary.objects.create(

            trip=trip,

            content=generated_itinerary

        )


        itinerary = markdown(

            generated_itinerary

        )



    return render(

        request,

        "ai/itinerary.html",

        {

            "trip": trip,

            "itinerary": itinerary,

        }

    )







@login_required
def regenerate_itinerary(request, trip_id):


    trip = get_object_or_404(

        Trip,

        id=trip_id,

        user=request.user

    )



    destinations = get_ordered_destinations(

        trip

    )



    AIItinerary.objects.filter(

        trip=trip

    ).delete()



    generated_itinerary = (

        AIItineraryService.generate_itinerary(

            trip,

            destinations

        )

    )



    AIItinerary.objects.create(

        trip=trip,

        content=generated_itinerary

    )



    return redirect(

        "ai:generate_itinerary",

        trip.id

    )








@login_required
def send_itinerary_email(request, trip_id):


    trip = get_object_or_404(

        Trip,

        id=trip_id,

        user=request.user

    )



    itinerary = (

        AIItinerary.objects
        .filter(
            trip=trip
        )
        .first()

    )



    if itinerary:


        ItineraryEmailService.send_itinerary_email(

            request.user,

            trip,

            itinerary.content

        )



        messages.success(

            request,

            "Itinerary sent successfully to your email."

        )



    return redirect(

        "ai:generate_itinerary",

        trip.id

    )