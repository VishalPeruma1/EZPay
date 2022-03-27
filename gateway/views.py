from cmath import log
import re
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from gateway.decorators import unAuthenticated_user

@unAuthenticated_user
def loginApp(request):
    if request.method == 'POST':
        phonenumber = request.POST.get('phonenumber')
        password = request.POST.get('password')
        if phonenumber == '' or password == '':
            return render(request, 'gateway/login.html', {'error':'ERROR: All fields are mandatory!'})
        else:
            user = authenticate(request, username=phonenumber, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'gateway/login.html', {'error': 'Invalid credentials'})

    return render(request, 'gateway/login.html')

@login_required(login_url='login')
def logoutApp(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    return HttpResponse('Authentication Successful') 

