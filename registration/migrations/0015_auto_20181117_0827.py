# Generated by Django 2.1.3 on 2018-11-17 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0014_auto_20181117_0617'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professor_profile',
            name='professor_course',
        ),
        migrations.AddField(
            model_name='professor_profile',
            name='professor_course',
            field=models.CharField(default='DSAA', max_length=100),
            preserve_default=False,
        ),
    ]
