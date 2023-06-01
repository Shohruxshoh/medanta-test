from django.contrib import admin
from drug.models import Drugs, Pharmacy, Operations
# Register your models here.

admin.site.register(Drugs)
admin.site.register(Pharmacy)
admin.site.register(Operations)
