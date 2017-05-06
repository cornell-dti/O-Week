from django import forms

class BulkUploadForm(forms.Form):
    csvFile = forms.FileField()