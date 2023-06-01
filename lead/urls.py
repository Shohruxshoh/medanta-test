from django.urls import path
from lead.views import CustomerListView, CustomerUpdateView, CustomerCreateView, CustomerDeleteView, loadRegion, \
    CustomDetailView, CustomerPayInstallmentListView, HomeView,  LeadUpdateView, check_user_phone
from service.views import loadService

app_name = 'lead'
urlpatterns = [
    # path('', HomeView.as_view(), name='index'),
    path('check/', check_user_phone, name='check-phone'),
    path('', CustomerListView.as_view(), name='customers'),
    path('created/', CustomerCreateView.as_view(), name='create'),
    path('update/<int:pk>', CustomerUpdateView.as_view(), name='customer_update'),
    path('lead-update/<int:pk>', LeadUpdateView.as_view(), name='lead_update'),
    path('ajax-region/', loadRegion, name='region'),
    path('ajax-service/', loadService, name='load-service'),
    path('delete/<int:pk>', CustomerDeleteView.as_view(), name='customer_delete'),
    path('detail/<int:pk>', CustomDetailView.as_view(), name='customer_detail'),
    path('customer-pay', CustomerPayInstallmentListView.as_view(), name='customer-pay'),
]
