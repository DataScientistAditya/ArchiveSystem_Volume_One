from logging import PlaceHolder
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import models
from django.db.models import fields
from django.forms import Form
from django.forms.models import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import Account, UploadDocuments
from .backends import AccountAuth




class Register_Forms(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Enter Your Password here"}),validators=[validate_password])
	email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Enter Your Email here"}))
	username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter Your Username here"}))
	class Meta:
		model = Account
		fields = ("email", "username", "password")
		label = {

			"email": "Email",
			"username": "Username",
			"password": "Password",

		}



class AccountAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Email", required=True ,widget=forms.EmailInput(attrs={"placeholder":"Enter Your Registered email"}))
    password =  forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Enter Your Registered password"}), required=True)


class OTP_form(forms.Form):
	Otp = forms.IntegerField(label="Enter OTP to Verify")

class Reset_Password_Form(forms.Form):
    Email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder":"Enter Your Registered Email"}))
    
class Reset_Password(forms.Form):
    Password_one = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"placeholder":"Please enter New Password"}))
    Password_two = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"placeholder":"Repeat Password"}))

class UploadDocumentsForm(ModelForm):
	class Meta:
		model = UploadDocuments
		fields = ("Name","Document","Thumbnail", "Category", "Language")
		label = {

			"Name": "Name",
			"Document": "Document(Upload pdf only)",
			"Thumbnail": "Thumbnail(Upload pdf Image)",
			"Category": "Category",
			"Language": "Language",

		}