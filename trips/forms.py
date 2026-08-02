from django import forms
from .models import Trip


class TripForm(forms.ModelForm):

    INTEREST_CHOICES = [

        ("Adventure", "🏔 Adventure"),
        ("Beaches", "🏖 Beaches"),
        ("Mountains", "⛰ Mountains"),
        ("Food", "🍴 Food"),
        ("History", "🏛 History"),
        ("Photography", "📸 Photography"),
        ("Wildlife", "🦁 Wildlife"),
        ("Shopping", "🛍 Shopping"),

    ]


    interests = forms.MultipleChoiceField(

        choices=INTEREST_CHOICES,

        widget=forms.CheckboxSelectMultiple,

        required=False,

    )



    class Meta:

        model = Trip


        fields = [

            "trip_name",

            "source_city",

            "start_date",

            "end_date",

            "budget",

            "travelers",

            "transport",

            "travel_style",

            "food_preference",

            "budget_priority",

            "interests",

        ]



        widgets = {


            "start_date": forms.DateInput(

                attrs={
                    "type": "date",
                    "class": "form-control"
                }

            ),


            "end_date": forms.DateInput(

                attrs={
                    "type": "date",
                    "class": "form-control"
                }

            ),



            "budget": forms.NumberInput(

                attrs={
                    "class": "form-control",
                    "placeholder": "Enter budget"
                }

            ),



            "travelers": forms.NumberInput(

                attrs={
                    "class": "form-control",
                    "min": 1
                }

            ),



            "source_city": forms.TextInput(

                attrs={
                    "class": "form-control",
                    "placeholder": "Search starting city"
                }

            ),



            "trip_name": forms.TextInput(

                attrs={
                    "class": "form-control",
                    "placeholder": "Enter trip name"
                }

            ),



            "transport": forms.Select(

                attrs={
                    "class": "form-select"
                }

            ),



            "travel_style": forms.RadioSelect(

                attrs={
                    "class": "form-check-input"
                }

            ),



            "food_preference": forms.RadioSelect(

                attrs={
                    "class": "form-check-input"
                }

            ),



            "budget_priority": forms.RadioSelect(

                attrs={
                    "class": "form-check-input"
                }

            ),

        }



    def save(self, commit=True):

        instance = super().save(commit=False)


        instance.interests = self.cleaned_data.get(
            "interests",
            []
        )


        if commit:

            instance.save()


        return instance