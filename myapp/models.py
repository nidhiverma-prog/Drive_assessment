from django.db import models

# Create your models here.
class Movies(models.Model):
    title=models.CharField(max_length=50,default=None)
    reviews=models.CharField(max_length=50,default=None)

    def __str__(self):
        return self.title
