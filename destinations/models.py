import uuid

from django.core.exceptions import ValidationError
from django.db import models

from trips.models import Trip


class Destination(models.Model):


    PLACE_TYPES = [

        ("City", "City"),
        ("Hill Station", "Hill Station"),
        ("Beach", "Beach"),
        ("Temple", "Temple"),
        ("Heritage", "Heritage"),
        ("Wildlife", "Wildlife"),
        ("Other", "Other"),

    ]


    id = models.UUIDField(

        primary_key=True,

        default=uuid.uuid4,

        editable=False,

    )


    trip = models.ForeignKey(

        Trip,

        on_delete=models.CASCADE,

        related_name="destinations",

    )


    city = models.CharField(

        max_length=100

    )


    state = models.CharField(

        max_length=100,

        blank=True,

    )


    country = models.CharField(

        max_length=100,

        blank=True,

    )


    latitude = models.FloatField(

        null=True,

        blank=True,

    )


    longitude = models.FloatField(

        null=True,

        blank=True,

    )


    estimated_cost = models.DecimalField(

        max_digits=10,

        decimal_places=2,

        default=0,

    )


    place_type = models.CharField(

        max_length=30,

        choices=PLACE_TYPES,

        default="City",

    )


    notes = models.TextField(

        blank=True

    )


    order = models.PositiveIntegerField(

        editable=False,

        db_index=True,

        null=True,

        blank=True,

    )


    # ==============================
    # ROUTE DETAILS
    # ==============================


    distance_from_previous = models.FloatField(

        null=True,

        blank=True,

        help_text="Distance from previous location in KM"

    )


    travel_time_from_previous = models.CharField(

        max_length=100,

        blank=True,

        help_text="Travel duration from previous location"

    )



    class Meta:


        ordering = [

            "order"

        ]


        constraints = [


            models.UniqueConstraint(

                fields=[

                    "trip",

                    "city"

                ],

                name="unique_destination_per_trip",

            ),



            models.UniqueConstraint(

                fields=[

                    "trip",

                    "order"

                ],

                name="unique_destination_order_per_trip",

            ),


        ]



    @property
    def location_name(self):


        data = []


        if self.city:

            data.append(self.city)


        if self.state:

            data.append(self.state)


        if self.country:

            data.append(self.country)



        return ", ".join(data)



    def clean(self):


        if self.trip_id:


            duplicate = (

                Destination.objects

                .filter(

                    trip=self.trip,

                    city__iexact=self.city,

                )

                .exclude(

                    pk=self.pk

                )

            )


            if duplicate.exists():

                raise ValidationError(

                    {

                        "city":

                        "This destination already exists in this trip."

                    }

                )



    def save(self, *args, **kwargs):


        self.full_clean()



        # Automatically assign order


        if self.order is None:


            last_order = (

                Destination.objects

                .filter(

                    trip=self.trip

                )

                .aggregate(

                    models.Max("order")

                )

                .get(

                    "order__max"

                )

            )


            self.order = (

                last_order or 0

            ) + 1



        super().save(*args, **kwargs)



    def __str__(self):

        return self.city