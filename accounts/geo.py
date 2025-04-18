from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
import logging

logger = logging.getLogger(__name__)

class GeoIPMiddleware(MiddlewareMixin):
    """
    Check if user's country is allowed
    """
    def process_request(self, request):
        if settings.DEBUG:  
            return None
            
        try:
            # Get client IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
                
            # Skip for localhost
            if ip == '127.0.0.1' or ip == '::1':
                return None
                
            # Check country
            g = GeoIP2()
            country = g.country(ip)
            
            if country['country_code'] not in settings.ALLOWED_COUNTRIES:
                logger.warning(f"Access blocked for IP {ip} from {country['country_name']}")
                return HttpResponseForbidden("Access from your country is not allowed.")
                
        except Exception as e:
            logger.error(f"GeoIP error: {str(e)}")
            
        return None