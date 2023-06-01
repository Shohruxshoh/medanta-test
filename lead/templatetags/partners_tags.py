from django import template
from deposit.models import PartnerAndPatient

register = template.Library()


@register.simple_tag()
def get_partner(id):
    if PartnerAndPatient.objects.filter(patient_id=id).exists():
        part = PartnerAndPatient.objects.get(patient_id=id)
        name = part.partner.partner.last_name + " " + part.partner.partner.first_name + " " + part.partner.partner.phone
        return name
    return "Medanta"
