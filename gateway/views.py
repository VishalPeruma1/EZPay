import re
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
def home(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email == 'abc@gmail.com' and password == 'acb':
            return redirect('dashboard')
        else: 
            return HttpResponse('Invalid Response')
    return render(request, 'gateway/login.html')

def dashboard(request):
    return HttpResponse('Authentication Successful') 