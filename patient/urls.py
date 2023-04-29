from django.urls import path
from .views import PatientComeHistoryCreateView, SearchCardIdView, CreateCardIdView, Home, historyView, \
    QRCodeRegisterView, PatientComeHistoryCardView, OpticCamePatientView, QRCodePartnerView, QRCodeRegisterListView, \
    QRCodePartnerListView, qr_register_code, qr_partner_register_code

app_name = 'patient'

urlpatterns = [
    path('', Home.as_view()),
    path('create-history/', PatientComeHistoryCreateView.as_view(), name='create-history'),
    path('search-patient/', SearchCardIdView.as_view(), name='search-patient'),
    path('create-card-id/', CreateCardIdView.as_view(), name='create-card-id'),
    path('card-id/<str:cardId>', historyView, name='card-id'),
    path('register/<str:cardId>', QRCodeRegisterView.as_view(), name='qr-register'),
    path('come-history/<int:id>', PatientComeHistoryCardView.as_view(), name='qr-come-patient'),
    path('come-history-detail/<int:pk>', OpticCamePatientView.as_view(), name='qr-come-patient-detail'),
    path('partner-register/<int:id>', QRCodePartnerView.as_view(), name='partner-register'),
    path('register-list/', QRCodeRegisterListView.as_view(), name='register-list'),
    path('partner-register-list/', QRCodePartnerListView.as_view(), name='partner-register-list'),
    path('check-code/', qr_register_code, name='code-check'),
    path('check-code-partner/', qr_partner_register_code, name='code-check-partner'),
]
