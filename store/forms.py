from django.contrib.auth.models import User
from django import forms
from store.models import Contact, UserProfileInfo


class FormContact(forms.ModelForm):
    name = forms.CharField(max_length=150, label="Name", widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': "Your Name",
        'required': "required"
    }))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Email',
        'required': 'required'
    }))
    subject = forms.CharField(max_length=250, label="Subject", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': "Subject",
        'required': 'required'
    }))
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Message',
        'rows': '5',
        'required': 'required',
    }))

    class Meta:
        model = Contact
        fields = '__all__'


class FormUser(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Username", widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': "Username",
        'required': "required"
    }))
    email = forms.CharField(max_length=150, label="Email", widget=forms.EmailInput(attrs={
        'class': "form-control",
        'placeholder': "Email",
        'required': "required"
    }))
    password = forms.CharField(max_length=150, label="Password", widget=forms.PasswordInput(attrs={
        'class': "form-control",
        'placeholder': "Password",
        'required': "required"
    }))
    confirm_password = forms.CharField(max_length=150, label="Confirm Password", widget=forms.PasswordInput(attrs={
        'class': "form-control",
        'placeholder': "Confirm Password",
        'required': "required"
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class FormUserProfileInfo(forms.ModelForm):
    portfolio = forms.URLField(label='Portfolio', required=False, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Portfolio",
    }))
    image = forms.ImageField(label='Image', widget=forms.FileInput(attrs={
        "class": "form-control-file"
    }))

    class Meta:
        model = UserProfileInfo
        exclude = ('user',)