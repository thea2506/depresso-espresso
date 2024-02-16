from django.shortcuts import render, redirect  
from .register import Register
from django.contrib.auth import login
# Create your views here.  

# https://www.techwithtim.net/tutorials/django/user-registration   
# https://www.youtube.com/watch?v=lHYzmlx2Vso&list=PLbMO9c_jUD44i7AkA4gj1VSKvCFIf59fb&index=7
def register(request):  
    if request.method == 'POST':  
        form = Register(request.POST)
        if form.is_valid():  
            user = form.save()
            login(request, user)
            #return redirect('/userself/profile') # should redirect to user's new profile on creation
            return redirect('/')    
        
    else:
        form = Register()

    return render(
        request=request,
        template_name = "test_register.html",
        context={"form: form"}
    )

    

