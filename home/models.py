__author__ = "shrey"
from django.db import models

class Tab(models.Model):
    name = models.CharField(max_length=20)
    link = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Alert(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

