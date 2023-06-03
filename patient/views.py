import os
from io import BytesIO
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from deposit.models import Partner
from device.models import DeviceImage
from diagnostic.models import OphthalmologyStatus
from drug.models import Pharmacy, Operations
from patient.forms import QRCodeRegisterForm, QRCodePartnerForm
from patient.models import PatientComeHistory, CardToUser, QRCodeRegister, QRCodePartner, PhoneCode, \
    QrCodeGenerator1
from user.models import User, PATIENT, ADMINISTRATOR, RECEPTION, DOCTOR, NURSE, Clinic
from medanta.mixins import AllowedRolesMixin
from qrcode import *
import json
from docx import Document
from docx.shared import Inches


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
            object_list = self.model.objects.filter(clinic_id=self.request.user.clinic.id, card_id__icontains=query)
        else:
            object_list = self.model.objects.none()
        return object_list


class PatientComeHistoryCardView(View):
    def get(self, request, id, *args, **kwargs):
        patient_come = User.objects.filter(pk=id)
        context = {'patient_comes': patient_come}
        return render(request, 'qrcoderegister/patient-history-come.html', context)


# url va qr kod orqali ro'yxatdan o'tish
def historyView(request, cardId, clinicId):
    history = CardToUser.objects.filter(patient__clinic_id=clinicId, card_id__iexact=cardId)
    for h in history:
        if history:
            return redirect('patient:qr-come-patient', h.patient.id)
    return redirect('patient:qr-register', clinicId, cardId)


def code_generate(phone):
    import random
    if phone:
        key = random.randint(100000, 999999)
    return key


class QRCodeRegisterView(View):
    def get(self, request, clinicId, cardId, *args, **kwargs):
        context = {"card_id": cardId}
        self.request.session['card_id'] = cardId
        self.request.session['clinicId'] = clinicId
        print(self.request.session['card_id'])
        print(self.request.session['clinicId'])
        return render(request, 'qrcoderegister/qr_register.html', context)

    def post(self, request, cardId, *args, **kwargs):
        form = QRCodeRegisterForm(request.POST or None)
        if request.method == "POST":
            qr_phone = request.POST.get('qr_phone')
            self.request.session['qr_phone'] = qr_phone
            code1 = code_generate(qr_phone)
            print(code1)
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
        context["images"] = DeviceImage.objects.filter(patient__ophth_to_patient_come_history=self.object.id)
        context["drugs"] = Pharmacy.objects.filter(patient__ophth_to_patient_come_history=self.object.id)
        context["operatsiya"] = Operations.objects.filter(patient__ophth_to_patient_come_history=self.object.id)
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
            print(code1)
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
        queryset = QRCodePartner.objects.filter(partner__partner__clinic_id=self.request.user.clinic.id,
                                                is_confirmed=True)
        return queryset


def qr_partner_register_code(request):
    phone = request.session['qr_phone']
    get_code = PhoneCode.objects.get(phone=phone)
    register = QRCodePartner.objects.filter(qr_phone=request.session['qr_phone']).last()
    print(get_code.code)
    if get_code.code == request.POST.get('code'):
        register.is_confirmed = True
        register.save()
        return redirect("patient:success")

    return render(request, 'qrcoderegister/code.html')


def qr_register_code(request):
    phone = request.session['qr_phone']
    get_code = PhoneCode.objects.get(phone=phone)
    register = QRCodeRegister.objects.filter(qr_phone=request.session['qr_phone']).last()
    fio = register.fio.split()
    print(get_code.code == request.POST.get('code'))
    if get_code.code == request.POST.get('code'):
        if len(fio) == 3:
            patient = User.objects.create(clinic_id=request.session['clinicId'], phone=phone, first_name=fio[1],
                                          last_name=fio[0],
                                          middle_name=fio[len(fio) - 1])
        elif len(fio) == 2:
            patient = User.objects.create(clinic_id=request.session['clinicId'], phone=phone, first_name=fio[1],
                                          last_name=fio[0])
        else:
            patient = User.objects.create(clinic_id=request.session['clinicId'], phone=phone, first_name=fio[0])
        print(CardToUser.objects.create(patient=patient, card_id=register.card_id_qr))
        QRCodeRegister.objects.filter(qr_phone=phone).delete()
        return redirect("patient:success")

    return render(request, 'qrcoderegister/code.html')


def success(request):
    return render(request, 'qrcoderegister/success-register.html')


from django.http import JsonResponse


def qr_gen(request):
    qr = QrCodeGenerator1.objects.filter(clinic_id=request.user.clinic.id).last()
    id = CardToUser.objects.filter(clinic_id=request.user.clinic.id).last()
    if qr is not None:
        if qr or qr.qr_code_img:
            qr1 = qr_code_generator_number(qr.qr_code)
            print(qr1)
            img_name1 = 'qr' + str(qr1) + '.ico'
            os.remove(f'static/images/{img_name1}')
        qr = qr_code_generator_number(int(id.card_id) + 1)
        qr_generte = qr_generator(request, qr)
        img_name = 'qr' + str(qr) + '.ico'
        context = {"qr_code": qr, "image": f'static/images/{img_name}', 'pk': qr_generte.pk}
        return JsonResponse({"qr_code": context}, status=200)
    else:
        qr = qr_code_generator_number(1)
        qr_generte = qr_generator(request, qr)
        img_name = 'qr' + str(qr) + '.ico'
        QrCodeGenerator1.objects.create(clinic_id=request.user.clinic.id, qr_code=qr, qr_code_url=qr_generte.qr_code_url, qr_code_img=img_name)
        qr = {"qr_code": qr, "image": f'static/images/{img_name}', 'pk': qr_generte.pk}
        return JsonResponse({"qr_code": qr}, status=200)


def qr_code_second_generator(request, pk):
    aa = request.get_host()
    host = request.META['REMOTE_ADDR']
    user = User.objects.get(pk=pk)
    card_to_user = CardToUser.objects.filter(clinic_id=request.user.clinic.id, patient_id=user.pk).last()
    familiya = user.last_name
    ism = user.first_name
    birthday = user.birthday
    phone = user.phone
    data = f'http://{request.get_host()}/patient/card-id/{request.user.clinic.id}/{card_to_user.card_id}'
    context = {"qr_code": card_to_user.card_id, "image": data, "familiya": familiya, "ism": ism, "birthday": birthday,
               "phone": phone, "name": host, 'host':aa}
    return render(request, "print/print.html", context)


def qr_code_generator_number(qr_code):
    qr_code1 = len(str(qr_code))
    zero = ("0" * (7 - qr_code1)) + str(qr_code)
    return zero


def qr_generator(request, qr):
    data = f'http://{request.get_host()}/patient/card-id/{request.user.clinic.id}/{qr}'
    img = make(data)
    img_name = 'qr' + str(qr) + '.ico'
    img.save(f'static/images/{img_name}')
    return QrCodeGenerator1.objects.create(clinic_id=request.user.clinic.id, qr_code=qr, qr_code_url=data, qr_code_img=img_name)
