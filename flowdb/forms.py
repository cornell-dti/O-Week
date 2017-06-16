# forms.py
# Arnav Ghosh
# 16th June 2017

from django import forms
from django.forms import ModelForm

from .models import EventDetail, Category

class BulkUploadForm(forms.Form):
    csvFile = forms.FileField()

class EventDetailForm(ModelForm):
	class Meta:
		model = EventDetail
		fields = ['name', 'description', 'location', 'category', 'images', 'required',
				  'start_date', 'end_date', 'start_time', 'end_time']
		
class CategoriesForm(ModelForm):
	class Meta:
		model = Category
		fields = ['category', 'description']