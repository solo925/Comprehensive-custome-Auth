from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings
import datetime

class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            current_time = timezone.now()
            last_activity = request.session.get('last_activity')
            
            # Get timeout from settings, default 30 minutes
            timeout_seconds = getattr(settings, 'SESSION_COOKIE_AGE', 1800)
            
            if last_activity:
                last_activity = datetime.datetime.fromisoformat(last_activity)
                last_activity = last_activity.replace(tzinfo=timezone.utc)
                
                if (current_time - last_activity).total_seconds() > timeout_seconds:
                    logout(request)
                    messages.warning(request, "Your session has expired due to inactivity.")
                    # Don't store last_activity in this case
                    return
            
            # Update last activity
            request.session['last_activity'] = current_time.isoformat()