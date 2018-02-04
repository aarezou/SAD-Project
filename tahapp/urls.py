from django.urls import path

from . import views


urlpatterns = [
	path('', views.index, name='index'),
	path('needful_view/', views.needful_view, name='needful_view'),
	path('helper_needful_info/<int:needful_id>/', views.helper_needful_info, name='helper_needful_info'),
	path('helper_view/', views.helper_view, name='helper_view'),
	path('login/', views.login, name='login'),
	path('logout', views.logout, name='needCare'),
	path('register/', views.register, name='register'),
	path('submitLetter/', views.submitLetter, name='letter'),
	path('helperChange/', views.submitHelperChange, name='helperChange'),
	path('needCare/', views.submitNeedCare, name='needCare'),
	path('helper_needful_care/', views.helper_needful_care, name='helper_needful_care'),
	path('submit_achievement/', views.submit_achievement, name='submit_achievement'),
	path('forward_letter/', views.forward_letter, name='forward_letter'),
	path('submit_need_helper/', views.submit_need_helper, name='submit_need_helper'),
	path('donor_view/', views.donor_view, name='donor_view'),
	path('pay_need_donor/', views.pay_need_donor, name='pay_need_donor'),
	path('donor_needful_care/', views.donor_needful_care, name='donor_needful_care'),
	path('donor_needful_info/<int:needful_id>/', views.donor_needful_info, name='donor_needful_info'),
]
