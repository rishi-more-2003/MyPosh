from django.db import models
from posh.models import PoshUser, EstablishmentUser
from django.conf import settings
import datetime

class Groups(models.Model):
    group_name = models.CharField(max_length=100)
    section = models.CharField(max_length=100,default='Third Year')
    group_code = models.CharField(max_length = 10,default='0000000')

    def __str__(self):
        return self.group_name

class Employee(models.Model):
    employee_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE)

class Enterprise(models.Model):
    enterprise_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE)

class Notice(models.Model):
    notice_name = models.CharField(max_length=50)
    group_id = models.ForeignKey(Groups,on_delete=models.CASCADE)
    due_date = models.DateField()
    due_time = models.TimeField(default=datetime.time(10,10))
    posted_date = models.DateField(auto_now_add=True)
    instructions = models.TextField()

    def __str__(self):
        return self.notice_name

class Submissions(models.Model):
    notice_id = models.ForeignKey(Notice,on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    submitted_date=models.DateField(auto_now_add=True)
    submitted_time=models.TimeField(auto_now_add=True)
    submitted_on_time = models.BooleanField(default=True)
    submission_file = models.FileField(upload_to='documents/')
