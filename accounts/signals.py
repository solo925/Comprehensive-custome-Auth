from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from .models import LoginHistory, User
from django.utils import timezone

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    # Update user's last login IP
    if isinstance(user, User):
        user.last_login_ip = ip
        user.save(update_fields=['last_login_ip'])
    
    # Create login history entry
    LoginHistory.objects.create(
        user=user,
        ip_address=ip,
        user_agent=user_agent,
        status='success'
    )

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    if user:
        ip = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        LoginHistory.objects.create(
            user=user,
            ip_address=ip,
            user_agent=user_agent,
            status='logout'
        )

@receiver(user_login_failed)
def user_login_failed_handler(sender, credentials, request, **kwargs):
    username = credentials.get('username', '')
    try:
        user = User.objects.get(email=username)
        ip = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        LoginHistory.objects.create(
            user=user,
            ip_address=ip,
            user_agent=user_agent,
            status='failed'
        )
    except User.DoesNotExist:
        pass  # Can't log history if we don't know the user

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip