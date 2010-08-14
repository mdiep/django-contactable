
from django import template

register = template.Library()

@register.inclusion_tag('contactable/contact_info.html')
def contact_info(contactable):
    contact_info = contactable.contact_info
    return {'contactable':   contactable,
            'phone_numbers': contact_info.phone_numbers.all()}

