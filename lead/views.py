from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView
from accountant.models import DayAccountant
from deposit.models import Deposit, Partner, PartnerAndPatient
from lead.forms import CustomerForm, CustomerUpdateForm, LeadForm
from lead.models import Lead
from patient.models import PatientComeHistory, QrCodeGenerator1
from patient.models import CardToUser
from service.models import Service
from user.models import User, District, PATIENT, Clinic, ADMINISTRATOR, RECEPTION, DOCTOR
from medanta.mixins import AllowedRolesMixin


# Create your views here.

class HomeView(LoginRequiredMixin, ListView):
    queryset = Clinic.objects.all()
    template_name = "index.html"


class CustomerCreateView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [RECEPTION, ADMINISTRATOR]
    model = User
    form_class = CustomerForm
    template_name = 'lead/create.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(CustomerCreateView, self).get_context_data(**kwargs)
        context['partner'] = Partner.objects.filter(partner__clinic_id=self.request.user.clinic.id)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.clinic = self.request.user.clinic
        self.object.phone = str(self.object.phone).replace(" ", '')
        user = User.objects.filter(phone=self.object.phone).exists()
        if not user:
            self.object.username = str(self.object.first_name) + str(self.object.phone)
            self.object.save()
            if self.request.POST.get('qr-pk') != "":
                qr = QrCodeGenerator1.objects.get(pk=self.request.POST.get('qr-pk'))
                qr.qr_code = int(self.request.POST.get('qr-code'))
                qr.save()
                CardToUser.objects.create(clinic=self.request.user.clinic, patient_id=self.object.pk,
                                          card_id=self.request.POST.get('qr-code'))
            PartnerAndPatient.objects.create(partner_id=self.request.POST.get("partner"), patient_id=self.object.pk)
            return redirect('lead:customer_detail', self.object.id)
        else:
            messages.error(self.request, "Bunday telefon raqam mavjud")
            return redirect("lead:create")


class CustomerUpdateView(AllowedRolesMixin, LoginRequiredMixin, UpdateView):
    allowed_roles = [RECEPTION, ADMINISTRATOR]
    model = User
    form_class = CustomerUpdateForm
    template_name = 'lead/update.html'
    success_url = '/'


class CustomerDeleteView(AllowedRolesMixin, LoginRequiredMixin, DeleteView):
    allowed_roles = [RECEPTION, ADMINISTRATOR]
    model = User
    template_name = 'lead/delete.html'
    success_url = '/'


class CustomerListView(LoginRequiredMixin, ListView):
    template_name = 'lead/customers.html'
    model = User
    paginate_by = 50

    def get_queryset(self):
        queryset = User.objects.filter(role=PATIENT, clinic=self.request.user.clinic).order_by("-created_at")
        return queryset


class CustomerPayInstallmentListView(LoginRequiredMixin, ListView):
    template_name = 'reception/director/pay_installments_patient.html'
    model = User
    paginate_by = 50

    def get_queryset(self):
        queryset = User.objects.filter(clinic=self.request.user.clinic, is_installment=True)
        return queryset


class CustomDetailView(AllowedRolesMixin, LoginRequiredMixin, DetailView):
    allowed_roles = [RECEPTION, ADMINISTRATOR, DOCTOR]
    model = User
    template_name = 'lead/customer_detail.html'

    def post(self, request, *args, **kwargs):
        if request.POST.get("summa") is not None:
            Deposit.objects.create(user_id=request.POST.get('patient'), service_id=request.POST.get('service_deposit'),
                                   sum_total=request.POST.get('summa'))
            return redirect('lead:customer_detail', pk=request.POST.get('patient'))
        if request.POST.get('paid') is None:
            paid = False
        else:
            paid = True
        if request.POST.get('service') is not None:
            if request.POST.get('percentage') == '':
                percentage = 1
            else:
                percentage = request.POST.get('percentage')
            service = Service.objects.filter(id=request.POST.get('service'), service_price__is_active=True).last()
            lead_price = int(service.service_price.price) * (1 - (int(percentage) / 100))
            Lead.objects.create(user_id=request.POST.get('patient'),
                                service_id=request.POST.get('service'),
                                lead_price=lead_price,
                                paid=paid,
                                percentage=percentage,
                                payment_method=request.POST.get('payment_method'),
                                )
            if paid:
                DayAccountant.objects.create(patient_id=request.POST.get('patient'),
                                             service_id=request.POST.get('service'), sum_total=lead_price)
            return redirect('lead:customer_detail', pk=request.POST.get('patient'))

        if request.POST.get('card_id') is None or request.POST.get('card_id') == '':
            if request.POST.get('is_active') is None:
                history_patient = PatientComeHistory.objects.get(patient_id=request.POST.get('patient'))
                history_patient.is_active = False
                history_patient.save()
            else:
                PatientComeHistory.objects.create(patient_id=request.POST.get('patient'),
                                                  is_active=True)
            return redirect('lead:customer_detail', pk=request.POST.get('patient'))
        if not CardToUser.objects.filter(clinic=request.user.clinic, card_id=request.POST.get('card_id')).exists():
            CardToUser.objects.create(clinic=request.user.clinic, patient_id=request.POST.get('patient'),
                                      card_id=request.POST.get('card_id'))
            PatientComeHistory.objects.create(patient_id=request.POST.get('patient'), is_active=True)
        else:
            messages.error(request, "Bunday ID mavjud")
        return redirect('lead:customer_detail', pk=request.POST.get('patient'))

    def get_context_data(self, **kwargs):
        ctx = super(CustomDetailView, self).get_context_data(**kwargs)
        ctx['lead_form'] = LeadForm
        ctx['patient_first_come'] = PatientComeHistory.objects.filter(patient_id=self.object.id).first()
        ctx['patient_last_come'] = PatientComeHistory.objects.filter(patient_id=self.object.id).last()
        ctx['patients'] = PatientComeHistory.objects.filter(patient_id=self.object.id, is_active=True).last()
        return ctx


class LeadUpdateView(AllowedRolesMixin, LoginRequiredMixin, View):
    allowed_roles = [RECEPTION, ADMINISTRATOR]

    def get(self, request, pk, *args, **kwargs):
        lead = Lead.objects.get(pk=pk)
        return render(request, 'lead/lead-update.html', {"lead": lead})

    def post(self, request, pk, *args, **kwargs):
        lead = Lead.objects.get(pk=pk)
        if request.method == "POST":
            if request.POST.get('paid') is None:
                paid = False
            else:
                paid = True
            lead1 = Lead.objects.get(pk=pk)
            lead1.percentage = request.POST.get('percentage')
            lead1.paid = paid
            lead1.payment_method = request.POST.get('payment_method')
            lead1.save()
        return redirect("lead:customer_detail", lead.user.pk)


def loadRegion(request):
    region_id = request.GET.get('region_id')
    districts = District.objects.filter(region_id=region_id)
    return JsonResponse(list(districts.values('id', 'title')), safe=False)


def check_user_phone(request):
    phone = request.GET.get("phone")
    p = str(phone).replace(" ", '')
    data = {
        'is_has': User.objects.filter(clinic=request.user.clinic, phone=p).exists()
    }
    if data["is_has"]:
        data["erorr"] = "Bunday telefon mavjud"
    return JsonResponse(data)
