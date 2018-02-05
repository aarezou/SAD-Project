from django.contrib.auth.models import User
from tahapp.models import Profile, Admin


def update_admins():
	for user in User.objects.filter(is_superuser=True):
		profiles = Profile.objects.filter(user=user)
		if not profiles.exists():
			profile = Profile.objects.create(user=user, role='A')
			Admin.objects.create(profile=profile)