from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('needful/', views.needful, name='needful'),
    path('login/', views.login, name='login'),
    path('register/', views.login, name='register'),
]
