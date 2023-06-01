from django.urls import path
from drug.views import DrugListView, DrugCreateView, DrugUpdateView, DrugDeleteView, PharmacyView, OperationsView, \
    PharmacyListView, PharmacyDetailView, OperationDetailView, OperationListView

app_name = 'drug'

urlpatterns = [
    path('', DrugListView.as_view(), name='drugs'),
    path('drug-create/', DrugCreateView.as_view(), name='drug-create'),
    path('pharmacy-list', PharmacyListView.as_view(), name='pharmacy-list'),
    path('operation-list', OperationListView.as_view(), name='operation-list'),
    path('pharmacy-detail/<int:pk>', PharmacyDetailView.as_view(), name='pharmacy-detail'),
    path('operation-detail/<int:pk>', OperationDetailView.as_view(), name='operation-detail'),
    path('pharmacy-create/<int:pk>', PharmacyView.as_view(), name='pharmacy-create'),
    path('operation-create/<int:id>', OperationsView.as_view(), name='operation-create'),
    path('drug-update/<int:pk>', DrugUpdateView.as_view(), name='drug-update'),
    path('drug-delete/<int:pk>', DrugDeleteView.as_view(), name='drug-delete'),
]
