from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from deposit.models import Partner
from diagnostic.models import OphthalmologyStatus
from patient.forms import QRCodeRegisterForm, QRCodePartnerForm
from patient.models import PatientComeHistory, CardToUser, QRCodeRegister, QRCodePartner, PhoneCode
from user.models import User, PARTNER, PATIENT, ADMINISTRATOR, RECEPTION, DOCTOR, NURSE, Clinic
from medanta.mixins import AllowedRolesMixin


# Create your views here.

class Home(ListView):
    model = Clinic
    template_name = 'abs.html'


class PatientComeHistoryCreateView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [ADMINISTRATOR, RECEPTION]
    model = PatientComeHistory
    template_name = 'lead/create_patient_history.html'
    fields = ['patient', 'partner', 'is_active']
    success_url = '/list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('diagnostic:patient-come')

    def get_context_data(self, **kwargs):
        ctx = super(PatientComeHistoryCreateView, self).get_context_data(**kwargs)
        ctx['partners'] = Partner.objects.all()
        ctx['patients'] = User.objects.filter(role=PATIENT, clinic=self.request.user.clinic)
        return ctx


class CreateCardIdView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [ADMINISTRATOR, RECEPTION]
    model = CardToUser
    template_name = 'lead/create_id_card.html'
    fields = ['patient', "card_id"]

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('lead:customer_detail', self.object.patient.id)

    def get_context_data(self, **kwargs):
        ctx = super(CreateCardIdView, self).get_context_data(**kwargs)
        ctx['patients'] = User.objects.filter(role=PATIENT, clinic=self.request.user.clinic)
        return ctx


class SearchCardIdView(LoginRequiredMixin, ListView):
    template_name = 'lead/patient_search.html'
    model = CardToUser

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(card_id__icontains=query)
        else:
            object_list = self.model.objects.none()
        return object_list


class PatientComeHistoryCardView(View):
    def get(self, request, id, *args, **kwargs):
        patient_come = User.objects.filter(pk=id)
        context = {'patient_comes': patient_come}
        return render(request, 'qrcoderegister/patient-history-come.html', context)


# url va qr kod orqali ro'yxatdan o'tish
def historyView(request, cardId):
    history = CardToUser.objects.filter(card_id__iexact=cardId)
    for h in history:
        if history:
            return redirect('patient:qr-come-patient', h.patient.id)
    return redirect('patient:qr-register', cardId)


def code_generate(phone):
    import random
    if phone:
        key = random.randint(100000, 999999)
    return key


class QRCodeRegisterView(View):
    def get(self, request, cardId, *args, **kwargs):
        context = {"card_id": cardId}
        self.request.session['card_id'] = cardId
        print(self.request.session['card_id'])
        return render(request, 'qrcoderegister/qr_register.html', context)

    def post(self, request, cardId, *args, **kwargs):
        form = QRCodeRegisterForm(request.POST or None)
        if request.method == "POST":
            qr_phone = request.POST.get('qr_phone')
            self.request.session['qr_phone'] = qr_phone
            code1 = code_generate(qr_phone)
            phone1 = PhoneCode.objects.filter(phone__iexact=qr_phone).exists()
            qr_register = QRCodeRegister.objects.filter(qr_phone__iexact=qr_phone).exclude(is_confirmed=False)
            if form.is_valid():
                if not qr_register.exists():
                    if phone1:
                        PhoneCode.objects.filter(phone__iexact=qr_phone).delete()
                        PhoneCode.objects.create(phone=qr_phone, code=code1)
                        form.save()
                        return redirect('patient:code-check')
                    else:
                        PhoneCode.objects.create(phone=qr_phone, code=code1)
                        form.save()
                        return redirect('patient:code-check')
                else:
                    context = {'message': "Bu telefon raqam bilan ro'yxatdan o'tilgan"}
                    return render(request, 'qrcoderegister/qr_register.html', context)
        else:
            form = QRCodeRegisterForm(request.POST or None)
            context = {"form": form}
            return render(request, 'qrcoderegister/qr_register.html', context)


