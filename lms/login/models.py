from django.db import models
from django.contrib.auth.models import User



class course(models.Model):
    course_id = models.CharField(max_length=15,unique=True)
    course_name = models.CharField(max_length=30,unique=True)
    credits = models.IntegerField()


class professor_profile(models.Model):
    professor = models.OneToOneField(User,on_delete=models.CASCADE)
    professor_description = models.CharField(max_length=150)
    professor_photo = models.ImageField(upload_to='media_/photos')
    course = models.ManyToManyField(course)


# Create your models here.d
