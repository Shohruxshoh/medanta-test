from django.shortcuts import render, redirect
from django.views import View
from drug.models import Drugs, Pharmacy, Operations
from lead.models import Lead
from medanta.mixins import AllowedRolesMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from service.models import Service
from user.models import User, DOCTOR, ADMINISTRATOR, RECEPTION
from patient.models import PatientComeHistory


# Create your views here.


class DrugListView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DOCTOR, RECEPTION]
    model = Drugs
    template_name = 'drug/drug_list.html'

    def get_queryset(self):
        queryset = Drugs.objects.filter(clinic=self.request.user.clinic)
        return queryset


class DrugCreateView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR, RECEPTION]
    model = Drugs
    fields = ['name', 'clinic']
    template_name = 'drug/drug_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.clinic = self.request.user.clinic
        self.object.save()
        return redirect('drug:drugs')


class DrugUpdateView(AllowedRolesMixin, LoginRequiredMixin, UpdateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR, RECEPTION]
    model = Drugs
    fields = ['name']
    template_name = 'drug/drug_update.html'
    success_url = '/drug'


class DrugDeleteView(AllowedRolesMixin, LoginRequiredMixin, DeleteView):
    allowed_roles = [ADMINISTRATOR, DOCTOR, RECEPTION]
    model = Drugs
    template_name = 'drug/drug-delete.html'
    success_url = '/drug'


class PharmacyView(AllowedRolesMixin, LoginRequiredMixin, View):
    allowed_roles = [ADMINISTRATOR, DOCTOR, RECEPTION]

    def get(self, request, *args, **kwargs):
        drugs = Drugs.objects.filter(clinic=request.user.clinic)
        context = {"drugs": drugs}
        return render(request, 'drug/drug_add.html', context)

    def post(self, request, pk, *args, **kwargs):
        drugs = Drugs.objects.filter(clinic=request.user.clinic)
        for drug in drugs:
            if request.POST.get(f"true{drug.pk}") is not None:
                Pharmacy.objects.create(patient_id=pk, drug_id=request.POST.get(f"{drug.pk}"),
                                        start_time=request.POST.get(f"start_time{drug.pk}"),
                                        between_time=request.POST.get(f"between_time{drug.pk}"),
                                        lifetime=request.POST.get(f"lifetime{drug.pk}"),
                                        expensive_time=request.POST.get(f"time{drug.pk}"))
        return redirect("diagnostic:patient-come-now-doctor")


class PharmacyListView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DOCTOR, RECEPTION]
    model = PatientComeHistory
    template_name = 'drug/pharmacy_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pharm"] = Pharmacy.objects.filter(patient__patient__clinic_id=self.request.user.clinic, is_active=True)
        return context


class PharmacyDetailView(AllowedRolesMixin, LoginRequiredMixin, View):
    allowed_roles = [ADMINISTRATOR, DOCTOR, RECEPTION]

    def get(self, request, pk, *args, **kwargs):
        pharmacy = Pharmacy.objects.filter(patient_id=pk)
        context = {"pharmacies": pharmacy}
        return render(request, 'drug/pharmacy_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        pharmacy = Pharmacy.objects.filter(patient_id=pk)
        patient = PatientComeHistory.objects.get(pk=pk)
        patient.is_active = False
        patient.save()
        for i in pharmacy:
            if request.POST.get(f"{i.pk}") is not None:
                p = Pharmacy.objects.get(pk=i.pk)
                p.is_active = False
                p.save()
        return redirect('drug:pharmacy-list')


class OperationsView(AllowedRolesMixin, LoginRequiredMixin, View):
    allowed_roles = [ADMINISTRATOR, DOCTOR, RECEPTION]

    def get(self, request, id, *args, **kwargs):
        form = Service.objects.filter(service_price__clinic_id=request.user.clinic.pk)
        return render(request, 'drug/operation_create.html', {"id": id, 'form': form})

    def post(self, request, id, *args, **kwargs):
        if request.method == "POST":
            Operations.objects.create(patient_id=id, service_id=request.POST.get('service'))
        return redirect("diagnostic:patient-come-now-doctor")


class OperationListView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DOCTOR, RECEPTION]
    model = PatientComeHistory
    template_name = 'drug/operations_list.html'


class OperationDetailView(AllowedRolesMixin, LoginRequiredMixin, View):
    allowed_roles = [ADMINISTRATOR, DOCTOR, RECEPTION]

    def get(self, request, pk, *args, **kwargs):
        operations = Operations.objects.filter(patient_id=pk).last()
        context = {"operations": operations}
        return render(request, 'drug/operation-detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        if request.method == 'POST':
            if request.POST.get('paid') is None:
                paid = False
            else:
                paid = True
            if request.POST.get('percentage') == '':
                percentage = 1
            else:
                percentage = request.POST.get('percentage')
            service = Service.objects.filter(id=request.POST.get('service_id'), service_price__is_active=True).last()
            lead_price = int(service.service_price.price) * (1 - (int(percentage) / 100))
            Lead.objects.create(user_id=request.POST.get("user_id"), service_id=request.POST.get("service_id"),
                                percentage=percentage, lead_price=lead_price,
                                operation_came_time=request.POST.get("operation_came_time"), paid=paid,
                                payment_method=request.POST.get('payment_method'))
            operations = Operations.objects.filter(patient_id=pk).last()
            operations.is_active_operations = False
            operations.save()
            patient = PatientComeHistory.objects.filter(pk=pk, is_active=True).last()
            patient.is_active = False
            patient.save()
        return redirect('drug:operation-list')
