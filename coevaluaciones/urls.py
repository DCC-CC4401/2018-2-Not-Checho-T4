from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('', views.landing_page, name='landing_page'),
    path('ficha_curso/<curso_id>', views.ficha_curso, name='ficha_curso'),
    path('ficha_coevaluacion/<coev_id>', views.ficha_coevaluacion, name='ficha_coevaluacion'),
    path('subir_coevaluacion/<coev_id>', views.subir_coevaluacion, name='subir_coevaluacion'),
    path('perfil', views.perfil, name="perfil")
]
