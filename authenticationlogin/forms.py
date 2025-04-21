from django import forms
from .models import AuthenticatedUser

class SignupForm(forms.ModelForm):
    class Meta:
        model = AuthenticatedUser
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# from django import forms
from shop.models import WebsiteLogo

class LogoUploadForm(forms.ModelForm):
    class Meta:
        model = WebsiteLogo
        fields = ['image']
