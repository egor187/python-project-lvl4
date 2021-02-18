from django.shortcuts import render, redirect
from tasks.models import Task, TaskStatus, Label
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.views.generic import edit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from tasks.filters import TaskFilter


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
    protected_message = _("You don't have permissions to delete this status")

    # Override class method for add messages.
    def delete(self, request, *args, **kwargs):
        try:
            result = super().delete(request, *args, **kwargs)
            if self.success_message:
                messages.success(request, self.success_message)
            return result
        except Exception:
            if self.protected_message:
                messages.error(request, self.protected_message)
            return redirect(self.success_url)


class ListTasksView(generic.ListView):
    model = Task
    template_name = 'tasks_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        context['filter'] = TaskFilter(self.request.GET)
        return context


class TaskView(generic.DetailView):
    model = Task
    template_name = 'task_view.html'


class CreateTaskView(LoginRequiredMixin, SuccessMessageMixin, edit.CreateView):
    model = Task
    fields = '__all__'
    template_name = 'task_create_form.html'
    success_url = reverse_lazy('tasks:tasks_list')
    success_message = _('"%(name)s" - task was successfully created')

    # override class-method to achieve auto increment form field "creator" with current autheticated user
    def form_valid(self, form):
        form.instance.creator = self.request.user # attribute "user" contain current login user by LoginRequiredMixin
        return super().form_valid(form)

class UpdateTaskView(LoginRequiredMixin, SuccessMessageMixin, edit.UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'task_update_form.html'
    success_url = reverse_lazy('tasks:tasks_list')
    success_message = _('"%(name)s" - task was successfully updated')

class DeleteTaskView(LoginRequiredMixin, SuccessMessageMixin, edit.DeleteView):
    model = Task
    fields = [
        'name'
    ]
    template_name = 'task_delete_form.html'
    success_url = reverse_lazy('tasks:tasks_list')
    success_message = _('task was successfully deleted')
    protected_message = _("You don't have permissions to delete this status")

    def delete(self, request, *args, **kwargs):
        try:
            result = super().delete(request, *args, **kwargs)
            messages.success(request, self.success_message)
            return result
        except Exception:
            messages.error(request, self.protected_message)
        return redirect(self.success_url)


class ListLabelsView(generic.ListView):
    model = Label
    template_name = 'labels_index.html'


class LabelView(generic.DetailView):
    model = Label
    template_name = 'label_view.html'


class CreateLabelView(LoginRequiredMixin, SuccessMessageMixin, edit.CreateView):
    model = Label
    fields = '__all__'
    template_name = 'label_create_form.html'
    success_url = reverse_lazy('tasks:labels_list')
    success_message = _('"%(name)s" - label was successfully created')

class UpdateLabelView(LoginRequiredMixin, SuccessMessageMixin, edit.UpdateView):
    model = Label
    fields = '__all__'
    template_name = 'label_update_form.html'
    success_url = reverse_lazy('tasks:labels_list')
    success_message = _('"%(name)s" - label was successfully updated')

class DeleteLabelView(LoginRequiredMixin, SuccessMessageMixin, edit.DeleteView):
    model = Label
    template_name = 'label_delete_form.html'
    success_url = reverse_lazy('tasks:labels_list')
    success_message = _('label was successfully deleted')
    protected_message = _("You don't have permissions to delete this label")

    # def delete(self, request, *args, **kwargs):
    #     try:
    #         result = super().delete(request, *args, **kwargs)
    #         messages.success(request, self.success_message)
    #         return result
    #     except Exception:
    #         messages.error(request, self.protected_message)
    #     return redirect(self.success_url)