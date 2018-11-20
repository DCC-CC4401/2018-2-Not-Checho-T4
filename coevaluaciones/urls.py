from django.urls import path, include

from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('a', views.landing_page, name='landing_page'),
    path('',views.ficha_curso,name='ficha_curso'),
    path('ficha_coevaluacion/<coev_id>',views.ficha_coevaluacion,name='ficha_coevaluacion'),
    path('subir_coevaluacion/<coev_id>', views.subir_coevaluacion, name='subir_coevaluacion'),
]
