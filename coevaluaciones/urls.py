from django.urls import path, include

from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('', views.landing_page, name='landing_page')
]
