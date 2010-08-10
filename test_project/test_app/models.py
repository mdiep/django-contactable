
from django.db import models
from contactable.models import Contactable

class Person(Contactable):
    first_name = models.CharField(max_length=20, blank=True)
    last_name  = models.CharField(max_length=20, blank=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name_plural = 'people'
    
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name


