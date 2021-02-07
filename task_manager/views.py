from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView


def index(request):
    return render(request, 'index.html')


class Index(TemplateView):
    template_name = 'index.html'
