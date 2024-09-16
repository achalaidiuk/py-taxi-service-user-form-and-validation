from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver, Car


class CleanLicenseNumberMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be 8 characters long."
            )
        if (not license_number[:3].isalpha()
                or not license_number[:3].isupper()):
            raise forms.ValidationError(
                "First 3 characters must be uppercase letters."
            )
        if not license_number[3:].isdigit():
            raise forms.ValidationError("Last 5 characters must be digits.")

        return license_number


class DriverCreationForm(CleanLicenseNumberMixin, UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number", "first_name", "last_name"
        )


class DriverLicenseUpdateForm(CleanLicenseNumberMixin, forms.ModelForm):
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
