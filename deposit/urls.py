from django.urls import path
from deposit.views import CreateDepositView, DepositListView, CreatePartnerView, PartnersListView, PartnerUpdateView, \
    PartnerDeleteView, \
    PartnerCreateCardView, PartnerDetailView, depositDelete, PartnerAndPatientView

app_name = 'deposit'
urlpatterns = [
    path('create-deposit/', CreateDepositView.as_view(), name='create-deposit'),
    path('deposits-list/', DepositListView.as_view(), name='deposits-list'),
    path('patient-list/', PartnerAndPatientView.as_view(), name='patient-list'),
    path('deposit-delete/<int:pk>', depositDelete, name='deposit-delete'),
    path('create-partnet/', CreatePartnerView.as_view(), name='create-partnet'),
    path('partnet-list/', PartnersListView.as_view(), name='partnet-list'),
    path('partnet-detail/<int:pk>', PartnerDetailView.as_view(), name='partnet-detail'),
    path('partnet-update/<int:pk>', PartnerUpdateView.as_view(), name='partnet-update'),
    path('partnet-delete/<int:pk>', PartnerDeleteView.as_view(), name='partnet-delete'),
    path('create-partner-card/', PartnerCreateCardView.as_view(), name='create-partner-card'),
]
