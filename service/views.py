from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from service.forms import ServiceForm, InstallmentForm, PayInstalmentCombineForm
from service.models import Service, Installment, PayInstallmentPeriod, ServicePrice
from user.models import User, ADMINISTRATOR, DOCTOR, RECEPTION, DIRECTOR
from medanta.mixins import AllowedRolesMixin


# Create your views here.


class ServiceListView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DIRECTOR]
    model = Service
    template_name = 'reception/director/service/services.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Service.objects.filter(user=self.request.user)
        return queryset


class ServicePriceCreateView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [ADMINISTRATOR, DIRECTOR]
    model = ServicePrice
    template_name = 'reception/director/service/create_service_price.html'
    fields = ['price', 'is_active']
    success_url = '/service/services-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.clinic = self.request.user.clinic
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ServiceCreateView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [ADMINISTRATOR, DIRECTOR]
    model = Service
    form_class = ServiceForm
    template_name = 'reception/director/service/create_service.html'
    success_url = '/service/services-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        ctx = super(ServiceCreateView, self).get_context_data(**kwargs)
        ctx['prices'] = ServicePrice.objects.filter(clinic_id=self.request.user.clinic, is_active=True)
        return ctx


class ServiceUpdateView(AllowedRolesMixin, LoginRequiredMixin, UpdateView):
    allowed_roles = [ADMINISTRATOR, DIRECTOR]
    model = Service
    form_class = ServiceForm
    template_name = 'reception/director/service/update_service.html'
    success_url = '/service/services-list'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        price = ServicePrice.objects.filter(id=self.object.service_price.id)
        if request.POST.get('is_active') is not None:
            price.update(is_active=True)
        else:
            price.update(is_active=False)
        return redirect("service:services-list")

    def get_context_data(self, **kwargs):
        ctx = super(ServiceUpdateView, self).get_context_data(**kwargs)
        ctx['prices'] = ServicePrice.objects.filter(clinic_id=self.object.user.clinic, is_active=True)
        return ctx


class ServiceDeleteView(AllowedRolesMixin, LoginRequiredMixin, DeleteView):
    allowed_roles = [ADMINISTRATOR, DIRECTOR]
    model = Service
    template_name = 'reception/director/service/service-delete.html'
    success_url = '/service/services-list'


class InstallmentListView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DIRECTOR]
    model = Installment
    template_name = 'reception/director/installment/installmentes.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Installment.objects.all()
        return queryset


class InstallmentCreateView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [ADMINISTRATOR, DIRECTOR]
    model = Installment
    form_class = InstallmentForm
    template_name = 'reception/director/installment/create_installment.html'
    success_url = '/service/installmentes-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.month_pay = ((self.object.service.price - self.object.service.cost) * (
                1 + (self.object.percent / 100))) / self.object.month
        self.object.total_pay = ((self.object.service.price - self.object.service.cost) * (
                1 + (self.object.percent / 100)))
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class InstallmentUpdateView(AllowedRolesMixin, LoginRequiredMixin, UpdateView):
    allowed_roles = [ADMINISTRATOR, DIRECTOR]
    model = Installment
    form_class = InstallmentForm
    template_name = 'reception/director/installment/update_installment.html'
    success_url = '/service/installmentes-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.month_pay = ((self.object.service.price - self.object.service.cost) * (
                1 + (self.object.percent / 100))) / self.object.month
        self.object.total_pay = ((self.object.service.price - self.object.service.cost) * (
                1 + (self.object.percent / 100)))
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class InstallmentDeleteView(AllowedRolesMixin, LoginRequiredMixin, DeleteView):
    allowed_roles = [ADMINISTRATOR, DIRECTOR]
    model = Installment
    template_name = 'reception/director/installment/installment-delete.html'
    success_url = '/service/installmentes-list'


class InstallmentPaymentView(AllowedRolesMixin, LoginRequiredMixin, View):
    allowed_roles = [ADMINISTRATOR, DIRECTOR, RECEPTION]

    def get(self, request, *args, **kwargs):
        form = PayInstalmentCombineForm()
        context = {'form': form}
        return render(request, 'lead/instalment.html', context)

    def post(self, request, *args, **kwargs):
        form = PayInstalmentCombineForm(request.POST)
        if form.is_valid():
            service = Service.objects.get(pk=request.POST.get('service'))
            user = User.objects.get(pk=request.POST.get("user"))
            installment = Installment.objects.get(pk=request.POST.get("installment"))
            user.is_installment = True
            user.save()
            for l in range(0, installment.month):
                date_after_month = datetime.today() + relativedelta(months=l + 1)
                a = PayInstallmentPeriod.objects.create(installment_id=installment.pk, user_id=user.pk,
                                                        service_id=service.pk,
                                                        start_date=date_after_month,
                                                        sum=installment.month_pay)
            messages.success(request, "Success")
            return redirect('lead:customer_detail', pk=user.pk)
        else:
            form = PayInstalmentCombineForm()
        context = {'form': form}
        return render(request, 'lead/instalment.html', context)


def loadService(request):
    service_id = request.GET.get('service_id')
    installment = Installment.objects.filter(service_id=service_id)
    return JsonResponse(list(installment.values('id', 'month', 'percent')), safe=False)
