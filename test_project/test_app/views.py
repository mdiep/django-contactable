
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic.list_detail import object_detail, object_list

from contactable.forms import ContactInfoForm

from test_app.models import *

def person_detail(request, id):
    return object_detail(request, queryset=Person.objects.all(), object_id=id)

def person_edit(request, id):
    person = get_object_or_404(Person, id=id)
    if request.method == 'POST':
        form = ContactInfoForm(request.POST, instance=person)
        if form.is_valid():
            person = form.save()
            return HttpResponseRedirect(person.get_absolute_url())
    else:
        form = ContactInfoForm(instance=person)
    return render_to_response('test_app/person_edit.html', locals(),
                              context_instance=RequestContext(request))

def person_list(request):
    return object_list(request, queryset=Person.objects.all())

