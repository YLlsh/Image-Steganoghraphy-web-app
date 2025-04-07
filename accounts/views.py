from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def R_page(request):
    if request.method =='POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, "Username is already exists")
            return redirect('/R_page/')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username)
            
        user.set_password(password)
        user.save()    
        messages.info(request, "Account create sucessfully")

        return redirect('/R_page/')

    return render(request,"R_page.html")

def L_page(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user is None:
            messages.info(request,"Username or password is worng")
            return redirect('/l_page/')
        else:
            login(request,user)
            return redirect('/encode/')

    return render(request,"L_page.html")

def l_out(request):
    logout(request)
    return redirect('/l_page/')
