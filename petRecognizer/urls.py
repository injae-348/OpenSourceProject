from django.urls import path

from . import views

urlpatterns = [
    path('pet/',views.index, name='first-page'),
    
]