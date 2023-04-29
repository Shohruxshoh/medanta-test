from django.urls import path
from lead.views import CustomerListView, CustomerUpdateView, CustomerCreateView, CustomerDeleteView, loadRegion, \
    CustomDetailView, CustomerPayInstallmentListView, HomeView, patientHistoryIsActive
from service.views import loadService

app_name = 'lead'
urlpatterns = [
    # path('', HomeView.as_view(), name='index'),
    path('', CustomerListView.as_view(), name='customers'),
    path('created/', CustomerCreateView.as_view(), name='create'),
    path('update/<int:pk>', CustomerUpdateView.as_view(), name='customer_update'),
    path('ajax-region/', loadRegion, name='region'),
    path('ajax-service/', loadService, name='load-service'),
    path('delete/<int:pk>', CustomerDeleteView.as_view(), name='customer_delete'),
    path('detail/<int:pk>', CustomDetailView.as_view(), name='customer_detail'),
    path('customer-pay', CustomerPayInstallmentListView.as_view(), name='customer-pay'),
    path('patient-active/', patientHistoryIsActive, name='patient-active'),
]
