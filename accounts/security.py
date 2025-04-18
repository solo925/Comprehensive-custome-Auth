from django.utils.deprecation import MiddlewareMixin

class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add security headers to all responses
    """
    def process_response(self, request, response):
        # Content Security Policy
        response['Content-Security-Policy'] = "default-src 'self'; script-src 'self' https://cdnjs.cloudflare.com; style-src 'self' https://cdnjs.cloudflare.com; img-src 'self' data:; font-src 'self'; connect-src 'self'"
        
        # Prevent browsers from MIME-sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # XSS Protection
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Prevent clickjacking
        response['X-Frame-Options'] = 'DENY'
        
        # HSTS (already in settings.py for production)
        # response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # Referrer Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Feature Policy
        response['Feature-Policy'] = "geolocation 'none'; microphone 'none'; camera 'none'"
        
        return response