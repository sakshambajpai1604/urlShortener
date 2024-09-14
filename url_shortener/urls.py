
from django.contrib import admin
from django.urls import path 
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('shorten/', views.shorten_url, name='shorten_url'),
    path('<str:short_url>/', views.redirect_original_url, name='redirect_original_url'),
]