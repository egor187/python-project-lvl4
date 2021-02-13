from django.shortcuts import render
from tasks.models import Task, TaskStatus
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import edit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _


class ListStatusesView(generic.ListView):
    model = TaskStatus
    template_name = 'statuses_index.html'


class CreateStatusView(LoginRequiredMixin, SuccessMessageMixin, edit.CreateView):
    model = TaskStatus
    fields = [
        'name',
    ]
    template_name = 'status_create_form.html'
    success_url = reverse_lazy('tasks:statuses_list')
    success_message = _('%(name)s-status was successfully created')
