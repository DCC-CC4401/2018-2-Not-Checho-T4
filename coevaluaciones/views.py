from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone

from coevaluaciones.models import Roles
from .forms import AddResultadoForm
from .models import Curso, Coevaluacion, Resultado, CoevEstud


def login_user(request):
    """ Inicia sesión para un usuario.  """
    logout(request)
    if request.POST:
        username = request.POST['username'].replace('.', '').replace('-', '')
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    return render(request, "coevaluaciones/login.html", {})


@login_required(login_url='/login')
def logout_user(request):
    """ Cierra sesión para un usuario.  """
    logout(request)
    return redirect('login')


@login_required(login_url='/login')
def landing_page(request):
    """ Carga el landing page.
        En el landing page se muestran los cursos cursados por el usuario, junto con su rol en estos y una tabla con
        las 10 coevaluaciones más recientes.
    """
    user = request.user
    roles = Roles.objects.filter(user=user)
    coevaluaciones = CoevEstud.objects.filter(user=user).order_by("-coevaluacion__fin")[:9]
    context = {"user": user,
               "roles_usuario": roles,
               "coev_estud": coevaluaciones}
    return render(request, "coevaluaciones/landing-page.html", context)


@login_required(login_url='/login')
def perfil(request):
    # Tu Perfil
    user = request.user

    # Tus Cursos
    aux = Roles.objects.none()
    for c in Curso.objects.filter().order_by('-anho', '-semestre'):
        for r in Roles.objects.filter(user=user):
            if r.curso == c:
                aux |= Roles.objects.filter(user=user, curso=c)

    # Tus Notas
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

    def take_first(lista):
        return lista[0]

    res.sort(key=take_first, reverse=True)

    # Return
    return render(request, "coevaluaciones/perfil-vista-dueno.html", {'user': user, 'aux': aux, 'res': res})


@login_required(login_url='/login')
def ficha_curso(request, curso_id):
    user = request.user
    curso = Curso.objects.get(id=curso_id)
    roli = Roles.objects.get(user=user, curso=curso)
    if roli.rol == "Alumno":
        coevs = Coevaluacion.objects.filter(curso=curso).order_by('-fin')
        for c in coevs:
            actualizar_coevaluacion(c)
        queryset = CoevEstud.objects.none()
        for i in range(len(coevs)):
            queryset |= CoevEstud.objects.filter(user=user, coevaluacion__exact=coevs[i])
        return render(request, "coevaluaciones/curso-vista-alumno.html",
                      {'user': user, 'curso': curso, 'coevs': coevs, 'usercoev': queryset})
    else:
        # user_coev = CoevEstud.objects.filter(user=user)
        # if es un estudiante
        return render(request, "coevaluaciones/curso-vista-docente.html")


@login_required(login_url='/login')
def ficha_coevaluacion(request, coev_id):
    user = request.user
    coevaluacion = Coevaluacion.objects.get(id=coev_id)
    actualizar_coevaluacion(coevaluacion)
    roli = Roles.objects.get(user=user, curso=coevaluacion.curso)
    if roli.rol == "Alumno":
        # Compañeros
        user_coev = CoevEstud.objects.get(user=user, coevaluacion=coevaluacion)
        companheros = CoevEstud.objects.filter(coevaluacion=coevaluacion, equipo=user_coev.equipo).exclude(user=user)
        # Estado para compañeros
        contestadas = []
        for c in companheros:
            presente = Resultado.objects.filter(evaluador=user, evaluado=c.user, coevaluacion=coevaluacion).first()
            if presente is None:
                contestadas.append([c.user, False])
            else:
                contestadas.append([c.user, True])
        # Estado de la coevaluacion del estudiante
        l = 0
        for c in contestadas:
            if not c[1]:
                l = 1
        if l == 0:  # si contesto para todos
            user_coev.estado = "Contestada"
            user_coev.save()
        else:
            user_coev.estado = "Pendiente"
            user_coev.save()

        form = AddResultadoForm()
        context = {'user': user, 'coevaluacion': coevaluacion, 'curso': coevaluacion.curso, 'user_coev': user_coev,
                   'eval_form': form, 'contestadas': contestadas}
        return render(request, "coevaluaciones/coevaluacion-vista-alumno.html", context)
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


def actualizar_coevaluacion(coevaluacion):
    fecha_termino = coevaluacion.fin
    fecha_actual = timezone.now()
    if fecha_termino < fecha_actual:
        coevaluacion.estado = "Cerrada"
        coevaluacion.save()
    else:  # Para prueba de funcion
        coevaluacion.estado = "Abierta"
        coevaluacion.save()
