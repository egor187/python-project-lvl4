from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from users.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from .forms import CustomUserUpdateForm
from .forms import CustomUserCreationForm

class ListUserView(generic.ListView):
    model = CustomUser
    paginate_by = 10
    template_name = 'user_index.html'

    def listing(request):
        user_list = CustomUser.objects.all()
        paginator = Paginator(user_list, 5)
        page_number = request.Get.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'user_index.html', {'page_obj': page_obj})


class UserView(generic.DetailView):
    model = CustomUser


class CreateUserView(SuccessMessageMixin, CreateView, FormView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:user_list')
    success_message = _('%(username)s was successfully created')


# class LoginUserView(SuccessMessageMixin, LoginView):
#     success_message = _('%(username)s was successfully login')
#
#
# class LogoutUserView(SuccessMessageMixin, LogoutView):
#     success_message = _('%(username)s was successfully logout')


class PasswordChangeUserView(SuccessMessageMixin, PasswordChangeView):
    success_message = _('Password was successfully changed')
    success_url = reverse_lazy('users:user_list')


class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    fields = [
        'username',
        'first_name',
        'last_name',
        'email',
    ]

    # form_class = CustomUserUpdateForm

    not_owner_redirect_url = reverse_lazy('users:user_list')
    not_owner_message = _('You are not permitted to this action')
    success_message = _('Profile updated')

    # Redirect from update_form if pk in request different from page where update_form form
    # URLdispatcher capture <int:pk> as keyword arg (**kwargs) for pass to view (UpdateUserView). So, you may
    # compare value of kwarg['pk'] (which made by generic ListView from a model in template user_index.html)
    # with current pk of user in request object - django auth middware add object user to request, so "request.user.pk"
    # contains pk of currently authenticated user.
    def dispatch(self, request, *args, **kwargs):
        if kwargs['pk'] != request.user.pk:
            messages.error(request, self.not_owner_message)
            return redirect(self.not_owner_redirect_url)
        return super().dispatch(request, *args, **kwargs)



class DeleteUserView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = CustomUser
    success_url = '/users/'

    not_owner_redirect_url = reverse_lazy('users:user_list')
    not_owner_message = _('You are not owner for this action')
    no_permissions_message = _('You are not permitted to this action')
    success_message = 'Profile deleted'

    def handle_no_permission(self):
        messages.error(self.request, self.no_permissions_message)
        return super().handle_no_permission()

    def dispatch(self, request, *args, **kwargs):
        if kwargs['pk'] != request.user.pk:
            if self.not_owner_message:
                messages.error(request, self.not_owner_message)
            return redirect(self.not_owner_redirect_url)
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            result = super().delete(request, *args, **kwargs)
            if self.success_message:
                messages.success(request, self.success_message)
            return result
        except ProtectedError:
            if self.protected_message:
                messages.error(request, self.protected_message)
            return redirect(self.protected_url)
