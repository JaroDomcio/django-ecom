from django.urls import path
from .views import *

urlpatterns = [
    path('cart/', cart , name='cart'),
    path('cart-delete', cart_delete, name='cart-delete'),
    path('cart-add', cart_add, name='cart-add'),
    path('cart-update', cart_update, name='cart-update'),
]