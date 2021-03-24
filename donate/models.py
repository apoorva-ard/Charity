from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Cause(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    date_needed = models.DateTimeField()
    target = models.BigIntegerField()
    collected = models.BigIntegerField(default=0)
    recepient = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.TextField()
    message = models.TextField()
    unread = models.BooleanField(default=True)
        
class Donor(models.Model):
    name = models.CharField(max_length=200)
    comments = models.TextField(null=True)
    dob = models.DateTimeField(null=True)
    amount = models.BigIntegerField()
    accountno = models.BigIntegerField()
