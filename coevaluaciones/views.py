from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Curso, Equipo, Roles, PersonaEquipo, Preguntas, Coevaluacion, Resultado, CoevEstud

def login_user(request):
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    return render(request, "coevaluaciones/login.html", {})


@login_required(login_url='/login')
def landing_page(request):
    return render(request, "coevaluaciones/home-vista-alumno.html", {})


@login_required(login_url='/login')
def ficha_curso(request,curso_id):
    user = request.user
    #curso = Curso.objects.get(id=curso_id)
    curso = Curso.objects.get(nombre="Ingenieria de Software", codigo="CC4401", seccion=2,anho=2018,semestre=1)
    roli = Roles.objects.get(user=user,curso=curso)
    if roli.rol=="Alumno":
        coevs = Coevaluacion.objects.filter(curso=curso).order_by('-fin')
        queryset = CoevEstud.objects.none()
        for i in range(len(coevs)):
            queryset |= CoevEstud.objects.filter(user=user,coevaluacion__exact=coevs[i])
        return render(request, "coevaluaciones/curso-vista-alumno.html",
                      {'user':user,'curso': curso, 'coevs': coevs, 'usercoev': queryset})
    else:
        # user_coev = CoevEstud.objects.filter(user=user)
        # if es un estudiante
        return render(request, "coevaluaciones/curso-vista-docente.html")


@login_required(login_url='/login')
def ficha_coevaluacion(request, coev_id):
    return redirect('/')