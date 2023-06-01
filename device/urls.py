from django.urls import path
from device.views import DeviceImageAddView

app_name = "device"
urlpatterns = [
    path("add/<int:pk>", DeviceImageAddView.as_view(), name="add-image"),
]
