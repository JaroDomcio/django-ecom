from django.urls import path
from .views import *

urlpatterns = [
    path('home/', home, name='home'),
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', logout_user, name='logout'),
    path('profile-settings/',profile_settings, name='profile_settings'),
    path('product-details/<int:id>/', product_details, name='product_details'),
]