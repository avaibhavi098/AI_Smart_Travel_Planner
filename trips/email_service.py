from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string



class PreferenceEmailService:


    @staticmethod
    def send_preference_mail(user, trip):


        subject = f"Personalized Travel Tips For {trip.trip_name}"


        html_content = render_to_string(

            "emails/preference_mail.html",

            {

                "user":user,

                "trip":trip,

            }

        )


        email = EmailMultiAlternatives(

            subject,

            "",

            settings.DEFAULT_FROM_EMAIL,

            [user.email]

        )


        email.attach_alternative(

            html_content,

            "text/html"

        )


        email.send()