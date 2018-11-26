from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('', views.landing_page, name='landing_page'),
    path('ficha_curso/<curso_id>', views.ficha_curso, name='ficha_curso'),
    path('ficha_curso/<curso_id>/<mensaje>', views.ficha_curso, name='ficha_curso'),
    path('ficha_coevaluacion/<coev_id>', views.ficha_coevaluacion, name='ficha_coevaluacion'),
    path('subir_coevaluacion/<coev_id>', views.subir_coevaluacion, name='subir_coevaluacion'),
    path('perfil', views.perfil, name="perfil"),
    path('cambiarContra', views.cambiarContra, name="cambiarContra"),
    path('agregar_coevaluacion/<curso_id>',views.agregar_coevaluacion,name='agregar_coevaluacion'),
    path('publicar_coevaluacion/<curso_id>/<coev_id>',views.publicar_coevaluacion,name='publicar_coevaluacion'),
]
