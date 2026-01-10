# core/forms.py

from django import forms
from .models import Case, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('username',)

class EditProfileForm(UserChangeForm):
    # ปิดฟิลด์รหัสผ่านในฟอร์มนี้ เพราะเรามีฟอร์มแยกต่างหาก
    password = None 

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'ชื่อจริง',
            'last_name': 'นามสกุล',
            'email': 'อีเมล',
        }