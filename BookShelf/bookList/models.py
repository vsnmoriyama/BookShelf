from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class book(models.Model):                             #bookテーブル

    isbn = models.CharField(max_length=200)           #isbn
    picture_name = models.CharField(max_length=200)   #表紙
    title = models.CharField(max_length=200)          #書名
    author = models.CharField(max_length=200)         #著者
    publisher = models.CharField(max_length=200)      #出版社
    pubdate = models.DateField(default=timezone)      #出版日
