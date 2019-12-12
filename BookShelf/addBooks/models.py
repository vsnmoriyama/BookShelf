from django.db import models


class BookStatus(models.Model):                             # bookStatusテーブル

    isbn = models.CharField(max_length=200)         # isbn
    user_id = models.CharField(max_length=200)      # ユーザID
    status = models.CharField(max_length=200)       # status

    class Meta:
        unique_together = ('isbn', 'user_id')


class BookReview(models.Model):                             # bookStatusテーブル

    isbn = models.CharField(max_length=200)         # isbn
    user_id = models.CharField(max_length=200)      # ユーザID
    star = models.CharField(max_length=200)         # star
    review = models.CharField(max_length=200)       # レビュー

    class Meta:
        unique_together = ('isbn', 'user_id')