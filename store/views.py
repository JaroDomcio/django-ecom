from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Zalogowałeś się')
                return redirect('home')
            else:
                messages.success(request,"Nie udało ci się zalogować")

    else:
        form = LoginForm()
    return render(request,'login.html',{'form':form})


def logout_user(request):
    logout(request)
    messages.success(request, 'Wylogowałeś się')
    return redirect('home')