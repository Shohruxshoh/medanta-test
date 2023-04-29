from django.urls import path
from card.views import CreateCardView, DebtsCreateView

app_name = 'card'
urlpatterns = [
    path('create-card/', CreateCardView.as_view(), name='create-card'),
    path('debit-create/', DebtsCreateView.as_view(), name='debit-create'),
]
