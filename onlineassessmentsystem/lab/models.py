from django.db import models
from classroom.models import Classroom


# Create your models here.

class Lab(models.Model):
    labId = models.AutoField(primary_key=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    title = models.CharField(max_length=10, default="Default lab title")
    subject = models.CharField(null=False, max_length=50, default="DEFAULT-SUBJECT")
    description = models.CharField(null=False, max_length=1000, default="Default Lab description")
    deadline = models.DateTimeField()
