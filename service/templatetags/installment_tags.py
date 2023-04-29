from django import template
from datetime import datetime
from dateutil.relativedelta import relativedelta
from service.models import Debts

register = template.Library()


@register.simple_tag()
def get_sum(value):
    absaaa = datetime.today() + relativedelta(months=value)
    return absaaa

