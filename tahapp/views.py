from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from tahapp.models import Profile, Donor, Needful, Helper, Need, Payment, TnxLetter, ChangeHelper, Achievement


def index(request):
	if request.user.is_authenticated:
		profiles = Profile.objects.filter(user=request.user)
		if profiles.exists():
			profile = profiles[0]
			if profile.role == 'N':
				return redirect('needful_view')
			elif profile.role == 'H':
				return redirect('helper_view')
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


def helper_view2(request, context):
	helper = get_helper(request)
	if not helper:
		return redirect('index')
	context['yourNeedfuls'] = Needful.objects.filter(helper=helper)
	print(Needful.objects.filter(helper=helper).count())
	context['otherNeedfuls'] = Needful.objects.filter(helper=None)
	print('did you reach there')
	return render(request, 'tahapp/helper.html', context)


def helper_view(request):
	return helper_view2(request, {})


def neefulCare(request):
	helper = get_helper(request)
	if not helper:
		return redirect('index')
	context = {"other_needfuls_active": True}
	if request.method == 'POST':
		needful_id = request.POST.get('needful')
		needfuls = Needful.objects.filter(id=needful_id)
		if needfuls.exists():
			needful = needfuls[0]
			if not needful.helper:
				needful.helper = helper
				needful.save()
				context['needful_care_success'] = True
	return helper_view2(request, context)


def needfulinfo2(request, needful_id, context):
	helper = get_helper(request)
	if not helper:
		return redirect('index')
	needfuls = Needful.objects.filter(id=needful_id, helper=helper)
	if not needfuls.exists():
		return redirect('index')
	needful = needfuls[0]
	context['needful'] = needful
	context['achievements'] = Achievement.objects.filter(needful=needful)
	context['letters_to_helper'] = TnxLetter.objects.filter(needful=needful, helper=helper, is_to_donor=False)
	context['letters_to_forward'] = TnxLetter.objects.filter(needful=needful, is_to_donor=True, is_forwarded=False)
	return render(request, 'tahapp/needfulinfo.html', context)


def needfulinfo(request, needful_id):
	return needfulinfo2(request, needful_id, {})


def forward_letter(request):
	helper = get_helper(request)
	if helper and request.method == 'POST':
		letter_id = request.POST.get('forward_letter')
		if letter_id:
			letters = TnxLetter.objects.filter(id=letter_id, needful__helper=helper)
			if letters.exists():
				letter = letters[0]
				letter.is_forwarded = True
				letter.save()
				return needfulinfo2(request, letter.needful.id, {'forward_letter_success': True})
	return redirect('index')


def submit_achievement(request):
	helper = get_helper(request)
	if helper and request.method == 'POST':
		needful_id = request.POST.get('id')
		if needful_id:
			needfuls = Needful.objects.filter(id=needful_id, helper=helper)
			if needfuls.exists():
				desc = request.POST.get('achievement_submit')
				context = {}
				if desc and desc != '':
					needful = needfuls[0]
					Achievement.objects.create(needful=needful, desc=desc)
					context['submit_achievement_success'] = True
				else:
					context['submit_achievement_failed'] = True
				return needfulinfo2(request, needful_id, context)
	return redirect('index')


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


def get_helper(request):
	if not request.user.is_authenticated:
		return None
	try:
		profile = Profile.objects.filter(user=request.user)[0]
		helper = Helper.objects.filter(profile=profile)[0]
		return helper
	except Exception:
		return None
