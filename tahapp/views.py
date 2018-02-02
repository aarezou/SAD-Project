from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm


def index(request):
	print("in index view")
	return render(request, 'tahapp/tmp.html')


def needful(request):
	return render(request, 'tahapp/needful.html')#HttpResponse("Hello, world. You're at the polls index.")


def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			return HttpResponse('login post success ' + str(form.cleaned_data['username']))
		return render(request, 'tahapp/index.html', {'login_failed': True})
	return HttpResponse('login but wtf')


def register(request):
	print("in register view")
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			s = str(form.cleaned_data['username'])
			#s = str(form.cleaned_data['role'])
			return HttpResponse('register post success ' + s)
		return HttpResponse('register post fail')
		#return render(request, 'tahapp/index.html', {'register_failed': True})
	return HttpResponse('register but wtf')

# Create your views here.
