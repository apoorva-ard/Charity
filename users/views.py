from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .forms import RegisterForm
from django.db import IntegrityError

def register(request):
    if (request.method=='POST'):
        form = RegisterForm(request.POST)
        if(form.is_valid()):
            try:
                form.save()
            except IntegrityError as e:
                context = {'form': form}
                messages.info(request, 'Username is already taken')
                return render(request, 'users/register.html', context)
            cleaned = form.cleaned_data
            uname = cleaned.get('username')
            messages.success(request, f'Account created for {uname}!')
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)

def login(request):
    if(request.method=='POST'):
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        
        user = authenticate(request, username=uname, password=pwd)

        if(user is not None):
            auth_login(request, user)
            return redirect('app-home')
        else:
            messages.info(request, 'Username or password is incorrect')
    context={'nbar':'login'}
    return render(request, 'users/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('app-home')