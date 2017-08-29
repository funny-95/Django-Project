from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class MyUser(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(max_length=200)
    gonghao = models.CharField(max_length=200,unique=True)
    depth = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    permission = models.IntegerField(default=1)

    def __unicode__(self):
        return self.user.username

class File(models.Model):
    title=models.TextField()
    details=models.TextField()
    public_time=models.DateField()

class Qiandao(models.Model):
    username = models.CharField(max_length=200)
    gonghao = models.CharField(max_length=200,unique=True)
    date = models.DateField()
    first_qiandao = models.CharField(max_length=200)
    second_qiandao = models.CharField(max_length=200)

class Qingjia(models.Model):
    gonghao = models.CharField(max_length=200,unique=True)
    from_date = models.CharField(max_length=200)
    to_date = models.CharField(max_length=200)
    now_date = models.CharField(max_length=200,default=date.today())
    cause = models.CharField(max_length=200)
    approve_result = models.CharField(max_length=200)
    refuse_reason = models.CharField(max_length=200)
    approve_person = models.CharField(max_length=200)

class Salary(models.Model):
    gonghao = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    depth = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    base_salary = models.CharField(max_length=200)
    ti_cheng = models.CharField(max_length=200)
    jiaban = models.CharField(max_length=200,default=0)
    queqing = models.CharField(max_length=200,default=0)
    tiaoxiu = models.CharField(max_length=200,default=0)
    qingjia = models.CharField(max_length=200,default=0)
    jiaban_hour = models.CharField(max_length=200, default=0)
    queqing_hour = models.CharField(max_length=200, default=0)
    tiaoxiu_hour = models.CharField(max_length=200, default=0)
    qingjia_hour = models.CharField(max_length=200, default=0)
    jiangjin = models.CharField(max_length=200)
    total_salary = models.CharField(max_length=200)
    mouth_time = models.CharField(max_length=200,default=0)

class Base_salary(models.Model):
    depth = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    base_salary = models.CharField(max_length=200)
    jiaban = models.CharField(max_length=200, default=0)
    queqing = models.CharField(max_length=200, default=0)
    qingjia = models.CharField(max_length=200, default=0)