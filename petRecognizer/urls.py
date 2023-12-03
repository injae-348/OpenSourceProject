from django.urls import path

from . import views

urlpatterns = [
    path('pet/',views.first_page, name='first_page'),
    path('pet_result/',views.second_page,name='second_page'),
]