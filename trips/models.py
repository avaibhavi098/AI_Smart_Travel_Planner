import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone


class Trip(models.Model):


    TRANSPORT_CHOICES = [
        ("Car", "Car"),
        ("Bike", "Bike"),
        ("Bus", "Bus"),
        ("Train", "Train"),
        ("Flight", "Flight"),
        ("Mixed", "Mixed"),
    ]



    TRAVEL_STYLE_CHOICES = [

        ("Budget", "Budget"),

        ("Balanced", "Balanced"),

        ("Luxury", "Luxury"),

        ("Backpacking", "Backpacking"),

        ("Family", "Family"),

    ]



    FOOD_CHOICES = [

        ("Veg", "Veg"),

        ("Non Veg", "Non Veg"),

        ("Local Cuisine", "Local Cuisine"),

        ("No Preference", "No Preference"),

    ]



    BUDGET_PRIORITY_CHOICES = [

        ("Cheapest", "Cheapest"),

        ("Balanced", "Balanced"),

        ("Comfortable", "Comfortable"),

        ("Premium", "Premium"),

    ]



    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )



    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trips",
    )



    trip_name = models.CharField(
        max_length=200
    )



    # ==============================
    # SOURCE LOCATION (START POINT)
    # ==============================


    source_city = models.CharField(
        max_length=100,
        blank=True,
    )


    source_state = models.CharField(
        max_length=100,
        blank=True,
    )


    source_country = models.CharField(
        max_length=100,
        blank=True,
    )


    source_latitude = models.FloatField(
        null=True,
        blank=True,
    )


    source_longitude = models.FloatField(
        null=True,
        blank=True,
    )



    # ==============================
    # TRIP DETAILS
    # ==============================


    start_date = models.DateField()


    end_date = models.DateField()



    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )



    travelers = models.PositiveIntegerField(
        default=1
    )



    transport = models.CharField(
        max_length=20,
        choices=TRANSPORT_CHOICES,
    )



    # ==============================
    # PERSONALIZATION SETTINGS
    # ==============================


    travel_style = models.CharField(

        max_length=30,

        choices=TRAVEL_STYLE_CHOICES,

        default="Balanced",

    )



    food_preference = models.CharField(

        max_length=30,

        choices=FOOD_CHOICES,

        default="No Preference",

    )



    budget_priority = models.CharField(

        max_length=30,

        choices=BUDGET_PRIORITY_CHOICES,

        default="Balanced",

    )



    interests = models.JSONField(

        default=list,

        blank=True,

    )



    created_at = models.DateTimeField(
        auto_now_add=True
    )



    updated_at = models.DateTimeField(
        auto_now=True
    )



    @property
    def trip_days(self):

        return (
            self.end_date - self.start_date
        ).days + 1



    @property
    def status(self):

        today = timezone.now().date()


        if today < self.start_date:

            return "Upcoming"


        if self.start_date <= today <= self.end_date:

            return "Ongoing"


        return "Completed"

    @property
    def source_location(self):

        location = []

        if self.source_city:
            location.append(self.source_city)

        if self.source_state:
            location.append(self.source_state)

        if self.source_country:
            location.append(self.source_country)

        return ", ".join(location)


    @property
    def has_source(self):

        return bool(
            self.source_city
        )

    def __str__(self):

        return self.trip_name