# Generated by Django 4.2.5 on 2023-09-29 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default='2023-09-29 22:23:47.766147'),
        ),
    ]
