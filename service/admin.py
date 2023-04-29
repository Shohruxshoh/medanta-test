from django.contrib import admin
from .models import Service, Installment, PayInstallmentPeriod, ServicePrice

# Register your models here.

admin.site.register(Service)
admin.site.register(Installment)
admin.site.register(PayInstallmentPeriod)
admin.site.register(ServicePrice)
