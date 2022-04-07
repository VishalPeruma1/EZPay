from cmath import log
import re
from unicodedata import decimal, name
from webbrowser import get
from django.dispatch import receiver
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from gateway.decorators import unAuthenticated_user
from gateway.models import Account, Bank, Transaction
from django.db.models import Q
import qrcode
import hashlib
from django.contrib.auth.password_validation import validate_password

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

@unAuthenticated_user
def forgotpassword(request):
    return render(request,'gateway/construction.html')

@unAuthenticated_user
def signup(request):
    data = {}
    if request.method == 'POST':
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        phonenumber = request.POST.get('phone_no')
        emailaddress = request.POST.get('email')
        address = request.POST.get('address')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')
        dob = request.POST.get('dob')
        if firstname == '' or lastname == '' or phonenumber == '' or address == '' or password == '' or password_repeat == '' or dob == '' or emailaddress == '':
            return render(request, 'gateway/general-register.html', {'error':'ERROR: All fields are mandatory! '})
        else: 
            if password != password_repeat:
                return render(request, 'gateway/general-register.html', {'error':'ERROR: Passwords do not match! '})
            else:
                try:
                    v = validate_password(password) 
                    userobj = User.objects.create_user (
                        username = str(phonenumber),
                        password = password
                    )
                    account = Account (
                        first_name = firstname,
                        last_name = lastname,
                        dob = dob, 
                        phone_number = phonenumber, 
                        email_address = emailaddress,
                        address = address, 
                        user = userobj
                    )
                    account.save()
                    user = authenticate(request, username=phonenumber, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('bankdetails') 
                except ValidationError as v:
                    errorstr = '\n'.join(v)
                    return render(request, 'gateway/general-register.html', {'error': errorstr}) 
    return render(request,'gateway/general-register.html')

@login_required(login_url='login')
def bankdetails(request):
    acc_holder = Account.objects.filter(user=User.objects.get(id=request.user.id))
    banks = Bank.objects.all()
    if request.method=='POST':
        bankname = request.POST.get('bank')
        acc_number = request.POST.get('acc_number')
        mpin = request.POST.get('mpin')
        mpin_repeat = request.POST.get('mpin_repeat')
        if bankname == '' or acc_number == '' or mpin == '' or mpin_repeat == '':
            return render(request, 'gateway/bank-register.html', {'error':'ERROR: All fields are mandatory! '})
        else:
            if mpin != mpin_repeat:
                return render(request, 'gateway/bank-register.html', {'error':'ERROR: MPINs do not match! '})
            if len(acc_number)!=10:
                return render(request, 'gateway/bank-register.html', {'error':'ERROR: Invalid Account Number! '})
            else:
                banknamee, branch_name = bankname.split(', ')
                bankobj = Bank.objects.get(name = banknamee, branch_name = branch_name)
                acc_holder.update(
                    acc_number = acc_number,
                    mpin = mpin, 
                    bank = bankobj
                )

                return redirect('dashboard')    
    return render(request,'gateway/bank-register.html', {'banks': banks})

@login_required(login_url='login')
def logoutApp(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    acc_holder = Account.objects.get(user=User.objects.get(id=request.user.id))
    transactions =list(Transaction.objects.filter(Q(sender = acc_holder) | Q(receiver = acc_holder)))[-5:]
    return render(request, 'gateway/dashboard.html', {'user': acc_holder, 'transactions': transactions})

@login_required(login_url='login')
def transaction_history(request):
    acc_holder = Account.objects.get(user=User.objects.get(id=request.user.id))
    transactions = Transaction.objects.filter(Q(sender = acc_holder) | Q(receiver = acc_holder))
    return render(request, 'gateway/transaction-history.html', {'user': acc_holder, 'transactions': transactions})

@login_required(login_url='login')
def receive(request):
    acc_holder = Account.objects.get(user=User.objects.get(id=request.user.id))
    encrypted_string=hashlib.sha256(str(acc_holder.phone_number).encode())
    img=qrcode.make(encrypted_string)
    img.save("static/my_qr.png")
    return render(request, 'gateway/receive.html', {'user': acc_holder})

@login_required(login_url='login')
def profile(request):
    acc_holder = Account.objects.get(user=User.objects.get(id=request.user.id))
    return render(request, 'gateway/profile.html', {'user': acc_holder})

@login_required(login_url='login')
def editprofile(request):
    acc_holder = Account.objects.filter(user=User.objects.get(id=request.user.id))
    acc_holder_ = Account.objects.get(user=User.objects.get(id=request.user.id))

    if request.method=='POST':
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        phonenumber = request.POST.get('phone_no')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        address = request.POST.get('address')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')
        if firstname == '' or lastname == '' or phonenumber == '' or dob == '' or email == '' or address == '' or password == '' or password_repeat == '':
            return render(request, 'gateway/edit-profile.html', {'error':'ERROR: All fields are mandatory! '})
        else:
            if password != password_repeat: 
                return render(request, 'gateway/edit-profile.html', {'error':'ERROR: Passwords do not match! '})
            else:
                try:
                    v = validate_password(password) 
                    acc_holder.update(
                        first_name = firstname,
                        last_name = lastname, 
                        phone_number = phonenumber,
                        email_address = email, 
                        dob = dob,
                        address = address, 
                    )
                    userobj = User.objects.get(id = request.user.id)
                    userobj.set_password(password_repeat)
                    userobj.save()
                except ValidationError as v:
                    errorstr = '\n'.join(v)
                    return render(request, 'gateway/edit-profile.html', {'error': errorstr}) 
                
    return render(request, 'gateway/edit-profile.html', {'user': acc_holder_})

@login_required(login_url='login')
def transaction_failed(request):
    acc_holder = Account.objects.get(user=User.objects.get(id=request.user.id))
    return render(request, 'gateway/transaction-failed.html', {'user': acc_holder})

@login_required(login_url='login')
def transaction_successful(request):
    acc_holder = Account.objects.get(user=User.objects.get(id=request.user.id))
    return render(request, 'gateway/transaction-successful.html', {'user': acc_holder})

@login_required(login_url='login')
def send(request):
    acc_holder = Account.objects.get(user=User.objects.get(id=request.user.id))
    acc_receiver  = Account.objects.all()

    if request.method=='POST':
        rec_phone_number = request.POST.get('phone_no')
        mpin = request.POST.get('mpin')
        amount = request.POST.get('amount')
        phones = list(Account.objects.all().values_list('phone_number', flat=True))
        if not int(rec_phone_number) in phones:
            return redirect('transactionfailed')
        else: 
            if len(rec_phone_number) == 10:
                if (acc_holder.balance > 0.0 and acc_holder.balance >= float(amount) and float(amount) > 0):
                    if (int(mpin)==acc_holder.mpin):
                        iSender = acc_holder
                        iReceiver = Account.objects.get(phone_number = int(rec_phone_number))
                        iReceiver.balance = iReceiver.balance + float(amount)
                        iSender.balance = iSender.balance - float(amount)
                        acc_holder.save()
                        iReceiver.save()
                        print(type(rec_phone_number))
                        transaction = Transaction.objects.create(
                            sender = acc_holder,
                            receiver = acc_receiver.get(phone_number = int(rec_phone_number)),
                            amount = float(amount)
                        )
                        transactions = Transaction.objects.get(id=transaction.id)
                        return render(request, 'gateway/transaction-successful.html', {'transactions': transactions , 'receiver': iReceiver})
                    else: 
                        return redirect('transactionfailed')
                else: 
                    return redirect('transactionfailed')
    return render(request, 'gateway/send.html', {'user': acc_holder})


