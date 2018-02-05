from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from tahapp.models import Profile, Donor, Needful, Helper, Need, Payment,\
	TnxLetter, ChangeHelper, Achievement, Foundation, Donation, Admin, ChangeInfoRequest


def index(request):
	if request.user.is_authenticated:
		profiles = Profile.objects.filter(user=request.user)
		if profiles.exists():
			profile = profiles[0]
			if profile.role == 'N':
				return redirect('needful_view')
			elif profile.role == 'H':
				return redirect('helper_view')
			elif profile.role == 'D':
				return redirect('donor_view')
			elif profile.role == 'A':
				return redirect('admin_view')
	return render(request, 'tahapp/index.html')


def logout(request):
	auth_logout(request)
	return redirect('index')


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


def needful_view2(request, context):
	needful = get_needful(request)
	if not needful:
		return redirect(index)
	context['payments'] = Payment.objects.filter(need__needful=needful)
	context['needs'] = Need.objects.filter(needful=needful, is_urgent=False, done=False)
	context['profile'] = needful.profile
	return render(request, 'tahapp/needful.html', context)


def needful_view(request):
	return needful_view2(request, {})


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


def change_info(request):
	if request.method == 'POST' and request.user.is_authenticated:
		profiles = Profile.objects.filter(user=request.user)
		if profiles.exists():
			profile = profiles[0]
			if profile.role != 'A':
				first_name = request.POST.get('first_name')
				last_name = request.POST.get('last_name')
				bio = request.POST.get('bio')
				if profile.user.first_name != fn or profile.user.last_name != ln or profile.bio != bio:
					for change in ChangeInfoRequest.objects.filter(profile=profile):
						change.delete()
					ChangeInfoRequest.objects.create(profile=profile, first_name=first_name, last_name=last_name, bio=bio)
	return redirect('index')


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
	context['otherNeedfuls'] = Needful.objects.filter(helper=None, is_verified=True)
	context['profile'] = helper.profile
	return render(request, 'tahapp/helper.html', context)


def helper_view(request):
	return helper_view2(request, {})


def helper_needful_care(request):
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


def helper_needful_info2(request, needful_id, context):
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
	context['needs'] = Need.objects.filter(needful=needful)
	return render(request, 'tahapp/helper_needful_info.html', context)


def helper_needful_info(request, needful_id):
	return helper_needful_info2(request, needful_id, {})


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
				return helper_needful_info2(request, letter.needful.id, {'forward_letter_success': True})
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
				return helper_needful_info2(request, needful_id, context)
	return redirect('index')


def submit_need_helper(request):
	helper = get_helper(request)
	if helper and request.method == 'POST':
		needful_id = request.POST.get('id')
		needfuls = Needful.objects.filter(id=needful_id, helper=helper)
		if needfuls.exists():
			needful = needfuls[0]
			desc = request.POST.get('need_desc')
			value = request.POST.get('need_val')
			temp = request.POST.get('is_urgent')
			is_urgent = True if temp else False
			if value and desc and desc != '':
				Need.objects.create(needful=needful, desc=desc, value=value, is_urgent=is_urgent)
				return helper_needful_info2(request, needful.id, {'submit_need_helper_success': True})
			else:
				return helper_needful_info2(request, needful.id, {'submit_need_helper_failed': True})
	return redirect('index')


def donor_view2(request, context):
	donor = get_donor(request)
	if not donor:
		return redirect('index')
	context['yourNeedfuls'] = Needful.objects.filter(donor=donor)
	context['otherNeedfuls'] = Needful.objects.filter(donor=None, is_verified=True).exclude(helper=None)
	context['payments'] = Payment.objects.filter(donor=donor)
	context['credit'] = donor.credit
	context['profile'] = donor.profile
	return render(request, 'tahapp/donor.html', context)


def donor_view(request):
	return donor_view2(request, {})


def donor_needful_info2(request, needful_id, context):
	donor = get_donor(request)
	if not donor:
		return redirect('index')
	needfuls = Needful.objects.filter(id=needful_id, donor=donor)
	if not needfuls.exists():
		return redirect('index')
	needful = needfuls[0]
	context['needful'] = needful
	context['achievements'] = Achievement.objects.filter(needful=needful)
	context['letters_to_donor'] = TnxLetter.objects.filter(needful=needful, is_to_donor=True, is_forwarded=True)
	context['needs'] = Need.objects.filter(needful=needful)
	return render(request, 'tahapp/donor_needful_info.html', context)


def donor_needful_info(request, needful_id):
	return donor_needful_info2(request, needful_id, {})


def donor_needful_care(request):
	donor = get_donor(request)
	if not donor:
		return redirect('index')
	context = {"other_needfuls_active": True}
	if request.method == 'POST':
		needful_id = request.POST.get('needful')
		needfuls = Needful.objects.filter(id=needful_id)
		if needfuls.exists():
			needful = needfuls[0]
			if (not needful.donor) and needful.helper:
				needful.donor = donor
				needful.save()
				context['needful_care_success'] = True
	return donor_view2(request, context)


def pay_need_donor(request):
	donor = get_donor(request)
	if not donor:
		return redirect('index')
	if request.method == 'POST':
		need_id = request.POST.get('id')
		needs = Need.objects.filter(id=need_id, needful__donor=donor).exclude(needful=None)
		if needs.exists():
			need = needs[0]
			if need.value <= donor.credit:
				donor.credit -= need.value
				donor.save()
				need.done = True
				need.save()
				Payment.objects.create(need=need, donor=donor)
				return donor_needful_info2(request, need.needful.id, {'pay_success': True})
			else:
				return donor_needful_info2(request, need.needful.id, {'pay_failed': True})
	return redirect('index')


