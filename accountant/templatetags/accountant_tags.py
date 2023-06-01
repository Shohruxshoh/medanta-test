from django import template
from lead.models import Lead

register = template.Library()


@register.simple_tag()
def get_sum(id, first_date, last_date):
    sum = 0
    if first_date is None or last_date is None or first_date == '' or last_date == '':
        service = Lead.objects.filter(service_id=id, paid=True)
        for i in service:
            sum = sum + i.lead_price
        return sum
    service = Lead.objects.filter(service_id=id, paid=True, created_at__range=[first_date, last_date])
    for i in service:
        sum = sum + i.lead_price
    return sum


@register.simple_tag()
def get_count(id, first_date, last_date):
    if first_date is None or last_date is None or first_date == '' or last_date == '':
        count = Lead.objects.filter(service_id=id, paid=True).count()
        return count
    count = Lead.objects.filter(service_id=id, paid=True, created_at__range=[first_date, last_date]).count()
    return count
