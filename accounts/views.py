from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from destinations.models import Destination
from trips.models import Trip

from .forms import RegisterForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import PasswordResetOTP
from .services import OTPService
from .email_service import send_password_reset_otp

from .email_service import send_verification_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User



def home(request):
    return render(request, "home.html")


from django.contrib.auth.hashers import make_password
from .models import PendingUser



def register(request):

    if request.user.is_authenticated:
        return redirect("dashboard")


    if request.method == "POST":

        form = RegisterForm(request.POST)


        if form.is_valid():

            data = form.cleaned_data


            if User.objects.filter(
                username=data["username"]
            ).exists():

                messages.error(
                    request,
                    "Username already exists."
                )

                return render(
                    request,
                    "accounts/register.html",
                    {"form":form}
                )


            if User.objects.filter(
                email=data["email"]
            ).exists():

                messages.error(
                    request,
                    "Email already registered."
                )

                return render(
                    request,
                    "accounts/register.html",
                    {"form":form}
                )


            PendingUser.objects.filter(
                email=data["email"]
            ).delete()



            pending = PendingUser.objects.create(

                first_name=data["first_name"],

                last_name=data["last_name"],

                username=data["username"],

                email=data["email"],

                password=make_password(
                    data["password"]
                )

            )



            send_verification_email(
                pending,
                request
            )


            messages.success(
                request,
                "Verification email sent."
            )


            return redirect(
                "login"
            )


    else:

        form = RegisterForm()



    return render(
        request,
        "accounts/register.html",
        {
            "form":form
        }
    )

from django.shortcuts import get_object_or_404



def activate_account(request, token):


    pending = get_object_or_404(
        PendingUser,
        token=token
    )



    user = User.objects.create(

        first_name=pending.first_name,

        last_name=pending.last_name,

        username=pending.username,

        email=pending.email,

        password=pending.password,

        is_active=True

    )



    pending.delete()



    messages.success(
        request,
        "Email verified successfully. You can login now."
    )


    return redirect(
        "login"
    )




def user_login(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            messages.success(
                request,
                "Welcome back!"
            )

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "accounts/login.html"
    )


def user_logout(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("login")


@login_required
def dashboard(request):

    trips = Trip.objects.filter(
        user=request.user
    )

    total_trips = trips.count()

    upcoming_trips = trips.filter(
        start_date__gte=timezone.now().date()
    ).count()

    completed_trips = trips.filter(
        end_date__lt=timezone.now().date()
    ).count()

    total_destinations = Destination.objects.filter(
        trip__user=request.user
    ).count()

    recent_trips = trips.order_by(
        "-created_at"
    )[:5]

    context = {

        "total_trips": total_trips,

        "upcoming_trips": upcoming_trips,

        "completed_trips": completed_trips,

        "total_destinations": total_destinations,

        "recent_trips": recent_trips,

    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )



@login_required
def profile(request):

    user = request.user


    trips = Trip.objects.filter(
        user=user
    )


    total_trips = trips.count()


    total_destinations = Destination.objects.filter(
        trip__user=user
    ).count()



    completed_trips = 0


    for trip in trips:

        if trip.status == "Completed":

            completed_trips += 1



    return render(
        request,
        "accounts/profile.html",
        {
            "user": user,

            "total_trips": total_trips,

            "total_destinations": total_destinations,

            "completed_trips": completed_trips,
        }
    )



def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")

        user = User.objects.filter(
            email=email
        ).first()


        if user:

            otp = OTPService.generate()


            PasswordResetOTP.objects.filter(
                user=user
            ).delete()


            PasswordResetOTP.objects.create(
                user=user,
                otp=otp
            )


            send_password_reset_otp(
                user,
                otp
            )


            request.session["reset_email"] = email


            return redirect(
                "verify_otp"
            )


        messages.error(
            request,
            "Email not found."
        )


    return render(
        request,
        "accounts/forgot_password.html"
    )



def verify_otp(request):

    email = request.session.get(
        "reset_email"
    )


    if not email:
        return redirect(
            "forgot_password"
        )


    user = User.objects.get(
        email=email
    )


    if request.method == "POST":


        entered_otp = request.POST.get(
            "otp"
        )


        otp_obj = PasswordResetOTP.objects.filter(
            user=user,
            otp=entered_otp
        ).first()



        if otp_obj:


            if otp_obj.is_expired():

                messages.error(
                    request,
                    "OTP expired. Please request again."
                )


            else:

                otp_obj.is_verified = True

                otp_obj.save()


                return redirect(
                    "reset_password"
                )


        else:

            messages.error(
                request,
                "Invalid OTP."
            )


    return render(
        request,
        "accounts/verify_otp.html"
    )









