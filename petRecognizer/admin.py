from django.contrib import admin

# Register your models here.
from .models import PetImage, PetBreed

admin.site.register(PetImage)
admin.site.register(PetBreed)
