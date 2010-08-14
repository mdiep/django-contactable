
from django import forms

from contactable.models import *

PhoneNumberFormSet = forms.models.inlineformset_factory(ContactInfo, PhoneNumber, extra=1)

class ContactInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            instance = kwargs['instance']
            if isinstance(instance, Contactable):
                kwargs['instance'] = instance.contact_info
        super(ContactInfoForm, self).__init__(self, *args, **kwargs)
        self.phone_number_formset = PhoneNumberFormSet(*args, **kwargs)
    
    def is_valid(self):
        return super(ContactInfoForm, self).is_valid() \
           and self.phone_number_formset.is_valid()
    
    def save(self):
        info = super(ContactInfoForm, self).save()
        self.phone_number_formset.save()
        return info.contactable
    
    class Meta:
        model   = ContactInfo
        exclude = ['content_type', 'object_id']

