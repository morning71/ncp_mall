# Generated by Django 2.1.8 on 2019-12-06 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='image',
            field=models.ImageField(default='media/manager/image/default_picture.jpg', upload_to='media/manager/image'),
        ),
    ]
