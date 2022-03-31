from django.urls import path
from gateway.views import *
urlpatterns = [
    path('', home, name='dashboard'),
    path('login/',loginApp, name="login"),
    path('logout/',logoutApp,name='logout'),
    path('transaction-history/',transaction_history,name='transactions'),
    path('receive/',receive,name='receive'),
    path('profile/',profile,name='profile'),
    path('under-construction/',forgotpassword,name='forgotpassword'),
    path('signup/',signup,name='signup'),
    path('bank-details/',bankdetails,name='bankdetails'),
    path('edit-profile/',editprofile,name='editprofile'), 
    path('send/',send,name='send'),
    path('transaction-failed/',transaction_failed,name='transactionfailed'),
    path('transaction-success/',transaction_successful,name='transactionsuccessful')
]