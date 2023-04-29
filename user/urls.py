from django.urls import path
from django.views.generic import TemplateView

from user.views import user_signup, user_logout, handler404, CreateEmployeeView, EmployeesListView, EmployeeUpdateView, \
    EmployeeDeleteView

app_name = 'user'

urlpatterns = [
    path('create-employee/', CreateEmployeeView.as_view(), name='create-employee'),
    path('employee-list/', EmployeesListView.as_view(), name='employee-list'),
    path('employee-update/<int:pk>', EmployeeUpdateView.as_view(), name='employee-update'),
    path('employee-delete/<int:pk>', EmployeeDeleteView.as_view(), name='employee-delete'),
    path('signup/', user_signup, name='signup'),
    path('login/', TemplateView.as_view(template_name='account/login.html'),
         name='login_view'),
    path('logout/', user_logout, name='logout'),
    path('handler404/', handler404, name='handler404'),
]
