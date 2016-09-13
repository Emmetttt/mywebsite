from django import forms

from .models import Band


# class BandForm(forms.ModelForm):
#     class Meta:
#         model = Band
#         fields = ('band_name',)

class BandForm(forms.Form):
	band_input = forms.CharField(label='Band Name', max_length=50)