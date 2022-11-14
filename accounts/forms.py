from django import forms
# from jsonschema import ValidationError
from .models import Account,UserProfile
class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':"Enter password",
        'class':'form-control'
    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':"Confirm password",
        'class':'form-control'
    }))
    email=forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder':"Enter email",
        'class':'form-control'
    }))
    first_name=forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':"Enter first name",
        'class':'form-control'
    }))
    last_name=forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':"Enter last name",
        'class':'form-control'
    }))
    phone_number=forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':"Enter Phone Number",
        'class':'form-control'
    }))
    class Meta:
        model=Account
        fields=['first_name','last_name','phone_number','email','password']

    def clean(self):
        cleaned_data=super(RegistrationForm,self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        if password!=confirm_password:
            raise forms.ValidationError(
                'password does not match'
            )

class UserForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=['first_name','last_name','phone_number']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['address_line_1','address_line_2','city','state','country',]