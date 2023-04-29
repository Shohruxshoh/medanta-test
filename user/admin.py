from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User, Region, District, Clinic


# Register your models here.

class UsersAdmin(UserAdmin):
    list_display = ('phone', 'last_name', 'first_name', 'clinic', 'is_active')
    list_filter = ('role', )


admin.site.register(User)
admin.site.register(Region)
admin.site.register(District)
admin.site.register(Clinic)
