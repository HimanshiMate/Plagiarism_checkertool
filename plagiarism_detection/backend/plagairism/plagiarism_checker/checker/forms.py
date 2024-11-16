from django import forms
from checker.models import RegiModel

class RegistrationForm(forms.ModelForm):
    class Meta:
        model= RegiModel
        fields='__all__'

class LoginForm(forms.ModelForm):
    class Meta:
        model =  RegiModel
        fields=('email','password')