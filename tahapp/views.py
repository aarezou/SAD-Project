from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile, Donor, Needful, Helper


def index(request):
	if request.user.is_authenticated:
		return needful(request)
	return render(request, 'tahapp/index.html')


def needful(request):
	return render(request, 'tahapp/needful.html')


def login(request):
	if request.user.is_authenticated:
		return index(request)
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user:
				return index(request)
		return render(request, 'tahapp/index.html', {'login_failed': True})
	return index(request)


def register(request):
	if request.user.is_authenticated:
		return index(request)
	context = {'register_active': True}
	if request.method == 'POST':
		role = request.POST.get('role')
		password_repeat = request.POST.get('password_repeat')
		form = RegisterForm(request.POST)
		if not role:
			context['no_role'] = True
		elif password_repeat and form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']

			if User.objects.filter(username=username).exists():
				context['username_taken'] = True
			elif password != password_repeat:
				context['unequal_passwords'] = True
			else:
				user = User.objects.create_user(username=username, email=email, password=password)
				profile = Profile.objects.create(user=user, role=role[0])
				if role[0] == 'H':
					Helper.objects.create(profile=profile)
				elif role[0] == 'D':
					Donor.objects.create(profile=profile)
				else:
					Needful.objects.create(profile=profile)
				context['success'] = True
		else:
			context['form_not_valid'] = True
	return render(request, 'tahapp/index.html', context)

def submitLetter(request):
	return HttpResponse("Hello, world. You're at the polls index.")


def submitHelperChange(request):
	return HttpResponse("Hello, world. You're at the polls index.")


def submitNeedCare(request):
	return HttpResponse("Hello, world. You're at the polls index.")

