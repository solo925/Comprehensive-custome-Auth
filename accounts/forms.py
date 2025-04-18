from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from .models import User

class CaptchaAuthenticationForm(AuthenticationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'captcha']
        
class CaptchaRegistrationForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'captcha']