from django.contrib import admin
from .models import CardUser, Post, Post1
from service.models import Debts
# Register your models here.

admin.site.register(CardUser)
admin.site.register(Debts)
admin.site.register(Post1)
admin.site.register(Post)
