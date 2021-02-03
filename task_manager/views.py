from django.http import HttpResponse
from django.views.generic.base import TemplateView


def index(request):
    return HttpResponse("Welcome to last fourth HEXLET project!")


class Index(TemplateView):
    template_name = 'index.html'
