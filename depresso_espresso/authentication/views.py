from django.shortcuts import render, redirect  
from .register import Register
from django.contrib.auth import login, authenticate
# Create your views here.  

# https://www.techwithtim.net/tutorials/django/user-registration   
# https://www.youtube.com/watch?v=lHYzmlx2Vso&list=PLbMO9c_jUD44i7AkA4gj1VSKvCFIf59fb&index=7

def register(request):  
    if request.method == 'POST':  
        print(request.POST)
        form = Register(request.POST)
        
        if form.is_valid():  
            user = form.save()
            login(request, user)
            #return redirect('/userself/profile') # should redirect to user's new profile on creation
            return redirect('/')    
        
        else:
        
            for error in list(form.errors.values()):
                print(request, error)
                
    else:
        form = Register()

    return render(request, "dist/index.html")

# https://stackoverflow.com/questions/75401759/how-to-set-up-login-view-in-python-django
def loginview(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user:
            login(request, user)
            return redirect('/')
        

    return render(request, 'dist/index.html')




def index(request):
    return render(request, "dist/index.html")

'''
    

    
'''
