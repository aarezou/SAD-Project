from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm


def index(request):
	print("in index view")
	return render(request, 'tahapp/index.html')


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
		role = request.POST.get('role')
		form = RegisterForm(request.POST)
		if role and form.is_valid():
			s = str(form.cleaned_data['username'])
			return HttpResponse('register post success ' + s + ' ' + role)
		return render(request, 'tahapp/index.html', {'register_failed': True})
	return HttpResponse('register but wtf')

# Create your views here.