class OpticCamePatientView(DetailView):
    model = OphthalmologyStatus
    template_name = 'qrcoderegister/patient-history-cme-detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(OpticCamePatientView,
                        self).get_context_data(*args, **kwargs)
        context["come_od"] = PatientComeHistory.objects.filter(ophth_to_patient_come_history=self.object.id)
        return context


class QRCodePartnerView(View):
    def get(self, request, id, *args, **kwargs):
        form = QRCodePartnerForm(request.POST or None)
        context = {"id": id, "form": form}
        return render(request, 'partner/partner_register.html', context)

    def post(self, request, id, *args, **kwargs):
        form = QRCodePartnerForm(request.POST or None)
        if request.method == "POST":
            qr_phone = request.POST.get('qr_phone')
            self.request.session['qr_phone'] = qr_phone
            code1 = code_generate(qr_phone)
            phone1 = PhoneCode.objects.filter(phone__iexact=qr_phone).exists()
            partner_qr_code = QRCodePartner.objects.filter(qr_phone=qr_phone).exclude(is_confirmed=False)
            if form.is_valid():
                if not partner_qr_code.exists():
                    if phone1:
                        PhoneCode.objects.filter(phone__iexact=qr_phone).delete()
                        PhoneCode.objects.create(phone=qr_phone, code=code1)
                        form.save()
                        return redirect('patient:code-check-partner')
                    else:
                        PhoneCode.objects.create(phone=qr_phone, code=code1)
                        form.save()
                        return redirect('patient:code-check-partner')
                else:
                    context = {'message': "Bu telefon raqam bilan ro'yxatdan o'tilgan"}
                    return render(request, 'partner/partner_register.html', context)
        else:
            form = QRCodePartnerForm(request.POST or None)
            context = {"form": form}
            return render(request, 'partner/partner_register.html', context)

        context = {"form": form, "id": id}
        return render(request, 'partner/partner_register.html', context)


class QRCodeRegisterListView(LoginRequiredMixin, ListView):
    model = QRCodeRegister
    template_name = 'qrcoderegister/qr_code_register_list.html'


class QRCodePartnerListView(LoginRequiredMixin, ListView):
    model = QRCodePartner
    template_name = 'partner/qr_code_partner_list.html'

    def get_queryset(self):
        queryset = QRCodePartner.objects.filter(is_confirmed=True)
        return queryset


def qr_partner_register_code(request):
    phone = request.session['qr_phone']
    get_code = PhoneCode.objects.get(phone=phone)
    register = QRCodePartner.objects.filter(qr_phone=request.session['qr_phone']).last()
    print(get_code.code)
    if get_code.code == request.POST.get('code'):
        register.is_confirmed = True
        register.save()
        return render(request, 'qrcoderegister/success-register.html')

    return render(request, 'qrcoderegister/code.html')


def qr_register_code(request):
    phone = request.session['qr_phone']
    get_code = PhoneCode.objects.get(phone=phone)
    register = QRCodeRegister.objects.filter(qr_phone=request.session['qr_phone']).last()
    fio = register.fio.split()
    print(get_code.code)
    if get_code.code == request.POST.get('code'):

        if len(fio) == 3:
            patient = User.objects.create(phone=phone, first_name=fio[1], last_name=fio[0],
                                          middle_name=fio[len(fio) - 1])
        elif len(fio) == 2:
            patient = User.objects.create(phone=phone, first_name=fio[1], last_name=fio[0])
        else:
            patient = User.objects.create(phone=phone, first_name=fio[0])
        CardToUser.objects.create(patient=patient, card_id=register.card_id_qr)
        QRCodeRegister.objects.filter(qr_phone=phone).delete()
        return render(request, 'qrcoderegister/success-register.html')

    return render(request, 'qrcoderegister/code.html')