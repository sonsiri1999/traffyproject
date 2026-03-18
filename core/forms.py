# core/forms.py

from django import forms
from .models import Case, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['title', 'description', 'category', 'image_file']


class CaseEditForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['description', 'image_file']
        labels = {
            'description': 'คำอธิบายเคส',
            'image_file': 'รูปภาพประกอบ',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'image_file']

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        import re
        # อนุญาตเฉพาะตัวอักษรภาษาอังกฤษ (a-z, A-Z), ตัวเลข (0-9) และ @/./+/-/_
        if not re.match(r'^[a-zA-Z0-9@.+\-_]+$', username):
            raise forms.ValidationError(
                'ชื่อผู้ใช้ต้องประกอบด้วยตัวอักษรภาษาอังกฤษ ตัวเลข หรือ @/./+/-/_ เท่านั้น (ไม่อนุญาตภาษาไทยหรืออักษรอื่น)'
            )
        return username

class EditProfileForm(UserChangeForm):
    # ปิดฟิลด์รหัสผ่านในฟอร์มนี้ มีฟอร์มแยกต่างหาก
    password = None 

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'ชื่อจริง',
            'last_name': 'นามสกุล',
            'email': 'อีเมล',
        }