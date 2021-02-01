from django.http import HttpResponse


def index(request):
    return HttpResponse("Welcome to last fourth HEXLET project!")
