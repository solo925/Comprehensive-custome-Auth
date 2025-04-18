from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from accounts.forms import (
    CaptchaAuthenticationForm, 
    CaptchaRegistrationForm,
    CaptchaPasswordResetForm,
    CaptchaSetPasswordForm
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Override allauth views with our custom forms
    path('accounts/login/', auth_views.LoginView.as_view(
        form_class=CaptchaAuthenticationForm,
        template_name='allauth/account/login.html'
    ), name='account_login'),
    
    path('accounts/signup/', auth_views.LoginView.as_view(
        form_class=CaptchaRegistrationForm,
        template_name='allauth/account/signup.html'
    ), name='account_signup'),
    
    path('accounts/password/reset/', auth_views.PasswordResetView.as_view(
        form_class=CaptchaPasswordResetForm,
        template_name='allauth/account/password_reset.html'
    ), name='account_reset_password'),
    
    path('accounts/password/reset/key/<uidb36>-<key>/', auth_views.PasswordResetConfirmView.as_view(
        form_class=CaptchaSetPasswordForm,
        template_name='allauth/account/password_reset_from_key.html'
    ), name='account_reset_password_from_key'),
    
    # Default authentication URLs
    path('accounts/', include('allauth.urls')),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    
    # JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Include your accounts app URLs
    path('accounts/', include('accounts.urls')),
    
    # Homepage (just for testing)
    path('', login_required(TemplateView.as_view(template_name='home.html')), name='home'),
]