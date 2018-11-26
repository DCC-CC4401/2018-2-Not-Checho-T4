from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from coevaluaciones.models import Roles
from .forms import AddResultadoForm
from .models import Curso, Coevaluacion, Resultado, CoevEstud, Preguntas, Equipo, PersonaEquipo


def login_user(request):
    """ Inicia sesión para un usuario.  """
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
    cursos = Roles.objects.none()
    for c in Curso.objects.filter().order_by('-anho', '-semestre'):
        for r in Roles.objects.filter(user=user):
            if r.curso == c:
                cursos |= Roles.objects.filter(user=user, curso=c)

    # Tus Notas
    notas = []
    for c in CoevEstud.objects.filter(user=user):
        temp = (c.r1 + c.r2 + c.r3 + c.r4 + c.r5 + c.r6 + c.r7 + c.r8)/8
        notas.append([c.coevaluacion.inicio, c.coevaluacion.nombre, round(temp, 1)])
    notas.sort(reverse=True)

    # Return
    return render(request, "coevaluaciones/perfil-vista-dueno.html", {'user': user, 'cursos': cursos, 'notas': notas})

@login_required(login_url='/login')
def cambiarContra(request):
    userName = request.user
    passOld = request.POST['passOld']
    passNew = request.POST['passNew']
    passNewConfirm = request.POST['passNewConfirm']
    user = authenticate(username=userName, password=passOld)
    if user is not None:
        if passNew == passNewConfirm:
            userName.set_password(passNew)
            userName.save()
            login(request, userName)
    return HttpResponseRedirect('/perfil')


MENSAJE = {"error":" Ha ocurrido un error. \n No se ha agregado la Coevaluación \n Revisa que las ponderaciones sumen 1.",
         "exito":"Se ha agregado correctamente la Coevaluación.",
         " ":""}

@login_required(login_url='/login')
def ficha_curso(request, curso_id,mensaje=" "):
    """ Muestra las coevaluaciones para el curso."""
    user = request.user
    curso = Curso.objects.get(id=curso_id)
    rol_user = Roles.objects.get(user=user, curso=curso)
    coevs = Coevaluacion.objects.filter(curso=curso).order_by('-fin')
    for c in coevs:
        actualizar_coevaluacion(c)
    if rol_user.rol == "Alumno":
        queryset = CoevEstud.objects.none()
        for i in range(len(coevs)):
            queryset |= CoevEstud.objects.filter(user=user, coevaluacion__exact=coevs[i])
        return render(request, "coevaluaciones/curso-vista-alumno.html",
                      {'user': user, 'curso': curso, 'usercoev': queryset})
    elif rol_user.rol == "Profesor" or rol_user.rol == "Auxiliar" or rol_user.rol == "Ayudante":
        return render(request, "coevaluaciones/curso-vista-docente.html",{'user': user,'rol':rol_user.rol,'mensaje':MENSAJE[mensaje],
                                                                          'curso': curso,'coevaluaciones':coevs})
    else:
        return redirect('')


@login_required(login_url='/login')
def ficha_coevaluacion(request, coev_id):
    """ Muestra una coevaluacion y permite contestarla para un alumno. """
    user = request.user
    coevaluacion = Coevaluacion.objects.get(id=coev_id)
    actualizar_coevaluacion(coevaluacion)
    rol_user = Roles.objects.get(user=user, curso=coevaluacion.curso)
    if rol_user.rol == "Alumno":
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
    elif rol_user.rol == "Profesor" or rol_user.rol == "Auxiliar" or rol_user.rol == "Ayudante":
        return render(request, "coevaluaciones/coevaluacion-vista-docente.html")
    else:
        return redirect('')


@login_required(login_url='/login')
def subir_coevaluacion(request, coev_id):
    """ Sube los resultados de una coevaluacion. """
    if request.method == 'POST':
        form = AddResultadoForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('ficha_coevaluacion', coev_id=coev_id)


@login_required(login_url='/login')
def agregar_coevaluacion(request, curso_id):
    """ Agrega una coevaluacion a un curso. """
    if request.method == 'POST':
        nombre = request.POST['nombre_coev']
        inicio = str(request.POST['fecha_inicio'] + ' '+ request.POST['hora_inicio'])
        fin = str(request.POST['fecha_fin'] + ' '+ request.POST['hora_fin'])
        curso = Curso.objects.get(id=request.POST['curso_id'])
        p_p1 = request.POST['p_p1']
        p_p2 = request.POST['p_p2']
        p_p3 = request.POST['p_p3']
        p_p4 = request.POST['p_p4']
        p_p5 = request.POST['p_p5']
        p_p6 = request.POST['p_p6']
        p_p7 = request.POST['p_p7']
        p_p8 = request.POST['p_p8']
        sum = float(p_p1) + float(p_p2) + float(p_p3) + float(p_p4) + float(p_p5) +float(p_p6)+float(p_p7)+float(p_p8)
        if sum != 1.0:
            return redirect('ficha_curso',curso_id,"error")
        nueva_coevaluacion = Coevaluacion(nombre=nombre,
                                          curso=curso,
                                          inicio=inicio,
                                          fin=fin,
                                          preguntas= Preguntas.objects.all().first(),
                                          p1=float(p_p1),
                                          p2=float(p_p2),
                                          p3=float(p_p3),
                                          p4=float(p_p4),
                                          p5=float(p_p5),
                                          p6=float(p_p6),
                                          p7=float(p_p7),
                                          p8=float(p_p8))
        nueva_coevaluacion.save()
        #agregar los coevestud para todos los estudiantes con sus grupos correspondientes
        equipos = Equipo.objects.filter(curso=curso)
        personas = PersonaEquipo.objects.filter(equipo__in=equipos,estado=True)
        for p in personas:
            n_coevestud = CoevEstud(user=p.user,coevaluacion=nueva_coevaluacion,equipo=p.equipo,estado="Pendiente",
                                    r1=None, r2=None,r3=None,r4=None,r5=None,r6=None,r7=None,r8=None)
            n_coevestud.save()
    return redirect('ficha_curso',curso_id,"exito")


@login_required(login_url='/login')
def publicar_coevaluacion(request, curso_id,coev_id):
    coevaluacion = Coevaluacion.objects.get(id=coev_id)
    coevaluacion.estado = 'Publicada'
    coevaluacion.save()
    print(coevaluacion.estado)
    return redirect('ficha_curso', curso_id)


def actualizar_coevaluacion(coevaluacion):
    """ Actualiza el estado de una coevaluacion. """
    fecha_termino = coevaluacion.fin
    fecha_actual = timezone.now()
    if fecha_termino < fecha_actual and coevaluacion.estado == "Abierta":
        coevaluacion.estado = "Cerrada"
        coevaluacion.save()
    elif fecha_termino >= fecha_actual:
        coevaluacion.estado = "Abierta"
        coevaluacion.save()
