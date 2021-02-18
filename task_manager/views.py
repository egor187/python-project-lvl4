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


from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.translation import gettext as _

class LoginUserView(SuccessMessageMixin, LoginView):
    success_message = _('%(username)s was successfully login')


class LogoutUserView(SuccessMessageMixin, LogoutView):
    success_message = _('%(username)s was successfully logout')