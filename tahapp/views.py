from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm


def index(request):
    return render(request, 'tahapp/index.html')


def needful(request):
    return render(request, 'tahapp/needful.html')#HttpResponse("Hello, world. You're at the polls index.")


def login(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def register(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# Create your views here.
