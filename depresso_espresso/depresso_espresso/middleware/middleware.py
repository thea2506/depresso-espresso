import re
from django.conf import settings
from django.shortcuts import redirect

# Check if user is logged in
# Code taken from https://stackoverflow.com/a/74512029

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

class LoginRequiredMiddleware:
    pass
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__ (self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request,'user')
        path = request.path_info.lstrip('/')
        
        #if not request.user.is_authenticated:
        #    if not any(url.match(path) for url in EXEMPT_URLS):
         #       return redirect(settings.LOGIN_URL)
    