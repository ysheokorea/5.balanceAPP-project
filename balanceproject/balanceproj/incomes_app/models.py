from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.

class Source(models.Model):
    name=models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class Incomes(models.Model):
    date=models.DateField()
    source=models.CharField(max_length=200)
    amount= models.IntegerField()
    description=models.TextField()
    person = models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return str(self.date)
        
    
