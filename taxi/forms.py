from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator, MaxLengthValidator

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}\d{5}$",
                message="License number must consist of"
                        " 3 uppercase letters followed by 5 digits."
            ),
            MaxLengthValidator(
                8, "License number must be exactly 8 characters."
            )
        ]
    )
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number", "first_name", "last_name"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = ["manufacturer", "model", "drivers"]
