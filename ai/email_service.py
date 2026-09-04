from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .pdf_service import ItineraryPDFService



class ItineraryEmailService:


    @staticmethod
    def send_itinerary_email(user, trip, itinerary):


        subject = f"Your AI Travel Plan - {trip.trip_name}"


        # Plain text fallback
        text_content = f"""
Hi {user.username},

Your AI generated travel itinerary is ready.

Trip:
{trip.trip_name}

Budget:
₹{trip.budget}

Your detailed PDF itinerary is attached.

Enjoy your journey!

AI Smart Travel Planner
"""


        # Render HTML template
        html_content = render_to_string(

            "emails/itinerary_email.html",

            {
                "user": user,
                "trip": trip,
                "itinerary": itinerary,
            }

        )


        email = EmailMultiAlternatives(

            subject,

            text_content,

            settings.DEFAULT_FROM_EMAIL,

            [user.email],

        )


        # IMPORTANT LINE
        # This makes Gmail render HTML

        email.attach_alternative(

            html_content,

            "text/html"

        )


        # Generate PDF

        pdf = ItineraryPDFService.generate_pdf(

            trip,

            itinerary

        )


        email.attach(

            f"{trip.trip_name}_Itinerary.pdf",

            pdf,

            "application/pdf"

        )


        email.send()