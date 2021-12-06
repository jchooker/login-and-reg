from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add_registrant', views.add_registrant),
    path('add_success', views.add_success),
    path('login_attempt', views.login_attempt),
    path('logged_in', views.logged_in),
    path('log_out', views.logout)
]
