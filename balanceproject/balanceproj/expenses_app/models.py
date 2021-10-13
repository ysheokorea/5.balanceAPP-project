from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return str(self.name)

class Expenses(models.Model):
    date=models.DateField()
    category=models.CharField(max_length=255)
    amount = models.IntegerField()
    description=models.TextField()
    person=models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return str(self.name)