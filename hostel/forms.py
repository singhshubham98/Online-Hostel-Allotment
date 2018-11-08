
import re
from django import forms
from django.contrib.auth.models import User
from .models import Student, Diff, Room
from django.core.validators import EmailValidator
from django.utils.timezone import datetime


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('Email is already taken!!')
        if not EmailValidator(email):
            raise forms.ValidationError('Email does not exist!')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError(
                'Password length at least 8 characters')
        return password

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'[A-Za-z]{3,}', first_name):
            raise forms.ValidationError('Name is not valid!')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'[A-Za-z]{3,}', last_name):
            raise forms.ValidationError('Name is not valid!')
        return last_name


class DiffForm(forms.ModelForm):
    class Meta:
        model = Diff
        fields = ('is_student',)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('gender', 'father_name', 'date_of_birth', 'fee_receipt',
                  'address', 'city', 'state', 'pincode', 'join_year')

    def clean_join_year(self):
        join_year = self.cleaned_data.get('join_year')
        if not (join_year > 2013 and join_year <= datetime.now().year):
            raise forms.ValidationError('Please enter valid Join year')
        return join_year

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if not len(str(pincode)) == 6:
            raise forms.ValidationError('Please enter valid Pincode')
        return pincode

    def clean_father_name(self):
        father_name = self.cleaned_data.get('father_name')
        if not re.match(r'[A-Za-z]{3,}', father_name):
            raise forms.ValidationError('Name is not valid!')
        return father_name


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('room_no',)
