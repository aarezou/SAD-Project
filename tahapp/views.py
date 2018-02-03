from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from tahapp.models import Profile, Donor, Needful, Helper, Need, Payment, TnxLetter, ChangeHelper


def index(request):
	if request.user.is_authenticated:
		return redirect('needful_view')
	return render(request, 'tahapp/index.html')


def needful_view2(request, context):
	needful = get_needful(request)
	if not needful:
		return redirect(index)
	context['payments'] = Payment.objects.filter(need__needful=needful)
	context['needs'] = Need.objects.filter(needful=needful, is_urgent=False)
	return render(request, 'tahapp/needful.html', context)


def needful_view(request):
	return needful_view2(request, {})


def login(request):
	if request.user.is_authenticated:
		return redirect('index')
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user:
				auth_login(request, user)
				return redirect('index')
		return render(request, 'tahapp/index.html', {'login_failed': True})
	return redirect('index')


def register(request):
	if request.user.is_authenticated:
		return redirect('index')
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
	needful = get_needful(request)
	if not needful:
		return redirect('index')
	context = {'submit_letter_active': True}
	if request.method == 'POST':
		receiver = request.POST.get('receiver')
		txt = request.POST.get('txt')
		if txt and receiver and txt != '':
			TnxLetter.objects.create(needful=needful, donor=needful.donor, helper=needful.helper, context=txt, is_to_donor=(receiver=="Donor"))
			context['submit_letter_success'] = True
		else:
			context['submit_letter_failed'] = True
	return needful_view2(request, context)


def submitHelperChange(request):
	needful = get_needful(request)
	if not needful:
		return redirect('index')
	context = {"helper_change_active": True}
	if request.method == 'POST':
		txt = request.POST.get('description')
		if txt and txt != '':
			ChangeHelper.objects.create(needful=needful, desc=txt)
			context["helper_change_success"] = True
		else:
			context["helper_change_failed"] = True
	return needful_view2(request, context)


def submitNeedCare(request):
	needful = get_needful(request)
	if not needful:
		return redirect('index')
	context = {"need_care_active": True}
	if request.method == 'POST':
		need_id = request.POST.get('need')
		needs = Need.objects.filter(id=need_id, needful=needful)
		if needs.exists():
			need = needs[0]
			need.is_urgent = True
			need.save()
			context['need_care_success'] = True
	return needful_view2(request, context)


def helper(request):
	return render(request, 'tahapp/helper.html')


def logout(request):
	auth_logout(request)
	return redirect('index')


def get_needful(request):
	if not request.user.is_authenticated:
		return None
	try:
		profile = Profile.objects.filter(user=request.user)[0]
		needful = Needful.objects.filter(profile=profile)[0]
		return needful
	except Exception:
		return None
