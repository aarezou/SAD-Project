from django.db import models
from django.contrib.auth.models import User
from .choices import ROLE_CHOICES


class Foundation(models.Model):
	credit = models.IntegerField(default=0)
	min_needfuls = models.IntegerField(default=0)


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	role = models.CharField(max_length=1, choices=ROLE_CHOICES)
	bio = models.CharField(max_length=100, default='')


class Donor(models.Model):
	profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
	credit = models.IntegerField(default=0)


class Helper(models.Model):
	profile = models.OneToOneField(Profile, on_delete=models.CASCADE)


class Needful(models.Model):
	profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
	donor = models.ForeignKey(Donor, on_delete=models.SET_NULL, blank=True, null=True)
	helper = models.ForeignKey(Helper, on_delete=models.SET_NULL, blank=True, null=True)
	is_verified = models.BooleanField(default=False)
	monthly_paid = models.BooleanField(default=False)


class Admin(models.Model):
	profile = models.OneToOneField(Profile, on_delete=models.CASCADE)


class Need(models.Model):
	needful = models.ForeignKey(Needful, on_delete=models.SET_NULL, blank=True, null=True)
	value = models.IntegerField()
	desc = models.CharField(max_length=100)
	is_urgent = models.BooleanField(default=False)
	done = models.BooleanField(default=False)


class Payment(models.Model):
	need = models.ForeignKey(Need, on_delete=models.CASCADE)
	donor = models.ForeignKey(Donor, on_delete=models.SET_NULL, null=True)
	date = models.DateTimeField(auto_now_add=True)


class Donation(models.Model):
	donor = models.ForeignKey(Donor, on_delete=models.SET_NULL, null=True)
	value = models.IntegerField()
	date = models.DateTimeField(auto_now_add=True)


class TnxLetter(models.Model):
	needful = models.ForeignKey(Needful, on_delete=models.SET_NULL, blank=True, null=True)
	donor = models.ForeignKey(Donor, on_delete=models.SET_NULL, blank=True, null=True)
	helper = models.ForeignKey(Helper, on_delete=models.SET_NULL, blank=True, null=True)
	context = models.CharField(max_length=100)
	is_to_donor = models.BooleanField(default=False)
	is_forwarded = models.BooleanField(default=False)


class ChangeHelper(models.Model):
	needful = models.ForeignKey(Needful, on_delete=models.CASCADE, blank=True, null=True)
	desc = models.CharField(max_length=100)


class Achievement(models.Model):
	needful = models.ForeignKey(Needful, on_delete=models.CASCADE)
	desc = models.CharField(max_length=100)


class ChangeInfoRequest(models.Model):
	profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	bio = models.CharField(max_length=100)
	date = models.DateTimeField(auto_now_add=True)
