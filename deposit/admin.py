from django.contrib import admin
from deposit.models import Partner, Deposit, PartnerAndPatient

# Register your models here.
admin.site.register(PartnerAndPatient)
admin.site.register(Deposit)
admin.site.register(Partner)
