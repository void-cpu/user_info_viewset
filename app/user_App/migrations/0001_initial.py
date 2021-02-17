# Generated by Django 3.1.6 on 2021-02-17 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='最后修改时间', verbose_name='最后修改时间')),
                ('UserName', models.CharField(max_length=20, verbose_name='用户名')),
                ('TrueName', models.CharField(max_length=20, verbose_name='用户的真实姓名')),
                ('NameCards', models.CharField(max_length=30, verbose_name='用户的身份证号')),
                ('UserPwd', models.CharField(max_length=30, verbose_name='用户密码')),
                ('phone', models.CharField(max_length=20, unique=True, verbose_name='用户的手机号密码')),
                ('address', models.CharField(max_length=100, verbose_name='用户地址')),
                ('CapitalPwd', models.CharField(max_length=20, verbose_name='资金密码')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=30, verbose_name='用户余额')),
                ('BlankCard', models.CharField(blank=True, max_length=20, null=True, verbose_name='银行卡')),
                ('AnotherId', models.CharField(blank=True, max_length=30, null=True, verbose_name='另一个app_id')),
            ],
            options={
                'verbose_name': '用户管理',
                'verbose_name_plural': '用户管理',
                'db_table': 'uneatable',
            },
        ),
    ]