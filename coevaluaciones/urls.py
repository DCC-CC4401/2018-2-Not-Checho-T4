from django.urls import path, include

from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('a', views.landing_page, name='landing_page'),
    path('curso/<curso_id>',views.ficha_curso,name='ficha_curso'),
    path('coevaluacion/<coev_id>',views.ficha_coevaluacion,name='ficha_coevaluacion'),
]
