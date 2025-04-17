from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login-history/', views.login_history, name='login_history'),
    path('profile/', views.profile, name='profile'),

    # 2FA URLs
    path('setup-2fa/', views.setup_2fa, name='setup_2fa'),
    path('disable-2fa/', views.disable_2fa, name='disable_2fa'),
    
    # API endpoints
    path('api/profile/', views.user_profile_api, name='api_profile'),
    path('api/login-history/', views.login_history_api, name='api_login_history'),
]