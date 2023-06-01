from django.urls import path
from accountant.views import ServiceListView

app_name = 'accountant'

urlpatterns = [
    path("", ServiceListView.as_view(), name='accountant-list'),
]
