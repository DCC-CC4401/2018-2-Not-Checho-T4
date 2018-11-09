from django.urls import path, include

from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('', views.landing_page, name='landing_page'),
    path('ficha_curso/<curso_id>',views.ficha_curso,name='ficha_curso'),
    path('ficha_coevaluacion/<coev_id>',views.ficha_coevaluacion,name='ficha_coevaluacion'),
]
