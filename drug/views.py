from django.shortcuts import render, redirect
from django.views.generic import ListView
from drug.models import Drugs
from medanta.mixins import AllowedRolesMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView


# Create your views here.


class DrugListView(LoginRequiredMixin, ListView):
    model = Drugs
    template_name = 'drug/drug_list.html'


class DrugCreateView(LoginRequiredMixin, CreateView):
    model = Drugs
    fields = ['name', 'date', 'clinic']
    template_name = 'drug/drug_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.clinic = self.request.user.clinic
        self.object.save()
        return redirect('drug:drugs')


class DrugUpdateView(LoginRequiredMixin, UpdateView):
    model = Drugs
    fields = ['name', 'date']
    template_name = 'drug/drug_update.html'
    success_url = '/drug'

class DrugDeleteView(LoginRequiredMixin, DeleteView):
    model = Drugs
    template_name = 'drug/drug-delete.html'
    success_url = '/drug'
