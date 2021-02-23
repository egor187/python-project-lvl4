from django.shortcuts import redirect
from tasks.models import Task, TaskStatus
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


class CreateStatusView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    edit.CreateView
):
    model = TaskStatus
    fields = [
        'name',
    ]
    template_name = 'status_create_form.html'
    success_url = reverse_lazy('tasks:statuses_list')
    success_message = _('"%(name)s"-status was successfully created')


class UpdateStatusView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    edit.UpdateView
):
    model = TaskStatus
    fields = [
        'name',
    ]
    template_name = 'status_update_form.html'
    success_url = reverse_lazy('tasks:statuses_list')
    success_message = _('"%(name)s"-status was successfully updated')


class DeleteStatusView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    edit.DeleteView
):
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
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        """ To get acces to filter.qs need to override class_method.
        Call super() method and then assign key 'filter' in
        dict 'context' (for template variable 'filter') and put value
        into it as filter object. Then, by put in template
        <input> with attr 'name' and type 'checkbox' when clicking on
        it 'name' key get its value 'on'. So in this method
        possible to variate what qs will pass to filter object"""
        context = super().get_context_data(*kwargs)
        context['filter'] = TaskFilter(self.request.GET)
        if self.request.GET.get('self_tasks') == "on":
            context['filter'] = TaskFilter(
                self.request.GET,
                queryset=Task.objects.filter(creator=self.request.user)
            )
        return context

# Example with state filter in func-style
# @login_required
# def ListTasksView(request):
#     if request.GET.get("self_tasks") == "on":
#         queryset = Task.objects.filter(creator=request.user)
#     else:
#         queryset = Task.objects.all()
#     f = TaskFilter(request.GET, queryset)
#     return render(request, "tasks_index.html", {"filter": f})


class TaskView(generic.DetailView):
    model = Task
    template_name = 'task_view.html'


class CreateTaskView(LoginRequiredMixin, SuccessMessageMixin, edit.CreateView):
    model = Task
    fields = '__all__'
    template_name = 'task_create_form.html'
    success_url = reverse_lazy('tasks:tasks_list')
    success_message = _('Задача успешно создана')

    # override class-method to achieve auto increment form field
    # "creator" with current autheticated user
    def form_valid(self, form):
        # attribute "user" contain current login user by LoginRequiredMixin
        form.instance.creator = self.request.user
        return super().form_valid(form)


class UpdateTaskView(LoginRequiredMixin, SuccessMessageMixin, edit.UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'task_update_form.html'
    success_url = reverse_lazy('tasks:tasks_list')
    success_message = _('Задача успешно изменена')


class DeleteTaskView(LoginRequiredMixin, SuccessMessageMixin, edit.DeleteView):
    model = Task
    fields = [
        'name'
    ]
    template_name = 'task_delete_form.html'
    success_url = reverse_lazy('tasks:tasks_list')
    success_message = _('Задача успешно удалена')
    protected_message = _("Нельзя удалить задачу, к которой привязана метка")

    def delete(self, request, *args, **kwargs):
        try:
            result = super().delete(request, *args, **kwargs)
            messages.success(request, self.success_message)
            return result
        except Exception:
            messages.error(request, self.protected_message)
        return redirect(self.success_url)
