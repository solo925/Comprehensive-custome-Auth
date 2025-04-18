from django.utils.deprecation import MiddlewareMixin

class RoleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            # role-based permissions to request
            if request.user.role:
                request.role = request.user.role
                # all permissions from the role to the user session
                perms = list(request.user.role.permissions.values_list('codename', flat=True))
                request.role_permissions = perms
            else:
                request.role = None
                request.role_permissions = []
        return None