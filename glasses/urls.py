from django.urls import path
from glasses.views import GlassesListView, GlassCreateView, GlassGiveView, GlassesListNowView

app_name = "glasses"

urlpatterns = [
    path('glasses-list/', GlassesListView.as_view(), name="glasses-list"),
    path('glasses-list-now/', GlassesListNowView.as_view(), name="glasses-list-now"),
    path('glasses-create/<int:pk>', GlassCreateView.as_view(), name="glasses-create"),
    path('glasses-detail/<int:pk>', GlassGiveView.as_view(), name="glasses-detail"),
]
