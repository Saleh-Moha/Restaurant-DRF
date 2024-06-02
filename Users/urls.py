from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('user-profile/<int:pk>', User_Profile.as_view() ),
]