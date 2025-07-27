from django.urls import path
from .views import *

urlpatterns = [
    path('home/', home, name='home'),
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
]