def increase_credit(request):
	donor = get_donor(request)
	if not donor:
		return redirect('index')
	if request.method == 'POST':
		context = {'credit_active':True}
		value = int(request.POST.get('value'))
		if value and value > 0:
			donor.credit += value
			donor.save()
			context['credit_success'] = True
		else:
			context['credit_failed'] = True
		return donor_view2(request, context)
	return redirect('index')


def donate(request):
	donor = get_donor(request)
	if not donor:
		return redirect('index')
	if request.method == 'POST':
		context = {'credit_active':True}
		value = int(request.POST.get('value'))
		if value and value > 0:
			if donor.credit >= value:
				foundation = Foundation.objects.get(id=1)
				Donation.objects.create(value=value, donor=donor)
				foundation.credit += value
				foundation.save()
				donor.credit -= value
				donor.save()
				context['donation_success'] = True
			else:
				context['donation_not_enough'] = True
		else:
			context['donation_failed'] = True
		return donor_view2(request, context)
	return redirect('index')


def admin_view2(request, context):
	admin = get_admin(request)
	if not admin:
		return redirect('index')
	context['confirmed_needfuls'] = Needful.objects.filter(is_verified=True)
	context['other_needfuls'] = Needful.objects.filter(is_verified=False)
	context['donations'] = Donation.objects.all()
	context['credit'] = Foundation.objects.all()[0].credit
	context['min_helper'] = Foundation.objects.all()[0].min_needfuls
	context['helpers_num'] = []
	for helper in Helper.objects.all():
		context['helpers_num'].append((helper, Needful.objects.filter(helper=helper).count()))
	return render(request, 'tahapp/admin.html', context)


def admin_view(request):
	return admin_view2(request, {})


def admin_needful_info2(request, needful_id,  context):
	admin = get_admin(request)
	if not admin:
		return redirect('index')
	needfuls = Needful.objects.filter(id=needful_id)
	if not needfuls.exists():
		return redirect('index')
	needful = needfuls[0]
	context['needful'] = needful
	context['achievements'] = Achievement.objects.filter(needful=needful)
	context['needs'] = Need.objects.filter(needful=needful).order_by('done')
	return render(request, 'tahapp/admin_needful_info.html', context)


def admin_needful_info(request, needful_id):
	return admin_needful_info2(request, needful_id, {})


def admin_needful_confirm(request):
	admin = get_admin(request)
	if not admin:
		return redirect('index')
	if request.method == 'POST':
		id = request.POST.get('id')
		if id:
			needfuls = Needful.objects.filter(id=id, is_verified=False)
			if needfuls.exists():
				needful = needfuls[0]
				needful.is_verified = True
				needful.save()
				return admin_view2(request, {'other_needfuls_active': True, 'other_needfuls_success': True})
	return redirect('index')


def pay_need_admin(request):
	admin = get_admin(request)
	if not admin:
		return redirect('index')
	if request.method == 'POST':
		need_id = request.POST.get('id')
		if need_id:
			needs = Need.objects.filter(id=need_id, done=False).exclude(needful=None)
			if needs:
				need = needs[0]
				foundation = Foundation.objects.all()[0]
				if need.value <= foundation.credit:
					foundation.credit -= need.value
					foundation.save()
					need.done = True
					need.save()
					return admin_needful_info2(request, need.needful.id, {'pay_success': True})
				else:
					return admin_needful_info2(request, need.needful.id, {'pay_failed': True})
	return redirect('index')


def active_monthly_pay(request):
	admin = get_admin(request)
	if not admin:
		return redirect('index')
	if request.method == 'POST':
		id = request.POST.get('id')
		needfuls = Needful.objects.filter(id=id, monthly_paid=False)
		if needfuls.exists():
			needful = needfuls[0]
			needful.monthly_paid = True
			needful.save()
			return admin_view2(request, {'confirmed_needfuls_active': True, 'monthly_pay_true_success': True})
	return redirect('index')


def deactive_monthly_pay(request):
	admin = get_admin(request)
	if not admin:
		return redirect('index')
	if request.method == 'POST':
		id = request.POST.get('id')
		needfuls = Needful.objects.filter(id=id, monthly_paid=True)
		if needfuls.exists():
			needful = needfuls[0]
			needful.monthly_paid = False
			needful.save()
			return admin_view2(request, {'confirmed_needfuls_active': True, 'monthly_pay_false_success': True})
	return redirect('index')


def min_helper_change(request):
	admin = get_admin(request)
	if not admin:
		return redirect('index')
	if request.method == 'POST':
		context = {'helpers_active': True}
		value = request.POST.get('min_helper_value')
		if value:
			value = int(value)
			if value >= 0:
				foundation = Foundation.objects.all()[0]
				foundation.min_needfuls = value
				foundation.save()
				context['min_helper_change_success'] = True
			else:
				context['min_helper_change_failed'] = True
		else:
			context['min_helper_change_failed'] = True
		return admin_view2(request, context)
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
		return Helper.objects.filter(profile=profile)[0]
	except Exception:
		return None


def get_donor(request):
	if not request.user.is_authenticated:
		return None
	try:
		profile = Profile.objects.filter(user=request.user)[0]
		return Donor.objects.filter(profile=profile)[0]
	except Exception:
		return None


def get_admin(request):
	if not request.user.is_authenticated:
		return None
	try:
		profile = Profile.objects.filter(user=request.user)[0]
		return Admin.objects.filter(profile=profile)[0]
	except Exception:
		return None
