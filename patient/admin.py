from django.contrib import admin
from patient.models import PatientComeHistory, CardToUser, QRCodeRegister, QRCodePartner, PhoneCode

# Register your models here.

admin.site.register(PatientComeHistory)
admin.site.register(CardToUser)
admin.site.register(QRCodeRegister)
admin.site.register(QRCodePartner)
admin.site.register(PhoneCode)
# @admin.register(PatientComeHistory)
# class PatientComeHistoryAdmin(admin.ModelAdmin):
#     list_display = ['id' 'patient']
