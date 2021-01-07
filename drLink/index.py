from django import template
register = template.Library()

@register.filter
def index(lastAppointment, i):
    return lastAppointment[i]
