
from django.contrib import admin

from test_app.models import *

class PersonAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']

admin.site.register(Person, PersonAdmin)

