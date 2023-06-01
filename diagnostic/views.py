from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from diagnostic.forms import VisusForm, OphthalmologyStatusForm
from diagnostic.models import Visus, Complaint, Eyelids, Eyeball, Conjunctiva, Сornea, FrontCamera, PupilOfTheEye, Lens, \
    VitreousBody, OcularFundus, Diagnosis, OphthalmologyStatus
from medanta.mixins import AllowedRolesMixin
from patient.models import PatientComeHistory
from user.models import NURSE, ADMINISTRATOR, DOCTOR, RECEPTION, User


# Create your views here.

class VisusCreateView(AllowedRolesMixin, LoginRequiredMixin, View):
    allowed_roles = [NURSE, ADMINISTRATOR]

    def get(self, request, come_history_id, *args, **kwargs):
        patients = PatientComeHistory.objects.get(pk=come_history_id)
        form = VisusForm()
        context = {'form': form, 'patient': patients}
        return render(request, 'nurse/visus.html', context)

    def post(self, request, come_history_id, *args, **kwargs):
        form = VisusForm(request.POST)
        if form:
            bk_od = request.POST.get('bk_od')
            bk_os = request.POST.get('bk_os')
            cd_od = request.POST.get('cd_od')
            cd_os = request.POST.get('cd_os')
            sph_od = request.POST.get('sph_od')
            sph_os = request.POST.get('sph_os')
            cyl_od = request.POST.get('cyl_od')
            cyl_os = request.POST.get('cyl_os')
            ax_od = request.POST.get('ax_od')
            ax_os = request.POST.get('ax_os')
            bliz_od = request.POST.get('bliz_od')
            bliz_os = request.POST.get('bliz_os')
            ck_od = request.POST.get('ck_od')
            ck_os = request.POST.get('ck_os')

            a = Visus.objects.create(bk_id=bk_od, cd_id=cd_od, sph=sph_od, cyl=cyl_od, ax=ax_od, bliz=bliz_od,
                                     ck_id=ck_od,
                                     patient_come_history_id=come_history_id, nurse_id=request.user.pk)
            b = Visus.objects.create(bk_id=bk_os, eye=1, cd_id=cd_os, sph=sph_os, cyl=cyl_os, ax=ax_os, bliz=bliz_os,
                                     ck_id=ck_os, patient_come_history_id=come_history_id, nurse_id=request.user.pk)
            messages.success(request, "Success")
            return redirect('diagnostic:detail-visus', pk=come_history_id)
        else:
            form = VisusForm()
            context = {'form': form}
            return render(request, 'nurse/visus.html', context)


class PatientComeListActiveView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [NURSE, ADMINISTRATOR, DOCTOR, RECEPTION]
    model = PatientComeHistory
    template_name = 'nurse/patient_come.html'

    def get_queryset(self):
        queryset = PatientComeHistory.objects.filter(patient__clinic=self.request.user.clinic, is_active=True)
        return queryset


class VisusPatientDetailView(AllowedRolesMixin, LoginRequiredMixin, DetailView):
    allowed_roles = [NURSE, ADMINISTRATOR, DOCTOR, RECEPTION]
    model = PatientComeHistory
    template_name = 'nurse/visus_patient_detail.html'


class ComplaintListView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Complaint
    paginate_by = 50
    template_name = 'diagnostic/complaint/complaints.html'

    def get_queryset(self):
        queryset = Complaint.objects.filter(clinic_id=self.request.user.clinic.pk)
        return queryset


class ComplaintCreateView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Complaint
    template_name = 'diagnostic/complaint/complaint-create.html'
    fields = ['title']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.clinic = self.request.user.clinic
        self.object.save()
        return redirect('diagnostic:complaints')


