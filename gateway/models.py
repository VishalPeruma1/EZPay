import random
import uuid
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# class User extends
class Bank(models.Model):
    name = models.CharField(max_length=25)
    ifsc_code = models.CharField(max_length=25)
    branch_name = models.CharField(max_length=25)
    address = models.TextField()

    def __str__(self):
        return self.name + ', ' + self.branch_name

class Account(models.Model):
    acc_number = models.BigIntegerField(max_length=10, null=True, default = 0)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    dob = models.CharField(null=True, max_length=25) 
    phone_number = models.BigIntegerField(max_length=15)
    email_address = models.EmailField()
    mpin = models.IntegerField(max_length=6, null=True)
    address = models.TextField()
    balance = models.FloatField(default=0.0, max_length=10)

    def __str__(self):
        return str(self.acc_number)
        
    

class Transaction(models.Model):
    id = models.CharField(unique=True, primary_key=True, editable=False, default=uuid.uuid4, max_length=256)
    sender = models.ForeignKey(Account, on_delete=models.DO_NOTHING,related_name='sender')
    receiver = models.ForeignKey(Account, on_delete=models.DO_NOTHING,related_name='receiver')
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(max_length=7)

    def __str__(self):
        return str(self.id)

@receiver(post_save, sender=Account)
def updateAccountNumber(sender, instance, **kwargs):
    if instance.acc_number == 0:
        num = random.randint(1000000000,9999999999)
        unique_confirm =  list(Account.objects.all().values_list('acc_number', flat=True)) 
        while num in unique_confirm: 
            num= random.randint(1000000000,9999999999)
        Account.objects.filter(id = instance.id).update(acc_number = num)

