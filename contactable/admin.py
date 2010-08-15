
from django.contrib import admin

from contactable.models import *

class EmailAddressInline(admin.TabularInline):
    model = EmailAddress
    extra = 1

class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 1

class AddressInline(admin.TabularInline):
    model = Address
    extra = 1

class ContactInfoAdmin(admin.ModelAdmin):
    inlines = [ EmailAddressInline, PhoneNumberInline, AddressInline ]
    exclude = [ 'content_type', 'object_id' ]

admin.site.register(ContactInfo, ContactInfoAdmin)

