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
def perfil(request):
    #Tu Perfil
    user = request.user

    #Tus Cursos
    aux = Roles.objects.none()
    for c in Curso.objects.filter().order_by('-anho', '-semestre'):
        for r in Roles.objects.filter(user=user):
            if r.curso == c:
                aux |= Roles.objects.filter(user=user, curso=c)

    #Tus Notas
    res = []
    for r in Resultado.objects.filter(evaluado=user):
        temp = 0
        temp += r.a1 * r.coevaluacion.p1
        temp += r.a2 * r.coevaluacion.p2
        temp += r.a3 * r.coevaluacion.p3
        temp += r.a4 * r.coevaluacion.p4
        temp += r.a5 * r.coevaluacion.p5
        temp += r.a6 * r.coevaluacion.p6
        temp += r.a7 * r.coevaluacion.p7
        temp += r.a8 * r.coevaluacion.p8
        res.append([r.coevaluacion.inicio, r.coevaluacion.nombre, round(temp, 1)])
    def takeFirst(list):
        return list[0]
    res.sort(key=takeFirst, reverse=True)

    #Return
    return render(request, "coevaluaciones/perfil-vista-dueno.html", {'user': user, 'aux': aux, 'res': res})

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