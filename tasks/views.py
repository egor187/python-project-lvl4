from django.shortcuts import render
from tasks.models import Task, TaskStatus
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.views.generic import edit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _


class ListStatusesView(generic.ListView):
    model = TaskStatus
    template_name = 'statuses_index.html'


class StatusView(generic.DetailView):
    model = TaskStatus


class CreateStatusView(LoginRequiredMixin, SuccessMessageMixin, edit.CreateView):
    model = TaskStatus
    fields = [
        'name',
    ]
    template_name = 'status_create_form.html'
    success_url = reverse_lazy('tasks:statuses_list')
    success_message = _('"%(name)s"-status was successfully created')


class UpdateStatusView(LoginRequiredMixin, SuccessMessageMixin, edit.UpdateView):
    model = TaskStatus
    fields = [
        'name',
    ]
    template_name = 'status_update_form.html'
    success_url = reverse_lazy('tasks:statuses_list')
    success_message = _('"%(name)s"-status was successfully updated')


class DeleteStatusView(LoginRequiredMixin, SuccessMessageMixin, edit.DeleteView):
    model = TaskStatus
    fields = [
        'name',
    ]
    template_name = 'status_delete_form.html'
    success_url = reverse_lazy('tasks:statuses_list')
    success_message = _('status was successfully deleted')

    def delete(self, request, *args, **kwargs):
        try:
            result = super().delete(request, *args, **kwargs)
            if self.success_message:
                messages.success(request, self.success_message)
            return result
        except ProtectedError:
            if self.protected_message:
                messages.error(request, self.protected_message)
            # return redirect(self.protected_url)
            return redirect(self.success_url)


class ListTasksView(generic.ListView):
    model = Task
    template_name = 'tasks_index.html'


class TaskView(generic.DetailView):
    model = Task
    template_name = 'task_view.html'


class CreateTaskView(LoginRequiredMixin, SuccessMessageMixin, edit.CreateView):
    model = TaskStatus
    fields = '__all__'
    template_name = 'task_create_form.html'
    success_url = reverse_lazy('tasks:tasks_list')
    success_message = _('"%(name)s" - task was successfully created')


class UpdateTaskView(LoginRequiredMixin, SuccessMessageMixin, edit.UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'task_update_form.html'
    success_url = reverse_lazy('tasks:task_list')
    success_message = _('"%(name)s" - task was successfully updated')

class DeleteTaskView(LoginRequiredMixin, SuccessMessageMixin, edit.DeleteView):
    template_name = 'task_delete_form.html'
    success_url = reverse_lazy('tasks:task_list')
    success_message = _('task was successfully deleted')