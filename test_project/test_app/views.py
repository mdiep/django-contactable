
from django.views.generic.list_detail import object_detail, object_list

from test_app.models import *

def person_detail(request, id):
    return object_detail(request, queryset=Person.objects.all(), object_id=id)

def person_list(request):
    return object_list(request, queryset=Person.objects.all())

