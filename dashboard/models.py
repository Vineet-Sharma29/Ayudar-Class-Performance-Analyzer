
from django.db import models
from django.contrib.auth.models import User

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




class course_dashboard(models.Model):
    professor = models.OneToOneField(User,on_delete=models.CASCADE)
    course_difficulty = models.CharField(max_length=15,default='-')
    course_risk = models.CharField(max_length=15,default='-')
    course_average = models.FloatField(default=0)
    exam_difficulty = models.CharField(max_length=15,default='-')
    exam_cheat_risk = models.CharField(max_length=15,default='-')
    exam_average = models.FloatField(default=0)
    quartile_1 = models.FloatField(default=0)
    quartile_2 = models.FloatField(default=0)
    quartile_3 = models.FloatField(default=0)
    course_student_list = models.CharField(max_length=150,default='-')
    exam_student_list = models.CharField(max_length=150,default='-')
    needy_student_list = models.CharField(max_length=150,default='-')