class ComplaintUpdateView(AllowedRolesMixin, LoginRequiredMixin, UpdateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Complaint
    template_name = 'diagnostic/complaint/complaint-update.html'
    fields = ['title']
    success_url = '/diagnostic/complaints'


class ComplaintDeleteView(AllowedRolesMixin, LoginRequiredMixin, DeleteView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Complaint
    template_name = 'diagnostic/complaint/complaint-delete.html'
    success_url = '/diagnostic/complaints'


class EyelidsListView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Eyelids
    paginate_by = 50
    template_name = "diagnostic/eyelids/eyelids.html"

    def get_queryset(self):
        queryset = Eyelids.objects.filter(clinic_id=self.request.user.clinic.pk)
        return queryset


class EyelidsCreateView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Eyelids
    template_name = 'diagnostic/eyelids/eyelid-create.html'
    fields = ['title']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.clinic = self.request.user.clinic
        self.object.save()
        return redirect('diagnostic:eyelids')


class EyelidsUpdateView(AllowedRolesMixin, LoginRequiredMixin, UpdateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Eyelids
    template_name = 'diagnostic/eyelids/eyelid-update.html'
    fields = ['title']
    success_url = '/diagnostic/eyelids'


class EyelidsDeleteView(AllowedRolesMixin, LoginRequiredMixin, DeleteView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Eyelids
    template_name = 'diagnostic/eyelids/eyelid-delete.html'
    success_url = '/diagnostic/eyelids'


class EyeballListView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Eyeball
    paginate_by = 50
    template_name = "diagnostic/eyeball/eyeballs.html"

    def get_queryset(self):
        queryset = Eyeball.objects.filter(clinic_id=self.request.user.clinic.pk)
        return queryset


class EyeballCreateView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Eyeball
    template_name = 'diagnostic/eyeball/eyeball-create.html'
    fields = ['title']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.clinic = self.request.user.clinic
        self.object.save()
        return redirect('diagnostic:eyeballs')


class EyeballUpdateView(AllowedRolesMixin, LoginRequiredMixin, UpdateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Eyeball
    template_name = 'diagnostic/eyeball/eyeball-update.html'
    fields = ['title']
    success_url = '/diagnostic/eyeballs'


class EyeballDeleteView(AllowedRolesMixin, LoginRequiredMixin, DeleteView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Eyeball
    template_name = 'diagnostic/eyeball/eyeball-delete.html'
    success_url = '/diagnostic/eyeballs'


class ConjunctivaListView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Conjunctiva
    paginate_by = 50
    template_name = "diagnostic/conjunctiva/conjunctiva.html"

    def get_queryset(self):
        queryset = Conjunctiva.objects.filter(clinic_id=self.request.user.clinic.pk)
        return queryset


class ConjunctivaCreateView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Conjunctiva
    template_name = 'diagnostic/conjunctiva/conjunctiva-create.html'
    fields = ['title']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.clinic = self.request.user.clinic
        self.object.save()
        return redirect('diagnostic:conjunctivas')


class ConjunctivaUpdateView(AllowedRolesMixin, LoginRequiredMixin, UpdateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Conjunctiva
    template_name = 'diagnostic/conjunctiva/conjunctiva-update.html'
    fields = ['title']
    success_url = '/diagnostic/conjunctiva'


class ConjunctivaDeleteView(AllowedRolesMixin, LoginRequiredMixin, DeleteView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Conjunctiva
    template_name = 'diagnostic/conjunctiva/conjunctiva-delete.html'
    success_url = '/diagnostic/conjunctiva'


class СorneaListView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Сornea
    paginate_by = 50
    template_name = "diagnostic/cornea/cornea.html"

    def get_queryset(self):
        queryset = Сornea.objects.filter(clinic_id=self.request.user.clinic.pk)
        return queryset


class СorneaCreateView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Сornea
    template_name = 'diagnostic/cornea/cornea-create.html'
    fields = ['title']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.clinic = self.request.user.clinic
        self.object.save()
        return redirect('diagnostic:corneas')


class СorneaUpdateView(AllowedRolesMixin, LoginRequiredMixin, UpdateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Сornea
    template_name = 'diagnostic/cornea/cornea-update.html'
    fields = ['title']
    success_url = '/diagnostic/corneas'


class СorneaDeleteView(AllowedRolesMixin, LoginRequiredMixin, DeleteView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Сornea
    template_name = 'diagnostic/cornea/cornea-delete.html'
    success_url = '/diagnostic/corneas'


class FrontCameraListView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = FrontCamera
    paginate_by = 50
    template_name = "diagnostic/front-camera/front-cameras.html"

    def get_queryset(self):
        queryset = FrontCamera.objects.filter(clinic_id=self.request.user.clinic.pk)
        return queryset


class FrontCameraCreateView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = FrontCamera
    template_name = 'diagnostic/front-camera/front-camera-create.html'
    fields = ['title']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.clinic = self.request.user.clinic
        self.object.save()
        return redirect('diagnostic:front-cameras')


class FrontCameraUpdateView(AllowedRolesMixin, LoginRequiredMixin, UpdateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = FrontCamera
    template_name = 'diagnostic/front-camera/front-camera-update.html'
    fields = ['title']
    success_url = '/diagnostic/front-cameras'


class FrontCameraDeleteView(LoginRequiredMixin, DeleteView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = FrontCamera
    template_name = 'diagnostic/front-camera/front-camera-delete.html'
    success_url = '/diagnostic/front-cameras'


class PupilOfTheEyeListView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = PupilOfTheEye
    paginate_by = 50
    template_name = "diagnostic/pupil-of-the-eye/pupil-of-the-eye.html"

    def get_queryset(self):
        queryset = PupilOfTheEye.objects.filter(clinic_id=self.request.user.clinic.pk)
        return queryset


class PupilOfTheEyeCreateView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = PupilOfTheEye
    template_name = 'diagnostic/pupil-of-the-eye/pupil-of-the-eye-create.html'
    fields = ['title']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.clinic = self.request.user.clinic
        self.object.save()
        return redirect('diagnostic:pupil-of-the-eye')


class PupilOfTheEyeUpdateView(AllowedRolesMixin, LoginRequiredMixin, UpdateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = PupilOfTheEye
    template_name = 'diagnostic/pupil-of-the-eye/pupil-of-the-eye-update.html'
    fields = ['title']
    success_url = '/diagnostic/pupil-of-the-eye'


class PupilOfTheEyeDeleteView(AllowedRolesMixin, LoginRequiredMixin, DeleteView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = PupilOfTheEye
    template_name = 'diagnostic/pupil-of-the-eye/pupil-of-the-eye-delete.html'
    success_url = '/diagnostic/pupil-of-the-eye'


class LensListView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Lens
    paginate_by = 50
    template_name = "diagnostic/lens/lens.html"

    def get_queryset(self):
        queryset = Lens.objects.filter(clinic_id=self.request.user.clinic.pk)
        return queryset


class LensCreateView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Lens
    template_name = 'diagnostic/lens/lens-create.html'
    fields = ['title']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.clinic = self.request.user.clinic
        self.object.save()
        return redirect('diagnostic:lens')


class LensUpdateView(AllowedRolesMixin, LoginRequiredMixin, UpdateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Lens
    template_name = 'diagnostic/lens/lens-update.html'
    fields = ['title']
    success_url = '/diagnostic/lens'


class LensDeleteView(AllowedRolesMixin, LoginRequiredMixin, DeleteView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Lens
    template_name = 'diagnostic/lens/lens-delete.html'
    success_url = '/diagnostic/lens'


class VitreousBodyListView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = VitreousBody
    paginate_by = 50
    template_name = "diagnostic/vitreous-body/vitreous-body.html"

    def get_queryset(self):
        queryset = VitreousBody.objects.filter(clinic_id=self.request.user.clinic.pk)
        return queryset


class VitreousBodyCreateView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = VitreousBody
    template_name = 'diagnostic/vitreous-body/vitreous-body-create.html'
    fields = ['title']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.clinic = self.request.user.clinic
        self.object.save()
        return redirect('diagnostic:vitreous-body')


class VitreousBodyUpdateView(AllowedRolesMixin, LoginRequiredMixin, UpdateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = VitreousBody
    template_name = 'diagnostic/vitreous-body/vitreous-body-update.html'
    fields = ['title']
    success_url = '/diagnostic/vitreous-body'


class VitreousBodyDeleteView(AllowedRolesMixin, LoginRequiredMixin, DeleteView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = VitreousBody
    template_name = 'diagnostic/vitreous-body/vitreous-body-delete.html'
    success_url = '/diagnostic/vitreous-body'


class OcularFundusListView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = OcularFundus
    paginate_by = 50
    template_name = "diagnostic/ocular-fundus/ocular-fundus.html"

    def get_queryset(self):
        queryset = OcularFundus.objects.filter(clinic_id=self.request.user.clinic.pk)
        return queryset


class OcularFundusCreateView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = OcularFundus
    template_name = 'diagnostic/ocular-fundus/ocular-fundus-create.html'
    fields = ['title']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.clinic = self.request.user.clinic
        self.object.save()
        return redirect('diagnostic:ocular-fundus')


class OcularFundusUpdateView(AllowedRolesMixin, LoginRequiredMixin, UpdateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = OcularFundus
    template_name = 'diagnostic/ocular-fundus/ocular-fundus-update.html'
    fields = ['title']
    success_url = '/diagnostic/ocular-fundus'


class OcularFundusDeleteView(AllowedRolesMixin, LoginRequiredMixin, DeleteView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = OcularFundus
    template_name = 'diagnostic/ocular-fundus/ocular-fundus-delete.html'
    success_url = '/diagnostic/ocular-fundus'


class DiagnosisListView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Diagnosis
    paginate_by = 50
    template_name = "diagnostic/diagnosis/diagnosis.html"

    def get_queryset(self):
        queryset = Diagnosis.objects.filter(clinic_id=self.request.user.clinic.pk)
        return queryset


class DiagnosisCreateView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Diagnosis
    template_name = 'diagnostic/diagnosis/diagnosis-create.html'
    fields = ['title']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.clinic = self.request.user.clinic
        self.object.save()
        return redirect('diagnostic:diagnosis')


class DiagnosisUpdateView(AllowedRolesMixin, LoginRequiredMixin, UpdateView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Diagnosis
    template_name = 'diagnostic/diagnosis/diagnosis-update.html'
    fields = ['title']
    success_url = '/diagnostic/diagnosis'


class DiagnosisDeleteView(AllowedRolesMixin, LoginRequiredMixin, DeleteView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = Diagnosis
    template_name = 'diagnostic/diagnosis/diagnosis-delete.html'
    success_url = '/diagnostic/diagnosis'


class OphthalmologyStatusCreateView(AllowedRolesMixin, LoginRequiredMixin, View):
    allowed_roles = [ADMINISTRATOR, DOCTOR]

    def get(self, request, come_history_id, *args, **kwargs):
        patients = PatientComeHistory.objects.filter(pk=come_history_id, is_active=True)
        visus = ''
        for patient in patients:
            visus = Visus.objects.filter(patient_come_history=patient)
        form = OphthalmologyStatusForm()
        complains = Complaint.objects.all()
        context = {'form': form, 'patient': patients, "visus": visus, "complains": complains,
                   "come_history_id": come_history_id}
        return render(request, 'diagnostic/doctor.html', context)

    def post(self, request, come_history_id, *args, **kwargs):
        form = OphthalmologyStatusForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                complaints = request.POST.getlist('complaints')
                anamnesis = request.POST.get('anamnesis')
                allergy = request.POST.get('allergy')
                if allergy is None:
                    allergy = False
                else:
                    allergy = True
                eyelids_od = request.POST.getlist('eyelids')
                eyelids_os = request.POST.getlist('eyelids_os')
                eyeball_od = request.POST.getlist('eyeball')
                eyeball_os = request.POST.getlist('eyeball_os')
                conjunctiva_od = request.POST.getlist('conjunctiva')
                conjunctiva_os = request.POST.getlist('conjunctiva_os')
                cornea_od = request.POST.getlist('cornea')
                cornea_os = request.POST.getlist('cornea_os')
                front_camera_od = request.POST.getlist('front_camera')
                front_camera_os = request.POST.getlist('front_camera_os')
                zrachok_od = request.POST.getlist('zrachok')
                zrachok_os = request.POST.getlist('zrachok_os')
                lens_od = request.POST.getlist('lens')
                lens_os = request.POST.getlist('lens_os')
                vitreous_body_od = request.POST.getlist('vitreous_body')
                vitreous_body_os = request.POST.getlist('vitreous_body_os')
                ocular_fundus_od = request.POST.getlist('ocular_fundus')
                hour_indicator_od = request.POST.get('hour_indicator_od')
                ocular_fundus_os = request.POST.getlist('ocular_fundus_os')
                hour_indicator_os = request.POST.get('hour_indicator_os')
                diagnosis = request.POST.getlist('diagnosis')
                is_operation = request.POST.get('is_operation')
                if is_operation is None:
                    is_operation = False
                else:
                    is_operation = True
                o_od = OphthalmologyStatus.objects.create(is_operation=is_operation, allergy=allergy,
                                                          anamnesis=anamnesis, hour_indicator=hour_indicator_od,
                                                          patient_come_history_id=come_history_id,
                                                          doctor_id=request.user.pk)
                if is_operation:
                    patient = User.objects.get(patientcomehistory=come_history_id)
                    patient.is_operation = True
                    patient.save()
                o_od.save()
                o_od.complaints.set(complaints)
                o_od.eyelids.set(eyelids_od)
                o_od.eyeball.set(eyeball_od)
                o_od.conjunctiva.set(conjunctiva_od)
                o_od.cornea.set(cornea_od)
                o_od.front_camera.set(front_camera_od)
                o_od.zrachok.set(zrachok_od)
                o_od.lens.set(lens_od)
                o_od.vitreous_body.set(vitreous_body_od)
                o_od.ocular_fundus.set(ocular_fundus_od)
                o_od.diagnosis.set(diagnosis)

                o_os = OphthalmologyStatus.objects.create(is_operation=is_operation, eye=1, allergy=allergy,
                                                          anamnesis=anamnesis, hour_indicator=hour_indicator_os,
                                                          patient_come_history_id=come_history_id,
                                                          doctor_id=request.user.pk)
                o_os.save()
                o_os.complaints.set(complaints)
                o_os.eyelids.set(eyelids_os)
                o_os.eyeball.set(eyeball_os)
                o_os.conjunctiva.set(conjunctiva_os)
                o_os.cornea.set(cornea_os)
                o_os.front_camera.set(front_camera_os)
                o_os.zrachok.set(zrachok_os)
                o_os.lens.set(lens_os)
                o_os.vitreous_body.set(vitreous_body_os)
                o_os.ocular_fundus.set(ocular_fundus_os)
                o_os.diagnosis.set(diagnosis)
                # a = OphthalmologyStatus.objects.create(complaints=complaints, anamnesis=anamnesis, allergy=allergy,
                #                                        eyelids=eyelids_od, eyeball=eyeball_od,
                #                                        conjunctiva=conjunctiva_od,
                #                                        cornea=cornea_od, front_camera=front_camera_od,
                #                                        zrachok=zrachok_od,
                #                                        lens=lens_od, vitreous_body=vitreous_body_od,
                #                                        ocular_fundus=ocular_fundus_od,
                #                                        hour_indicator=hour_indicator_od,
                #                                        diagnosis=diagnosis, is_operation=is_operation,
                #                                        patient_come_history_id=come_history_id,
                #                                        doctor_id=request.user.pk)
                # b = OphthalmologyStatus.objects.create(complaints=complaints, anamnesis=anamnesis, eye=1,
                #                                        allergy=allergy,
                #                                        eyelids=eyelids_os, eyeball=eyeball_os,
                #                                        conjunctiva=conjunctiva_os,
                #                                        cornea=cornea_os, front_camera=front_camera_os,
                #                                        zrachok=zrachok_os,
                #                                        lens=lens_os, vitreous_body=vitreous_body_os,
                #                                        ocular_fundus=ocular_fundus_os,
                #                                        hour_indicator=hour_indicator_os,
                #                                        diagnosis=diagnosis, is_operation=is_operation,
                #                                        patient_come_history_id=come_history_id,
                #                                        doctor_id=request.user.pk)

                messages.success(request, "Success")
                return redirect('device:add-image', pk=come_history_id)
        else:
            form = OphthalmologyStatusForm()
            context = {'form': form}
            return render(request, 'diagnostic/doctor.html', context)
        return render(request, 'diagnostic/doctor.html')


class OphthalmologyStatusDetailView(AllowedRolesMixin, LoginRequiredMixin, DetailView):
    allowed_roles = [NURSE, ADMINISTRATOR, DOCTOR, RECEPTION]
    model = PatientComeHistory
    template_name = 'diagnostic/full_patient_detail.html'


class OperationView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = User
    paginate_by = 50
    template_name = 'operation/operation-list.html'


class OphthalmologyStatusListNowHave(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DOCTOR]
    model = PatientComeHistory
    template_name = 'doctor/now_patient.html'

    def get_queryset(self):
        queryset = PatientComeHistory.objects.filter(patient__clinic=self.request.user.clinic)
        return queryset

    def get_context_data(self, object_list=None, *args, **kwargs):
        ctx = super(OphthalmologyStatusListNowHave, self).get_context_data(**kwargs)
        for i in self.object_list:
            if i.is_active:
                ctx['visus'] = Visus.objects.filter(patient_come_history=i,
                                                    patient_come_history__is_active=True)
        return ctx
