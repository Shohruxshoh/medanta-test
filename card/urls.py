from django.urls import path
from card.views import CreateCardView, DebtsCreateView, PostCreate, PostList, Post1List

app_name = 'card'
urlpatterns = [
    path('create-card/', CreateCardView.as_view(), name='create-card'),
    path('debit-create/', DebtsCreateView.as_view(), name='debit-create'),
    path('post-create/', PostCreate.as_view(), name='post-create'),
    path('post-list/', Post1List.as_view(), name='post-list'),
    path('post-list1/', PostList.as_view(), name='post-list1'),
]
