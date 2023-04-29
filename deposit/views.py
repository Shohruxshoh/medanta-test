from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from deposit.models import Deposit, Partner
from user.forms import SignUpForm, EmployeeUpdateForm
from user.models import User, PARTNER
from django.contrib.auth.mixins import PermissionRequiredMixin


# Create your views here.


class CreateDepositView(LoginRequiredMixin, CreateView):
    model = Deposit
    template_name = 'deposit/create_deposit.html'
    fields = ['user', 'installment', 'bhm_sum']
    success_url = '/deposit/deposits-list'


class DepositListView(LoginRequiredMixin, ListView):
    model = Deposit
    template_name = 'deposit/deposits.html'
    paginate_by = 50


class CreatePartnerView(LoginRequiredMixin, CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'partner/create_partner.html'
    success_url = '/deposit/partnet-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.clinic = self.request.user.clinic
        self.object.phone = str(self.object.phone).replace(" ", "")
        self.object.username = str(self.object.first_name) + str(self.object.phone)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PartnersListView(LoginRequiredMixin, ListView):
    template_name = 'partner/partneres.html'
    model = User
    paginate_by = 50

    def get_queryset(self):
        queryset = User.objects.filter(clinic=self.request.user.clinic, role=PARTNER)
        return queryset


class PartnerUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EmployeeUpdateForm
    template_name = 'partner/partner-update.html'
    success_url = 'deposit/partnet-list'


class PartnerDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'partner/partner_detail.html'


class PartnerDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'partner/partner-delete.html'
    success_url = '/deposit/partnet-list'


class PartnerCreateCardView(LoginRequiredMixin, CreateView):
    model = Partner
    template_name = 'partner/create_partner_card.html'
    success_url = '/deposit/partnet-list'
    fields = ['partner', 'credit_card', 'expire_date']

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save(commit=False)
        self.object.credit_card = str(self.object.credit_card).replace(" ", "")
        month_year = str(self.object.expire_date).split('/')
        self.object.credit_card_month = month_year[0]
        self.object.credit_card_year = month_year[1]
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        ctx = super(PartnerCreateCardView, self).get_context_data(**kwargs)
        ctx['partners'] = User.objects.filter(role=PARTNER, clinic=self.request.user.clinic)
        return ctx
