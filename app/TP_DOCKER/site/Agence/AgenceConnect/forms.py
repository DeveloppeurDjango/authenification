from django.db import models
from django import forms


class ContactForm(forms.Form):
    nom = forms.CharField(max_length=100)
    prenoms = forms.CharField(max_length=100)
    email = forms.EmailField()
    sujet = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

