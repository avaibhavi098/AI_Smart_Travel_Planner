from django.contrib import admin
from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):

    list_display = (
        "trip_name",
        "user",
        "start_date",
        "end_date",
        "transport",
        "trip_days",
        "status",
    )

    search_fields = (
        "trip_name",
        "user__username",
    )

    list_filter = (
        "transport",
    )

    ordering = (
        "-created_at",
    )