from django.urls import path

from . import views

urlpatterns = [
    path('pet/',views.index),
]