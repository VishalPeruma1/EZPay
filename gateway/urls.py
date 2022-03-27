from django.urls import path
from gateway.views import *
urlpatterns = [
    path('', home, name='home'),
    path('success/',dashboard, name="dashboard"),

]