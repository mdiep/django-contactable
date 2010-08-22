
# What is django-contactable?

django-contactable is a reusable Django application for storing contact information. It provides building blocks for larger, CRM applications.

# Synopsis

Model:

    from django.db import models
    
    from contactable.models import Contactable
    
    class Person(Contactable):
        name = models.CharField(max_length=50)

Views:

    from django.http import HttpResponseRedirect
    from django.shortcuts import render_to_response, get_object_or_404
    
    from contactable.forms import ContactInfoForm
    
    def person_detail(request, id):
        person = get_object_or_404(Person, id=id)
        return render_to_response('detail template', locals())
    
    def person_edit(request, id):
        person = get_object_or_404(Person, id=id)
        if request.method == 'POST':
            form = ContactInfoForm(request.POST, instance=person)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(person.get_absolute_url())
        else:
            form = ContactInfoForm(instance=person)
        return render_to_response('edit template', locals())

Detail Template:

    {% load contactable %}
    
    {% contact_info person %}

Edit Template:

    {{ form }}


