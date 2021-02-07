from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from users.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.core.paginator import Paginator
from .forms import CustomUserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
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


class CreateUserView(CreateView, FormView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:user_list')


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy('users:profile')
    template_name = 'profile.html'



# class CreateUserView(CreateView, FormView):
#     model = CustomUser
#     # Форма для регистрации нового пользователя в системе аутентификации
#     form_class = UserCreationForm
# #    fields = '__all__'
#     success_url = '/users/'

#    def add_user_into_auth(self):
#        user = User.objects.create_user(self.object)
#        user.save()
#        return user


class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    fields = [
        'username',
        'first_name',
        'last_name',
        'email',
    ]
    # form_class = CustomUserCreationForm
    not_owner_redirect_url = reverse_lazy('users:user_list')
    not_owner_message = 'You are not permitted to this action'
    success_message = 'Profile updated'


    def dispatch(self, request, *args, **kwargs):
        if kwargs['pk'] != request.user.pk:
            if self.not_owner_message:
                messages.error(request, self.not_owner_message)
            return redirect(self.not_owner_redirect_url)
        return super().dispatch(request, *args, **kwargs)



class DeleteUserView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = CustomUser
    success_url = '/users/'

    not_owner_redirect_url = reverse_lazy('users:user_list')
    not_owner_message = 'You are not permitted to this action'
    success_message = 'Profile deleted'

    def handle_no_permission(self):
        messages.error(self.request, self.unauthorized_user_message)
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
