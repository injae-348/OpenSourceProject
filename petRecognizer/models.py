from django.db import models


class PetImage(models.Model):

    image = models.ImageField(upload_to='petImage')
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pet Image {self.id}"


