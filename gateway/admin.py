from django.contrib import admin
from gateway.models import *
# Register your models here.
admin.site.register(Account)
admin.site.register(Bank)
admin.site.register(Transaction)