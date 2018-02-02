from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User

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
	context = {'register_active': True}
	if request.method == 'POST':
		role = request.POST.get('role')
		password_repeat = request.POST.get('password_repeat')
		form = RegisterForm(request.POST)
		if not role:
			context['no_role'] = True
		elif form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']

			if User.objects.filter(username=username).exists():
				context['username_taken'] = True
			elif password != password_repeat:
				context['unequal_passwords'] = True
			else:
				User.objects.create_user(username=username, email=email, password=password)
				context['success'] = True
		else:
			context['form_not_valid'] = True
	return render(request, 'tahapp/index.html', context)

# Create your views here.
