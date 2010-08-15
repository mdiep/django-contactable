
from django import forms
from django.template.loader import render_to_string

from contactable.models import *

EmailAddressFormSet = forms.models.inlineformset_factory(ContactInfo, EmailAddress, extra=1)
PhoneNumberFormSet  = forms.models.inlineformset_factory(ContactInfo, PhoneNumber, extra=1)
AddressFormSet      = forms.models.inlineformset_factory(ContactInfo, Address, extra=1)

class ContactInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            instance = kwargs['instance']
            if isinstance(instance, Contactable):
                kwargs['instance'] = instance.contact_info
        super(ContactInfoForm, self).__init__(self, *args, **kwargs)
        self.email_address_formset = EmailAddressFormSet(*args, **kwargs)
        self.phone_number_formset  = PhoneNumberFormSet(*args, **kwargs)
        self.address_formset       = AddressFormSet(*args, **kwargs)
    
    def __unicode__(self):
        return render_to_string('contactable/contact_info_form.html', {'form': self})
    
    def is_valid(self):
        return super(ContactInfoForm, self).is_valid() \
           and self.email_address_formset.is_valid() \
           and self.phone_number_formset.is_valid() \
           and self.address_formset.is_valid()
    
    def save(self):
        info = super(ContactInfoForm, self).save()
        self.email_address_formset.save()
        self.phone_number_formset.save()
        self.address_formset.save()
        return info.contactable
    
    class Meta:
        model   = ContactInfo
        exclude = ['content_type', 'object_id']

