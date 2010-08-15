
from django import template

register = template.Library()

@register.inclusion_tag('contactable/contact_info.html')
def contact_info(contactable):
    contact_info = contactable.contact_info
    return {'contactable':     contactable,
            'email_addresses': contact_info.email_addresses.all(),
            'phone_numbers':   contact_info.phone_numbers.all(),
            'addresses':       contact_info.addresses.all()}

