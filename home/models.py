__author__ = "shrey"
from django.db import models

class Alert(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

