from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('needful/', views.needful, name='needful'),
    path('submitReq/', views.submitRequest, name='submitReq'),
]
