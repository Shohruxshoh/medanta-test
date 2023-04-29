from django.urls import path
from .views import ServiceListView, ServiceCreateView, ServiceUpdateView, ServiceDeleteView, InstallmentListView, \
    InstallmentCreateView, InstallmentUpdateView, InstallmentDeleteView, InstallmentPaymentView, ServicePriceCreateView

app_name = 'service'

urlpatterns = [
    path('service-price-create', ServicePriceCreateView.as_view(), name='service-price-create'),
    path('services-list/', ServiceListView.as_view(), name='services-list'),
    path('service-create/', ServiceCreateView.as_view(), name='service-create'),
    path('service-update/<int:pk>', ServiceUpdateView.as_view(), name='service-update'),
    path('service-delete/<int:pk>', ServiceDeleteView.as_view(), name='service-delete'),
    path('installmentes-list/', InstallmentListView.as_view(), name='installment-list'),
    path('installmentes-create/', InstallmentCreateView.as_view(), name='installment-create'),
    path('installmentes-update/<int:pk>', InstallmentUpdateView.as_view(), name='installment-update'),
    path('installmentes-delete/<int:pk>', InstallmentDeleteView.as_view(), name='installment-delete'),
    path('instalment-user/', InstallmentPaymentView.as_view(), name='instalment-user'),
]
