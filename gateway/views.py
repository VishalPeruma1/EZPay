from cmath import log
import re
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from gateway.decorators import unAuthenticated_user
from gateway.models import Account, Transaction
from django.db.models import Q
import qrcode
import hashlib

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
    acc_holder = Account.objects.get(user=User.objects.get(id=request.user.id))
    transactions =list(Transaction.objects.filter(Q(sender = acc_holder) | Q(receiver = acc_holder)))[:5]
    return render(request, 'gateway/dashboard.html', {'user': acc_holder, 'transactions': transactions})

@login_required(login_url='login')
def transaction_history(request):
    acc_holder = Account.objects.get(user=User.objects.get(id=request.user.id))
    transactions = Transaction.objects.filter(Q(sender = acc_holder) | Q(receiver = acc_holder))
    return render(request, 'gateway/transaction.html', {'user': acc_holder, 'transactions': transactions})

@login_required(login_url='login')
def receive(request):
    acc_holder = Account.objects.get(user=User.objects.get(id=request.user.id))
    encrypted_string=hashlib.sha256(str(acc_holder.phone_number).encode())
    img=qrcode.make(encrypted_string)
    img.save("static/my_qr.png")
    return render(request, 'gateway/receive.html', {'user': acc_holder})