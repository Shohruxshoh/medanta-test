from django.contrib import admin
from .models import CardUser
from service.models import Debts
# Register your models here.

admin.site.register(CardUser)
admin.site.register(Debts)
