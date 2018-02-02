from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Donor(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	credit = models.IntegerField()

class Helper(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)

class Needful(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	donor = models.ForeignKey(Donor, on_delete=models.SET_NULL, blank=True, null=True)
	helper = models.ForeignKey(Helper, on_delete=models.SET_NULL, blank=True, null=True)
	is_verified = models.BooleanField(default=False)

class Need(models.Model):
	needful = models.ForeignKey(Needful, on_delete=models.SET_NULL, blank=True, null=True)
	value = models.IntegerField()
	desc = models.CharField(max_length=100)
	is_urgent = models.BooleanField()
	done = models.BooleanField()

class Payment(models.Model):
	need = models.ForeignKey(Need, on_delete=models.CASCADE)
	date = models.DateTimeField()

class TnxLetter(models.Model):
	needful = models.ForeignKey(Needful, on_delete=models.SET_NULL, blank=True, null=True)
	donor = models.ForeignKey(Donor, on_delete=models.SET_NULL, blank=True, null=True)
	helper = models.ForeignKey(Helper, on_delete=models.SET_NULL, blank=True, null=True)
	context = models.CharField(max_length=100)

