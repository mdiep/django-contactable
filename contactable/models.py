
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
        if not hasattr(self, '_contact_info'):
            try:
                self._contact_info = ContactInfo.objects.get(contactable=self)
            except ContactInfo.DoesNotExist:
                self._contact_info = ContactInfo(contactable=self)
        return self._contact_info
    
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
    
    default_email_address   = models.OneToOneField('EmailAddress', blank=True, null=True)
    default_phone_number    = models.OneToOneField('PhoneNumber',  blank=True, null=True)
    default_address         = models.OneToOneField('Address',      blank=True, null=True)
    
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
        return self.address
    
    def delete(self):
        # If this is the default, change to a different default or nullify the default
        # before deleting. Otherwise, the ContactInfo will be deleted as well. This
        # can't be done with the pre_delete signal because that's too late.
        info = self.info
        if info.default_email_address == self:
            try:
                info.default_email_address = info.email_addresses.exclude(pk=self.pk)[0]
            except IndexError:
                info.default_email_address = None
            info.save()
        super(EmailAddress, self).delete()
    
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
        return self.number
    
    def delete(self):
        # If this is the default, change to a different default or nullify the default
        # before deleting. Otherwise, the ContactInfo will be deleted as well. This
        # can't be done with the pre_delete signal because that's too late.
        info = self.info
        if info.default_phone_number == self:
            try:
                info.default_phone_number = info.phone_numbers.exclude(pk=self.pk)[0]
            except IndexError:
                info.default_phone_number = None
            info.save()
        super(PhoneNumber, self).delete()

class Address(models.Model):
    LABEL_CHOICES = (
        ('h', 'home'),
        ('w', 'work'),
        ('o', 'other'),
    )
    
    info    = models.ForeignKey(ContactInfo, related_name='addresses')
    label   = models.CharField(max_length=1, choices=LABEL_CHOICES)
    street  = models.CharField(max_length=50, blank=True)
    street2 = models.CharField(max_length=50, blank=True)
    city    = models.CharField(max_length=50, blank=True)
    state   = us.USStateField(blank=True, null=True, default='AL')
    zip     = models.CharField(max_length=5, blank=True)
    
    def __unicode__(self):
        if self.street2:
            return "%s, %s, %s, %s, %s" % (self.street, self.street2, self.city, self.state, self.zip)
        else:
            return "%s, %s, %s, %s" % (self.street, self.city, self.state, self.zip)
    
    def delete(self):
        # If this is the default, change to a different default or nullify the default
        # before deleting. Otherwise, the ContactInfo will be deleted as well. This
        # can't be done with the pre_delete signal because that's too late.
        info = self.info
        if info.default_address == self:
            try:
                info.default_address = info.addresses.exclude(pk=self.pk)[0]
            except IndexError:
                info.default_address = None
            info.save()
        super(Address, self).delete()
    
    class Meta:
        verbose_name_plural = 'addresses'

