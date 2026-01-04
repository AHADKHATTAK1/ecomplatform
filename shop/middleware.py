from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from .models import Store


class StoreMiddleware(MiddlewareMixin):
    """
    Middleware to detect and set the current store based on:
    1. Custom domain (if configured)
    2. URL slug pattern (/store/<slug>/)
    
    ALSO blocks admin/dashboard access on custom domains for security
    """
    
    def process_request(self, request):
        store = None
        host = request.get_host().split(':')[0]  # Remove port if present
        
        # Try to match custom domain first
        is_custom_domain = False
        try:
            store = Store.objects.get(domain=host, is_active=True)
            is_custom_domain = True
        except Store.DoesNotExist:
            # Check if URL contains store slug pattern
            path_parts = request.path.strip('/').split('/')
            if len(path_parts) >= 2 and path_parts[0] == 'store':
                store_slug = path_parts[1]
                try:
                    store = Store.objects.get(slug=store_slug, is_active=True)
                except Store.DoesNotExist:
                    pass
        
        # Security: Block admin/dashboard access on custom domains
        if is_custom_domain:
            # Block admin, dashboard, and other management URLs
            blocked_paths = ['/admin/', '/dashboard/', '/my-stores/', '/create-store/']
            for blocked in blocked_paths:
                if request.path.startswith(blocked):
                    return HttpResponseForbidden(
                        "<h1>Access Denied</h1>"
                        "<p>Admin access is not available on this domain.</p>"
                        "<p>Please use the main platform to access your dashboard.</p>"
                    )
        
        # Attach store to request
        request.store = store
        request.is_custom_domain = is_custom_domain
        return None
