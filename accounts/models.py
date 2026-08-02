from django.db import models
from django.contrib.auth.models import User
import uuid


class PasswordResetOTP(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    otp = models.CharField(
        max_length=6
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_verified = models.BooleanField(
        default=False
    )


    def is_expired(self):

        from django.utils import timezone

        return (
            timezone.now() - self.created_at
        ).total_seconds() > 60




class PendingUser(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )


    first_name = models.CharField(
        max_length=150
    )


    last_name = models.CharField(
        max_length=150
    )


    username = models.CharField(
        max_length=150
    )


    email = models.EmailField()


    password = models.CharField(
        max_length=255
    )


    token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )