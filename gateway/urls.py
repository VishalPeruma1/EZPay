from django.urls import path
from gateway.views import *
urlpatterns = [
    path('', home, name='dashboard'),
    path('login/',loginApp, name="login"),
    path('logout/',logoutApp,name='logout')

]