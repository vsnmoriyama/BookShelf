from django.db import models


class User(models.Model):                             # Userテーブル
    user_id = models.CharField(max_length=200)          # id
    user_name = models.CharField(max_length=200)        # ユーザ名
