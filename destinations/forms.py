from django import forms

from .models import Destination


class DestinationForm(forms.ModelForm):

    latitude = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False,
    )

    longitude = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False,
    )

    state = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    country = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )


    class Meta:

        model = Destination

        fields = [
            "city",
            "state",
            "country",
            "latitude",
            "longitude",
            "notes",
        ]


        widgets = {

            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Search destination...",
                    "autocomplete": "off",
                }
            ),


            


            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Optional notes...",
                }
            ),

        }


    def clean_city(self):

        return self.cleaned_data["city"].strip()