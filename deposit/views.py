from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from deposit.models import Deposit, Partner, PartnerAndPatient
from medanta.mixins import AllowedRolesMixin
from user.forms import SignUpForm, EmployeeUpdateForm
from user.models import User, PARTNER, ADMINISTRATOR, DOCTOR
from django.contrib.auth.decorators import login_required


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


@login_required
def depositDelete(request, pk):
    deposit = Deposit.objects.get(pk=pk)
    id = deposit.user.pk
    deposit.delete()
    return redirect("lead:customer_detail", pk=id)


class CreatePartnerView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR, PARTNER]
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


class PartnersListView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DOCTOR, PARTNER]
    template_name = 'partner/partneres.html'
    model = User
    paginate_by = 50

    def get_queryset(self):
        queryset = User.objects.filter(clinic=self.request.user.clinic, role=PARTNER)
        return queryset


class PartnerUpdateView(AllowedRolesMixin, LoginRequiredMixin, UpdateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR, PARTNER]
    model = User
    form_class = EmployeeUpdateForm
    template_name = 'partner/partner-update.html'
    success_url = 'deposit/partnet-list'


class PartnerDetailView(AllowedRolesMixin, LoginRequiredMixin, DetailView):
    allowed_roles = [ADMINISTRATOR, DOCTOR, PARTNER]
    model = User
    template_name = 'partner/partner_detail.html'


class PartnerDeleteView(AllowedRolesMixin, LoginRequiredMixin, DeleteView):
    allowed_roles = [ADMINISTRATOR, DOCTOR, PARTNER]
    model = User
    template_name = 'partner/partner-delete.html'
    success_url = '/deposit/partnet-list'


class PartnerCreateCardView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR, PARTNER]
    model = Partner
    template_name = 'partner/create_partner_card.html'
    fields = ['partner', 'credit_card', 'expire_date']

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save(commit=False)
        self.object.credit_card = str(self.object.credit_card).replace(" ", "")
        month_year = str(self.object.expire_date).split('/')
        self.object.credit_card_month = month_year[0]
        self.object.credit_card_year = month_year[1]
        self.object.save()
        return redirect("deposit:partnet-detail", self.request.user.pk)

    def get_context_data(self, **kwargs):
        ctx = super(PartnerCreateCardView, self).get_context_data(**kwargs)
        ctx['partners'] = User.objects.filter(role=PARTNER, clinic=self.request.user.clinic)
        return ctx


class PartnerAndPatientView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DOCTOR, PARTNER]
    model = PartnerAndPatient
    template_name = 'partner/partner_patient.html'

    def get_queryset(self):
        partner = Partner.objects.filter(partner_id=self.request.user.pk).first()
        if partner:
            queryset = PartnerAndPatient.objects.filter(partner_id=partner.pk)
        else:
            return None
        return queryset
