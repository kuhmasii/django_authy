# Generated by Django 3.1.3 on 2021-06-06 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20210606_0342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictionary',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]
