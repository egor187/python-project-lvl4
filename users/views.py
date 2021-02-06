from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from users.models import User
from django.urls import reverse
from django.core.paginator import Paginator


class UserView(generic.DetailView):
    model = User


class ListUserView(generic.ListView):
    model = User
    paginate_by = 10
    template_name = 'user_index.html'

    def listing(request):
        user_list = User.objects.all()
        paginator = Paginator(user_list, 5)
        page_number = request.Get.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'user_index.html', {'page_obj': page_obj})



class CreateUserView(CreateView):
    model = User
    fields = '__all__'
#    success_url = '/users/'


class UpdateUserView(UpdateView):
    model = User
    fields = '__all__'
#    success_url = '/users/'


class DeleteUserView(DeleteView):
    model = User
    success_url = '/users/'
