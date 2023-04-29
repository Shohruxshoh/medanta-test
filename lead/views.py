from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView
from lead.forms import CustomerForm, CustomerUpdateForm, LeadForm
from lead.models import Lead
from patient.models import PatientComeHistory
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

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.clinic = self.request.user.clinic
        self.object.phone = str(self.object.phone).replace(" ", '')
        self.object.username = str(self.object.first_name) + str(self.object.phone)
        self.object.save()
        return redirect('lead:customer_detail', self.object.id)


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
        queryset = User.objects.filter(role=PATIENT)
        return queryset


class CustomerPayInstallmentListView(LoginRequiredMixin, ListView):
    template_name = 'reception/director/pay_installments_patient.html'
    model = User
    paginate_by = 50

    def get_queryset(self):
        queryset = User.objects.filter(is_installment=True)
        return queryset


class CustomDetailView(AllowedRolesMixin, LoginRequiredMixin, DetailView):
    allowed_roles = [RECEPTION, ADMINISTRATOR, DOCTOR]
    model = User
    template_name = 'lead/customer_detail.html'

    def post(self, request, *args, **kwargs):
        if request.POST.get('paid') is None:
            paid = False
        else:
            paid = True
        if request.POST.get('service') is not None:
            service = Service.objects.filter(id=request.POST.get('service'), service_price__is_active=True).last()
            lead_price = int(service.service_price.price) * (1 - (int(request.POST.get('percentage')) / 100))
            lead = Lead.objects.create(user_id=request.POST.get('patient'),
                                       service_id=request.POST.get('service'),
                                       lead_price=lead_price,
                                       paid=paid,
                                       percentage=request.POST.get('percentage'),
                                       payment_method=request.POST.get('payment_method'),
                                       )
            return redirect('lead:customer_detail', pk=request.POST.get('patient'))

        if request.POST.get('card_id') is None or request.POST.get('card_id') == '':
            print(request.POST.get('is_active'))
            if request.POST.get('is_active') is None:
                history_patient = PatientComeHistory.objects.get(patient_id=request.POST.get('patient'))
                history_patient.is_active = False
                history_patient.save()
                print(request.POST.get('patient'))
            else:
                history_patient = PatientComeHistory.objects.create(patient_id=request.POST.get('patient'),
                                                                    is_active=True)
                print(request.POST.get('patient'))
            return redirect('lead:customer_detail', pk=request.POST.get('patient'))
        if not CardToUser.objects.filter(card_id=request.POST.get('card_id')).exists():
            card = CardToUser.objects.create(patient_id=request.POST.get('patient'),
                                             card_id=request.POST.get('card_id'))
            history_patient = PatientComeHistory.objects.create(patient_id=request.POST.get('patient'), is_active=True)
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


class QrcodeRegisterView(CreateView):
    pass


def patientHistoryIsActive(request):
    pass


def loadRegion(request):
    region_id = request.GET.get('region_id')
    districts = District.objects.filter(region_id=region_id)
    return JsonResponse(list(districts.values('id', 'title')), safe=False)

# def generatsion(i):
#     mb_user_code = 'mb-000000' + i
#     if i > 10:
#         mb_user_code = 'mb-00000' + i
#     if i > 100:
#         mb_user_code = 'mb-0000' + i
#     if i > 1000:
#         mb_user_code = 'mb-000' + i
#     if i > 10000:
#         mb_user_code = 'mb-00' + i
#     if i > 100000:
#         mb_user_code = 'mb-0' + i
#     if i > 1000000:
#         mb_user_code = 'mb-' + i
#     return mb_user_code


# def create(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         last_name = request.POST['last_name']
#         first_name = request.POST['first_name']
#         middle_name = request.POST['middle_name']
#         region = request.POST.get('region')
#         district = request.POST.get('district')
#         birthday = request.POST['birthday']
#         phone = request.POST['phone']
#         passport_seria = request.POST['passport_seria']
#         passport_number = request.POST['passport_number']
#         person_id = request.POST['person_id']
#         gender = request.POST.get('gender')
#         username = first_name + str(phone)
#         user = User(username=username, last_name=last_name, first_name=first_name, middle_name=middle_name,
#                     region_id=region, district_id=district, birthday=birthday, phone=phone,
#                     passport_seria=passport_seria, passport_number=passport_number, person_id=person_id, gender=gender)
#         user.save()
#         success = f"Foydalanuvchi {username} qo'shildi"
#         return HttpResponse(success)
#     return render(request, 'lead/customers.html')
