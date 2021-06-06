from django.urls import path,include
from .views import *
urlpatterns = [
    path('cart', cart, name="cart"),
  
]
