from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from medanta.mixins import AllowedRolesMixin
from service.models import Service
from user.models import ADMINISTRATOR, DIRECTOR, ACCOUNTANT


# Create your views here.

class ServiceListView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DIRECTOR, ACCOUNTANT]
    model = Service
    template_name = 'accountant/accountant_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ServiceListView, self).get_context_data(**kwargs)
        context["first_date"] = self.request.GET.get('first_date')
        context["last_date"] = self.request.GET.get('last_date')
        return context
