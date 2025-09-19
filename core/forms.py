# core/forms.py

from django import forms
from .models import Case, Comment
from django.contrib.auth.models import User

class CaseForm(forms.ModelForm):

    class Meta:
        model = Case
        fields = ['title', 'description', 'category']

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['title', 'description', 'category', 'image_file']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'image_file']