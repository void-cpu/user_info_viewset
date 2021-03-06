# Generated by Django 3.1.6 on 2021-02-17 16:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user_App', '0002_auto_20210217_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodels',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='创建时间', verbose_name='创建时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usermodels',
            name='update_time',
            field=models.DateTimeField(auto_now=True, help_text='最后修改时间', verbose_name='最后修改时间'),
        ),
    ]
