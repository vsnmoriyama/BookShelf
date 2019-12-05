from django.db import models
import datetime

# Create your models here.
class book(models.Model):
    isbn = models.CharField(max_length=200)
    picture_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    auther = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    pubdate = models.DateField()

    def pubdateTochar(self):

        print(self.pubdate)
