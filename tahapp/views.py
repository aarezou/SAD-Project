from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm


def index(request):
	return render(request, 'tahapp/index.html')


def needful(request):
	return render(request, 'tahapp/needful.html')#HttpResponse("Hello, world. You're at the polls index.")


def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			return HttpResponse('login post success ' + str(form.cleaned_data['username']))
		return render(request, 'tahapp/index.html')
	return HttpResponse('login but wtf')


def register(request):
	return HttpResponse("Hello, world. You're at the polls index.")

# Create your views here.
