# Generated by Django 2.1.8 on 2020-01-08 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20200108_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='reply_time',
            field=models.DateTimeField(null=True, verbose_name='商家回复时间'),
        ),
    ]
