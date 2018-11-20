from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Curso, Equipo, Roles, PersonaEquipo, Preguntas, Coevaluacion, Resultado, CoevEstud
from .forms import AddResultadoForm
from django.core import serializers


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
def ficha_curso(request):#,curso_id):
    user = request.user
    #curso = Curso.objects.get(id=curso_id)
    ## ojo harcodeado
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
    user = request.user
    coevaluacion = Coevaluacion.objects.get(id=coev_id)
    roli = Roles.objects.get(user=user, curso=coevaluacion.curso)
    if roli.rol=="Alumno":
        # Compañeros
        user_coev = CoevEstud.objects.get(user=user, coevaluacion=coevaluacion)
        companheros = CoevEstud.objects.filter(coevaluacion=coevaluacion, equipo=user_coev.equipo).exclude(user=user)
        # Estado para compañeros
        contestadas = []
        for c in companheros:
            presente = Resultado.objects.filter(evaluador=user,evaluado=c.user,coevaluacion=coevaluacion).first()
            if presente is None:
                contestadas.append([c.user,False])
            else:
                contestadas.append([c.user,True])
        # Estado de la coevaluacion del estudiante
        l = 0
        for c in contestadas:
            if not c[1]:
                l = 1
        if l == 0: # si contesto para todos
            user_coev.estado = "Contestada"
            user_coev.save()
        else:
            user_coev.estado = "Pendiente"
            user_coev.save()

        form = AddResultadoForm()
        context = {'user': user, 'coevaluacion': coevaluacion, 'curso': coevaluacion.curso, 'user_coev': user_coev,
                   'eval_form': form,'contestadas':contestadas}
        return render(request, "coevaluaciones/coevaluacion-vista-alumno.html",context)
    else:
        return render(request, "coevaluaciones/coevaluacion-vista-docente.html")


@login_required(login_url='/login')
def subir_coevaluacion(request, coev_id):
    # user = request.user
    # coev = Coevaluacion.objects.get(id=coev_id)
    if request.method == 'POST':
        form = AddResultadoForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('ficha_coevaluacion', coev_id=coev_id)

