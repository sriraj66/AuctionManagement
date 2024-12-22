from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from authentication.forms import LoginForm,RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success,warning,error

TEMPLATE_ROOT = "auth/"


def user_login(request):
    if request.user.is_authenticated:
        return redirect("menu")
    
    if request.POST:
        form = LoginForm(data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect("menu")
    else:
        form = LoginForm()
        
    return render(request,"auth/login.html",{
        "form": form
    })


def user_register(request):
    
    if request.POST:
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect("index")
    else:
        form = RegisterForm()    
    return render(request,"auth/register.html",{
        "form": form
    })
    
@login_required
def user_logout(request):
    if request.POST:
        logout(request)
        success(request,"Good Bye")
    else:
        error(request,"Invalid Request !!")
    return redirect("user_login")

def menu(request):
    context = {}
    
    return render(request,"auth/menu.html",context)
