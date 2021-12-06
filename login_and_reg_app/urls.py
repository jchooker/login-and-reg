from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add_registrant', views.add_registrant),
    path('add_success', views.add_success),
    path('login_success', views.login_success)
]
