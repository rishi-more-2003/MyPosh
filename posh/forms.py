from django import forms
from .models import Education, EstablishmentLocation, PEDetails, VendorDetails

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['school', 'degree', 'field_of_study', 'start_date', 'end_date', 'grade', 'description']

class EstablishmentLocationForm(forms.ModelForm):
    class Meta:
        model = EstablishmentLocation
        exclude = ['username']

class PEDetailsForm(forms.ModelForm):
    class Meta:
        model = PEDetails
        exclude = ['username']

class VendorDetailsForm(forms.ModelForm):
    class Meta:
        model = VendorDetails
        exclude = ['username']
