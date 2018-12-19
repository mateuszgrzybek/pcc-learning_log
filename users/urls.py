"""Definiuje wzorce URL dla użytkowników"""

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout

from . import views

urlpatterns = [
    # Strona logowania
    url(r'^login/$',
     auth_views.LoginView.as_view(template_name='users/login.html'),
     name='login'),

     # Strona wylogowywania
     url(r'^logout/$', views.logout_view, name='logout'),

     # Strona rejestracji
     url(r'^register/$', views.register, name='register'),
]
