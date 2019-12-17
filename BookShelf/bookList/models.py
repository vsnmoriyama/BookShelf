from django.db import models


class book(models.Model):                                   # bookテーブル

    isbn = models.CharField(max_length=200)                 # isbn
    picture_name = models.CharField(max_length=200)         # 表紙
    title = models.CharField(max_length=200)                # 書名
    author = models.CharField(max_length=200)               # 著者
    publisher = models.CharField(max_length=200)            # 出版社
    pubdate = models.DateField()                            # 出版日
    genre = models.CharField(max_length=200, null=True)     # ジャンルコード
    text = models.CharField(max_length=500, null=True)      # 概要
    price = models.CharField(max_length=200, null=True)     # 価格
