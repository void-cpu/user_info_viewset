# Generated by Django 3.1.6 on 2021-02-17 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_App', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermodels',
            name='create_time',
        ),
        migrations.RemoveField(
            model_name='usermodels',
            name='update_time',
        ),
    ]