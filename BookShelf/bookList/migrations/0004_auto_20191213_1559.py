# Generated by Django 3.0 on 2019-12-13 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookList', '0003_auto_20191210_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='text',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
