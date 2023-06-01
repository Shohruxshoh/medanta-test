from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from medanta.mixins import AllowedRolesMixin
from django.views import View
from device.models import DeviceCategory, DeviceImage
from user.models import ADMINISTRATOR, DOCTOR


# Create your views here.

class DeviceImageAddView(AllowedRolesMixin, LoginRequiredMixin, View):
    allowed_roles = [ADMINISTRATOR, DOCTOR]

    def get(self, request, pk, *args, **kwargs):
        categories = DeviceCategory.objects.filter(clinic_id=request.user.clinic)
        context = {"categories": categories, "come_pk": pk}
        return render(request, 'device/device_image_add.html', context)

    def post(self, request, pk, *args, **kwargs):
        categories = DeviceCategory.objects.filter(clinic_id=request.user.clinic)
        for category in categories:
            if request.POST.get(f'true{category.pk}') is not None:
                if request.POST.get(f'{category.name}') != '' and request.POST.get(f'{category.name}1') != "":
                    DeviceImage.objects.create(device_id=category.pk, patient_id=pk,
                                               image=request.FILES.get(f'{category.name}'))
                    DeviceImage.objects.create(device_id=category.pk, patient_id=pk,
                                               image=request.FILES.get(f'{category.name}1'))
                elif request.POST.get(f'{category.name}1') == "":
                    DeviceImage.objects.create(device_id=category.pk, patient_id=pk,
                                               image=request.FILES.get(f'{category.name}'))
                elif request.POST.get(f'{category.name}') == "":
                    DeviceImage.objects.create(device_id=category.pk, patient_id=pk,
                                               image=request.FILES.get(f'{category.name}1'))

        return redirect('diagnostic:detail-optic', pk=pk)
