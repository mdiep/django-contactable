
from django.contrib.localflavor.us import models as us
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models

class Contactable(models.Model):
    def delete(self, **kwargs):
        self.contact_info.delete()
        super(Contactable, self).delete(**kwargs)
    
    def save(self, **kwargs):
        super(Contactable, self).save(**kwargs)
        self.contact_info.save()
    
    @property
    def contact_info(self):
        try:
            return ContactInfo.objects.get(contactable=self)
        except ContactInfo.DoesNotExist:
            return ContactInfo(contactable=self)
    
    class Meta:
        abstract = True

class ContactInfoManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'contactable' in kwargs:
            contactable = kwargs['contactable']
            kwargs['content_type'] = ContentType.objects.get_for_model(contactable)
            kwargs['object_id']    = contactable.pk
            del kwargs['contactable']
        return super(ContactInfoManager, self).get(*args, **kwargs)

class ContactInfo(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id    = models.PositiveIntegerField()
    contactable  = generic.GenericForeignKey()

    objects = ContactInfoManager()
    
    class Meta:
        verbose_name_plural = 'contact info'
    
    def __unicode__(self):
        return unicode(self.contactable)

class EmailAddress(models.Model):
    LABEL_CHOICES = (
        ('h', 'home'),
        ('w', 'work'),
        ('o', 'other'),
    )
    
    info    = models.ForeignKey(ContactInfo, related_name='email_addresses')
    label   = models.CharField(max_length=1, choices=LABEL_CHOICES)
    address = models.EmailField()
    
    def __unicode__(self):
        return "%s (%s)" % (self.address, self.get_label_display())
    
    class Meta:
        verbose_name_plural = 'email addresses'

class PhoneNumber(models.Model):
    LABEL_CHOICES = (
        ('m', 'mobile'),
        ('h', 'home'),
        ('w', 'work'),
        ('o', 'other'),
    )
    
    info   = models.ForeignKey(ContactInfo, related_name='phone_numbers')
    label  = models.CharField(max_length=1, choices=LABEL_CHOICES)
    number = us.PhoneNumberField()
    
    def __unicode__(self):
        return "%s (%s)" % (self.number, self.get_label_display())


