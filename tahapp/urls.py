from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('needful/', views.needful, name='needful'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
	path('submitLetter', views.submitLetter, name='letter'),
	path('helperChange', views.submitHelperChange, name='helperChange'),
	path('needCare', views.submitNeedCare, name='needCare'),
]
