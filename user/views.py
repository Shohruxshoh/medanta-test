from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import RedirectView, CreateView, UpdateView, DeleteView
from django.contrib.auth import logout
from medanta.mixins import AllowedRolesMixin
from user.forms import SignUpForm, EmployeeUpdateForm
from user.models import (ADMINISTRATOR, DIRECTOR, NURSE, DOCTOR, RECEPTION, ACCOUNTANT, MANAGER, PATIENT, Clinic, User,
                         PARTNER)
from django.views.generic import ListView


# Create your views here.

class RedirectToHomeView(AllowedRolesMixin, RedirectView):
    allowed_roles = [ADMINISTRATOR, DIRECTOR, NURSE, DOCTOR, RECEPTION, ACCOUNTANT, MANAGER, PATIENT]

    def get(self, request, *args, **kwargs):
        if request.user.role == ADMINISTRATOR:
            return redirect(reverse_lazy('user:index'))


class CreateEmployeeView(AllowedRolesMixin, LoginRequiredMixin, CreateView):
    allowed_roles = [ADMINISTRATOR, DIRECTOR]
    model = User
    form_class = SignUpForm
    template_name = 'reception/director/employee/create_employee.html'
    success_url = '/user/employee-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.clinic = self.request.user.clinic
        self.object.phone = str(self.object.phone).replace(" ", '')
        self.object.username = str(self.object.first_name) + str(self.object.phone)

        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')


class EmployeesListView(AllowedRolesMixin, LoginRequiredMixin, ListView):
    allowed_roles = [ADMINISTRATOR, DIRECTOR]
    template_name = 'reception/director/employee/employees.html'
    model = User
    paginate_by = 50

    def get_queryset(self):
        queryset = User.objects.filter(clinic=self.request.user.clinic).exclude(role=PATIENT).exclude(
            role=ADMINISTRATOR).exclude(role=PARTNER)
        return queryset


class EmployeeUpdateView(AllowedRolesMixin, LoginRequiredMixin, UpdateView):
    allowed_roles = [ADMINISTRATOR, DIRECTOR]
    model = User
    form_class = EmployeeUpdateForm
    template_name = 'reception/director/employee/employee-update.html'
    success_url = '/user/employee-list'


class EmployeeDeleteView(AllowedRolesMixin, LoginRequiredMixin, DeleteView):
    allowed_roles = [ADMINISTRATOR, DIRECTOR]
    model = User
    template_name = 'reception/director/employee/employee-delete.html'
    success_url = '/user/employee-list'


def user_signup(request):
    regions = Region.objects.all()

    context = {
        'regions': regions,
    }
    return render(request, f'account/signup.html', context)


@login_required
def user_logout(request):
    logout(request)
    return redirect('/')


def handler404(request, exception):
    return render(request, '_parts/404.html', status=404)


def handler403(request, exception):
    return render(request, '_parts/403.html', status=403)
