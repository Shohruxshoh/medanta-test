from django.urls import path
from drug.views import DrugListView, DrugCreateView, DrugUpdateView, DrugDeleteView

app_name = 'drug'

urlpatterns = [
    path('', DrugListView.as_view(), name='drugs'),
    path('drug-create/', DrugCreateView.as_view(), name='drug-create'),
    path('drug-update/<int:pk>', DrugUpdateView.as_view(), name='drug-update'),
    path('drug-delete/<int:pk>', DrugDeleteView.as_view(), name='drug-delete'),
]
