
from django.contrib import admin
from django.urls import path, include, re_path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    re_path(r'(^P<category_path>.+)/$', views.category_detail, name='category_detail'),
    path('get-address/', views.get_address, name='get_address')
]
