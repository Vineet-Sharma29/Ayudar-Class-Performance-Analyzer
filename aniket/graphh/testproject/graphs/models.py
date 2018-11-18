from django.db import models

class Student(models.Model):
	rollno = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=50)
	def __str__(self):
		return self.name

class Quiz(models.Model):
	name = models.CharField(max_length=20)
	prof = models.CharField(max_length=40)
	def __str__(self):
		return self.name

class QuizResult(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete='CASCADE')
	student = models.ForeignKey(Student, on_delete='CASCADE')
	marks = models.IntegerField()
	classaverage = models.FloatField(null=True, blank=True)
	def __str__(self):
		return str(self.quiz.name+'-marks-for-'+self.student.name)
	def save(self, *args, **kwargs):
		avg = 0
		objs = QuizResult.objects.all()
		for obj in objs:
			avg = avg + obj.marks
		avg = avg + self.marks
		avg = avg/(len(objs)+1)
		print(avg)
		self.classaverage = avg
		super(QuizResult, self).save(*args, **kwargs)
