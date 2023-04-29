from django import template

register = template.Library()


@register.simple_tag()
def startswith(text):
    text = str(text)
    return text[0:4] + '****' + text[12:16]


@register.simple_tag()
def month_and_year(month, year):
    month = str(month)
    year = str(year)
    return month + "/" + year[2:]

