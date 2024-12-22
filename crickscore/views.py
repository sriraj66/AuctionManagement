from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.messages import warning,error

TEMPLATE_ROOT = "crickscore/"

@login_required
def boards(request):
    
    if not request.user.is_staff:
        error(request,"Invaid User")
        warning(request,"Login As ADMIN")
        logout(request)
        return redirect("user_login")
    
    context = {}
    return render(request,TEMPLATE_ROOT+"boards.html",context)

@login_required
def create_match(request):
    
    if not request.user.is_staff:
        error(request,"Invaid User")
        warning(request,"Login As ADMIN")
        logout(request)
        return redirect("user_login")
    
    context = {}
    return render(request,TEMPLATE_ROOT+"matchcreation.html",context)