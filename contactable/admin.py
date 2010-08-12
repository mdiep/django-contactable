
from django.contrib import admin

from contactable.models import *

class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 1

class ContactInfoAdmin(admin.ModelAdmin):
    inlines = [ PhoneNumberInline ]
    exclude = [ 'content_type', 'object_id' ]

admin.site.register(ContactInfo, ContactInfoAdmin)

