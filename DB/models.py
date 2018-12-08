
from django.db import models


# Create your models here.


class Enrollments(models.Model):

    course_id = models.CharField(max_length=15)
    student_id = models.CharField(max_length=15)
    student_name = models.CharField(max_length=15)
    prof_id = models.CharField(max_length=15)
    status = models.CharField(max_length=15)

class csvfile(models.Model):
    req_file = models.FileField(upload_to='media_')


class Marks(models.Model):
    student_name = models.CharField(max_length=15)
    student_id = models.CharField(default=0,max_length=15)
    course_id = models.CharField(default=0,max_length=15)
    prof_id = models.CharField(default=0,max_length=15)
    marks = models.FloatField(default=0)
    q_name = models.CharField(max_length=15)

    class Meta:
        unique_together = ('student_id', 'course_id','prof_id','q_name','student_name')






