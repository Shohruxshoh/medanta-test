from django.contrib import admin
from device.models import DeviceCategory, DeviceImage

# Register your models here.

admin.site.register(DeviceCategory)
admin.site.register(DeviceImage)
