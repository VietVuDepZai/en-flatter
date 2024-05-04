from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, timedelta, date
# Create your models here.

class Question(models.Model):
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    yes=models.CharField(max_length=200)
    no=models.CharField(max_length=200)
    yes=models.CharField(max_length=200)
    no=models.CharField(max_length=200)
    cat=(('Yes','Yes'),('No','No'))
    answer=models.CharField(max_length=200,choices=cat)
    def __str__(self):
        return self.question 
    
class Result(models.Model):
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
    typeof=models.CharField(max_length=200, null=True, blank=True)

class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, default=None)
    profile_pic= models.ImageField(upload_to='profile_pic/',null=True,blank=True)
    mobile = models.CharField(max_length=20,default=None, null=True)
    status= models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    desc = models.TextField(max_length=500,default=None,blank=True)
    class Meta:
        ordering = ['-created_on']
    @property
    def get_name(self):
        return self.user.username
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.username
    # def save(self, *args, **kwargs):
    #     super(Patient, self).save(*args, **kwargs)
    #<iframe allowtransparency=“true” width=“485” height=“402” src="{{}}embed“ frameborder=”0" allowfullscreen></iframe>

class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,default=None)
    profile_pic= models.ImageField(upload_to='profile_pic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,default=None,blank=False)
    status= models.BooleanField(default=False)
    totalstar = models.IntegerField(default=5)
    timeclick = models.IntegerField(default=1)
    star = models.CharField(max_length=1,default=5)
    desc = models.TextField(max_length=500,default=None,blank=True)
    @property
    def get_name(self):
        return self.user.username
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.username
    # def save(self, *args, **kwargs):
    #     super(Doctor, self).save(*args, **kwargs)
    #
class Room(models.Model):
    name = models.CharField(max_length=1000)
class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)



class Event(models.Model):
    status = models.BooleanField(default=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a class="event" href="{url}"> {self.title} </a>'


