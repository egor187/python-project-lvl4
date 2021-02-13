from django.shortcuts import render
from tasks.models import Task, TaskStatus
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


class ListStatusesView(generic.ListView):
    model = TaskStatus
    template_name = 'statuses_index.html'



