from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('needfulv/', views.needfulv, name='needfulv'),
	path('helper/', views.helper, name='helper'),
	path('login/', views.login, name='login'),
	path('logout', views.logout, name='needCare'),
	path('register/', views.register, name='register'),
	path('submitLetter/', views.submitLetter, name='letter'),
	path('helperChange/', views.submitHelperChange, name='helperChange'),
	path('needCare/', views.submitNeedCare, name='needCare'),
]
