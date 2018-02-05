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
	path('increase_credit/', views.increase_credit, name='increase_credit'),
	path('donate/', views.donate, name='donate'),
	path('admin_view/', views.admin_view, name='admin_view'),
	path('admin_needful_confirm/', views.admin_needful_confirm, name='admin_needful_confirm'),
	path('admin_needful_info/<int:needful_id>/', views.admin_needful_info, name='admin_needful_info'),
	path('pay_need_admin/', views.pay_need_admin, name='pay_need_admin'),
	path('active_monthly_pay/', views.active_monthly_pay, name='active_monthly_pay'),
	path('deactive_monthly_pay/', views.deactive_monthly_pay, name='deactive_monthly_pay'),
	path('min_helper_change/', views.min_helper_change, name='min_helper_change'),
]
