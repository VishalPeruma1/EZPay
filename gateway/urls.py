from django.urls import path
from gateway.views import *
urlpatterns = [
    path('', home, name='dashboard'),
    path('login/',loginApp, name="login"),
    path('logout/',logoutApp,name='logout'),
    path('transactions/',transaction_history,name='transactions'),
    path('receive/',receive,name='receive'),
    path('profile/',profile,name='profile'),
    path('under_construction/',forgotpassword,name='forgotpassword'),
    path('signup/',signup,name='signup'),
    path('bankdetails/',bankdetails,name='bankdetails'),
    path('editprofile/',editprofile,name='editprofile'), 
    path('send/',send,name='send')

]