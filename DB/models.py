
from django.db import models


# Create your models here.


class Enrollments(models.Model):
    student_id = models.IntegerField(primary_key=True)
    course_id = models.CharField(null=False,max_length=15)
    status = models.CharField(max_length=15)

class csvfile(models.Model):
    req_file = models.FileField(upload_to='documents')


class Marks(models.Model):
    student_id = models.IntegerField(default=0)
    course_id = models.CharField(default=0,max_length=15)
    prof_id = models.IntegerField(default=0)
    marks = models.FloatField(default=0)
    q_name = models.CharField(max_length=15)

    class Meta:
        unique_together = ('student_id', 'course_id','prof_id','q_name')




"""class Marks(models.Model):
    student_id = models.ForeignKey(Enrollments,on_delete=models.PROTECT)
    course_id = models.ForeignKey(Enrollments, on_delete=models.PROTECT)
    marks = models.FloatField(null=False)
    q_name = models.CharField(max_length=15)"""


