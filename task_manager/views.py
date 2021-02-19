from django.shortcuts import render
from django.views.generic.base import TemplateView


def index(request):
    car = request.session['my_car'] = 'bmw'
    visits = request.session.get('visits', 0)
    request.session['visits'] = visits + 1
    return render(
        request,
        'index.html',
        context={'car': car, 'visits': visits}
    )


class Index(TemplateView):
    template_name = 'index.html'

    # Reassigned super method to get context_var - "num_visits"
    # with number of connections from session.
    def get_context_data(self, **kwargs):
        # Access to sessions in class-based views available from
        # request object, which constructs by .as_view() in
        # self.request. That's why access to self.request in
        # class-based views available also in others method of
        # class-based views, not only from get_context_data
        visits = self.request.session.get('visits', 0)
        self.request.session['visits'] = visits + 1
        num_visits = self.request.session['visits'] = visits + 1
        context = super().get_context_data(**kwargs)
        context['num_visits'] = num_visits
        return context

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# INSERT USERS_LOGIN/LOGOUT INTO TASK_MANAGER
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.translation import gettext as _


class LoginUserView(SuccessMessageMixin, LoginView):
    success_message = _('%(username)s was successfully login')


class LogoutUserView(SuccessMessageMixin, LogoutView):
    success_message = _('%(username)s was successfully logout')

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# INSERT USERS:LABELS INTO TASK_MANAGER
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
    success_url = reverse_lazy('labels_list')
    success_message = _('Метка успешно создана')


class UpdateLabelView(LoginRequiredMixin, SuccessMessageMixin, edit.UpdateView):
    model = Label
    fields = '__all__'
    template_name = 'label_update_form.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Метка успешно изменена')


class DeleteLabelView(LoginRequiredMixin, SuccessMessageMixin, edit.DeleteView):
    model = Label
    template_name = 'label_delete_form.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Метка успешно удалена')
    protected_message = _("You don't have permissions to delete this label")

    # def delete(self, request, *args, **kwargs):
    #     try:
    #         result = super().delete(request, *args, **kwargs)
    #         messages.success(request, self.success_message)
    #         return result
    #     except Exception:
    #         messages.error(request, self.protected_message)
    #     return redirect(self.success_url)


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# INSERT USERS:LABELS INTO TASK_MANAGER
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
    success_url = reverse_lazy('statuses_list')
    success_message = _('Статус успешно создан')


class UpdateStatusView(LoginRequiredMixin, SuccessMessageMixin, edit.UpdateView):
    model = TaskStatus
    fields = [
        'name',
    ]
    template_name = 'status_update_form.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Статус успешно изменен')


class DeleteStatusView(LoginRequiredMixin, SuccessMessageMixin, edit.DeleteView):
    model = TaskStatus
    fields = [
        'name',
    ]
    template_name = 'status_delete_form.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Статус успешно удален')
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