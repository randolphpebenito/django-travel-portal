from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class EmployeeAccountPosition(models.Model):
    position_name = models.CharField(max_length=64, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = u"Position"

    def __unicode__(self):
        return self.position_name

class EmployeeAccount(models.Model):
    firstname = models.CharField(max_length=64, blank=True)
    lastname = models.CharField(max_length=64, blank=True)
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    account_position = models.ForeignKey(EmployeeAccountPosition, related_name='position')
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u"Account"

    def __unicode__(self):
        return "%s %s" %(self.firstname, self.lastname)

    
