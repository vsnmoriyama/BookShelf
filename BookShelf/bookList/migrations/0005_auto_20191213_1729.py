# Generated by Django 3.0 on 2019-12-13 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookList', '0004_auto_20191213_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='text',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
