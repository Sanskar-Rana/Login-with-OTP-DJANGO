from django.urls import path
from .views import *

urlpatterns = [
  path('', login_attempt, name="login"),
  path('register', register, name="register"),
  path('otp', otp, name="otp"),
  path('login-otp', login_otp, name="login_otp"),
]
