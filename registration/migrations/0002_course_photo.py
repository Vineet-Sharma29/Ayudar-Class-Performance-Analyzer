# Generated by Django 2.1.3 on 2018-12-08 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='photo',
            field=models.ImageField(default='media_/photos/course.jfif', upload_to='media_/photos'),
        ),
    ]
