from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse


def send_password_reset_otp(user, otp):

    subject = "AI Smart Travel Planner Password Reset OTP"


    html_content = f"""

<!DOCTYPE html>

<html>

<body style="
background:#f1f5ff;
font-family:Arial;
padding:30px;
">


<div style="
max-width:600px;
margin:auto;
background:white;
padding:35px;
border-radius:24px;
">


<h1 style="
text-align:center;
color:#2563eb;
">

✈️ AI Smart Travel Planner

</h1>


<h2>
Password Reset OTP
</h2>


<p>
Hello {user.username},
</p>


<p>
Your OTP is:
</p>



<h1 style="
text-align:center;
background:#2563eb;
color:white;
padding:15px;
border-radius:15px;
letter-spacing:8px;
">

{otp}

</h1>



<p>
This OTP is valid for 60 seconds.
</p>



<hr>


<p style="
text-align:center;
color:#64748b;
">

AI Smart Travel Planner ❤️

</p>


</div>


</body>

</html>

"""


    email = EmailMultiAlternatives(

        subject,

        "",

        settings.EMAIL_HOST_USER,

        [user.email]

    )


    email.attach_alternative(
        html_content,
        "text/html"
    )


    email.send()





from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_verification_email(pending_user, request):

    link = request.build_absolute_uri(
        f"/activate/{pending_user.token}/"
    )


    subject = "Verify your AI Smart Travel Planner Account"


    html_content = f"""

<!DOCTYPE html>

<html>

<head>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

body {{

    margin:0;
    padding:15px;
    background:#f1f5ff;
    font-family:Arial,Helvetica,sans-serif;

}}


.email-container {{

    width:100%;
    max-width:600px;
    margin:auto;
    background:#ffffff;
    border-radius:22px;
    padding:35px 25px;
    box-sizing:border-box;

}}


.logo {{

    text-align:center;
    color:#2563eb;
    font-size:28px;
    font-weight:bold;

}}


.heading {{

    color:#1e293b;
    font-size:24px;

}}


.text {{

    color:#475569;
    font-size:16px;
    line-height:1.6;

}}


.verify-box {{

    text-align:center;
    margin:35px 0;

}}


.verify-btn {{

    display:inline-block;
    background:#2563eb;
    color:white!important;
    padding:15px 35px;
    border-radius:50px;
    text-decoration:none;
    font-weight:bold;
    font-size:16px;

}}


.info-box {{

    background:#eff6ff;
    padding:15px;
    border-radius:12px;
    color:#1e40af;
    font-size:14px;

}}


.footer {{

    text-align:center;
    color:#94a3b8;
    font-size:14px;

}}



@media only screen and (max-width:600px){{


body {{

    padding:8px;

}}


.email-container {{

    padding:25px 18px;
    border-radius:18px;

}}


.logo {{

    font-size:22px;

}}


.heading {{

    font-size:20px;

}}


.text {{

    font-size:15px;

}}


.verify-btn {{

    width:100%;
    padding:15px 0;
    box-sizing:border-box;

}}


}}


</style>

</head>


<body>


<div class="email-container">


<div class="logo">

✈️ AI Smart Travel Planner

</div>


<hr>


<h2 class="heading">

Welcome {pending_user.username}! 🎉

</h2>



<p class="text">

Thanks for joining AI Smart Travel Planner.

Please verify your email address to activate your account.

</p>



<div class="verify-box">


<a href="{link}"

class="verify-btn">

Verify Email Address

</a>


</div>



<div class="info-box">

🔒 This verification link is secure.

</div>



<p class="text">

If you did not create this account, ignore this email.

</p>



<hr>



<div class="footer">

AI Smart Travel Planner ❤️

<br>

Plan smarter. Travel better.

</div>



</div>


</body>

</html>

"""


    email = EmailMultiAlternatives(

        subject,

        "Please verify your email address.",

        settings.EMAIL_HOST_USER,

        [pending_user.email]

    )


    email.attach_alternative(
        html_content,
        "text/html"
    )


    email.send()

    