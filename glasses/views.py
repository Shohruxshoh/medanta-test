from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from medanta.mixins import AllowedRolesMixin
from django.views import View
from django.views.generic import ListView, DetailView
from diagnostic.models import Visus
from glasses.models import Glass
from user.models import DOCTOR, ADMINISTRATOR, GLASSES


# Create your views here.


class GlassesListView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DOCTOR, GLASSES]
    model = Glass
    template_name = 'glass/glass_list.html'

    def get_queryset(self):
        queryset = Glass.objects.filter(patient__patient__clinic=self.request.user.clinic)
        return queryset


class GlassesListNowView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DOCTOR, GLASSES]
    model = Glass
    template_name = 'glass/glass_list_now.html'

    def get_queryset(self):
        queryset = Glass.objects.filter(patient__patient__clinic=self.request.user.clinic, is_active=True)
        return queryset


class GlassCreateView(AllowedRolesMixin, LoginRequiredMixin, View):
    allowed_roles = [ADMINISTRATOR, DOCTOR, GLASSES]

    def get(self, request, pk, *args, **kwargs):
        visus = Visus.objects.filter(patient_come_history_id=pk, patient_come_history__is_active=True)
        context = {"visus": visus}
        return render(request, 'glass/glass_create.html', context)

    def post(self, request, pk, *args, **kwargs):
        if request.method == "POST":
            sph_od = request.POST.get("sph_od")
            sph_os = request.POST.get("sph_os")
            cyl_od = request.POST.get("cyl_od")
            cyl_os = request.POST.get("cyl_os")
            ax_od = request.POST.get("ax_od")
            ax_os = request.POST.get("ax_os")
            bliz_od = request.POST.get("bliz_od")
            bliz_os = request.POST.get("bliz_os")
            dp = request.POST.get("dp")
            true_bliz = request.POST.get("true_bliz")
            if true_bliz == "false":
                Glass.objects.create(patient_id=pk, sph_od=sph_od, sph_os=sph_os, cyl_od=cyl_od, cyl_os=cyl_os,
                                     ax_od=ax_od, ax_os=ax_os, dp=dp, doctor_id=request.user.pk)
            else:
                Glass.objects.create(patient_id=pk, sph_od=sph_od, sph_os=sph_os, cyl_od=cyl_od, cyl_os=cyl_os,
                                     ax_od=ax_od, ax_os=ax_os, dp=dp, bliz_od=bliz_od, bliz_os=bliz_os,
                                     doctor_id=request.user.pk)
            return redirect("diagnostic:patient-come-now-doctor")


class GlassGiveView(AllowedRolesMixin, LoginRequiredMixin, DetailView):
    allowed_roles = [ADMINISTRATOR, DOCTOR, GLASSES]
    model = Glass
    template_name = 'glass/glass_detail.html'

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            glass = Glass.objects.filter(pk=request.POST.get('object_pk'), is_active=True).last()
            glass.is_active = False
            glass.save()
            return redirect("glasses:glasses-list-now")

    def get_context_data(self, *args, **kwargs):
        context = super(GlassGiveView,
                        self).get_context_data(*args, **kwargs)
        context["pk"] = self.object.pk
        context["visus"] = Visus.objects.filter(patient_come_history__glass=self.object.pk,
                                                patient_come_history__is_active=True)
        return context
