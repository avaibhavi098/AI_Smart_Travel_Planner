from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


    accept_terms = forms.BooleanField(
        required=True,
        error_messages={
            "required": "You must accept the Terms and Conditions."
        },
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input"
            }
        )
    )


    class Meta:

        model = User

        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]


        widgets = {

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),


            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),


            "username": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),


            "email": forms.EmailInput(
                attrs={
                    "class": "form-control"
                }
            ),

        }



    def clean(self):

        cleaned = super().clean()


        password = cleaned.get(
            "password"
        )


        confirm_password = cleaned.get(
            "confirm_password"
        )


        if password and confirm_password:

            if password != confirm_password:

                raise forms.ValidationError(
                    "Passwords do not match."
                )


        return cleaned