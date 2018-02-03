from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('needful_view/', views.needful_view, name='needful_view'),
	path('needfulinfo/', views.needfulinfo, name='needfulinfo'),
	path('helper/', views.helper, name='helper'),
	path('login/', views.login, name='login'),
	path('logout', views.logout, name='needCare'),
	path('register/', views.register, name='register'),
	path('submitLetter/', views.submitLetter, name='letter'),
	path('helperChange/', views.submitHelperChange, name='helperChange'),
	path('needCare/', views.submitNeedCare, name='needCare'),
]
