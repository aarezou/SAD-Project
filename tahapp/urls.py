from django.urls import path

from . import views


urlpatterns = [
	path('', views.index, name='index'),
	path('needful_view/', views.needful_view, name='needful_view'),
	path('needfulinfo/<int:needful_id>/', views.needfulinfo, name='needfulinfo'),
	path('helper_view/', views.helper_view, name='helper_view'),
	path('login/', views.login, name='login'),
	path('logout', views.logout, name='needCare'),
	path('register/', views.register, name='register'),
	path('submitLetter/', views.submitLetter, name='letter'),
	path('helperChange/', views.submitHelperChange, name='helperChange'),
	path('needCare/', views.submitNeedCare, name='needCare'),
	path('needfulCare/', views.neefulCare, name='needfulCare'),
	path('submit_achievement/<int:needful_id>/', views.submit_achievement, name='submit_achievement'),
	path('forward_letter/', views.forward_letter, name='forward_letter'),
]
