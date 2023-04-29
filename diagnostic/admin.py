from django.contrib import admin

from diagnostic.models import *

# Register your models here.

admin.site.register(Visus)
admin.site.register(Params0To20)
admin.site.register(Complaint)

admin.site.register(OphthalmologyStatus)
