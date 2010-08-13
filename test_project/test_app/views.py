
from django.views.generic.list_detail import object_list

from test_app.models import *

def person_list(request):
    return object_list(request, queryset=Person.objects.all())

