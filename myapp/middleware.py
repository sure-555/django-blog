from django.shortcuts import redirect
from django.urls import reverse

class RedirectAuthenticatedUser:
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self,request):
        #check the use is authenticated
        if request.user.is_authenticated:
                paths_to_redirect=[reverse('alpha:login'),reverse('alpha:register'),reverse('alpha:forgot_password')]
                if request.path in paths_to_redirect:
                     return redirect(reverse('alpha:index'))
        
        return(self.get_response(request))
    
class RestrictUnauthenticatedUser:
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self,request):
        #check the use is not authenticated
        paths_to_restrict=[reverse('alpha:dashboard')]
        if not request.user.is_authenticated and request.path in paths_to_restrict:
                return redirect(reverse('alpha:login'))
        
        return(self.get_response(request))