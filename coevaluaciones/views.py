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
        res.append([r.coevaluacion.inicio, r.coevaluacion.nombre, round(temp, 1), r.coevaluacion.curso])
    res.sort(reverse=True)

    # lista_coevs es la lista del nombre de todas las coevaluaciones sin repeticiones
    lista_coevs = []
    for i in range(len(res)):
        if res[i][1] not in lista_coevs:
            lista_coevs.append(res[i][1])

    # par_coevs_nota es una lista de cada coevaluacion sin repeticiones con las notas promediadas
    par_coevs_nota = []
    for nombre_coev in lista_coevs:
        i=0
        nota = 0
        for r in res:
            if r[1] == nombre_coev:
                nota += r[2]
                i += 1
        i = max(1, i)
        nota = nota/i
        par_coevs_nota.append([nombre_coev, nota])

    # trip_notas es una lista de cada coevaluacion sin repeticiones con las notas promediadas y la fecha de inicio de cada coevaluacion
    trip_notas = []
    for i in range(len(par_coevs_nota)):
        trip_notas.append([par_coevs_nota[i][0], par_coevs_nota[i][1], 0])
    for a in trip_notas:
        for b in res:
            if b[1] == a[0]:
                a[2] = b[0]

    # Return
    return render(request, "coevaluaciones/perfil-vista-dueno.html", {'user': user, 'aux': aux, 'notas': trip_notas})

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

MENSAJE={"error":" Ha ocurrido un error. \n No se ha agregado la Coevaluación \n Revisa que las ponderaciones sumen 1.",
         "exito":"Se ha agregado correctamente la Coevaluación.",
         " ":""}

@login_required(login_url='/login')
def ficha_curso(request, curso_id,mensaje=" "):
    user = request.user
    curso = Curso.objects.get(id=curso_id)
    roli = Roles.objects.get(user=user, curso=curso)
    coevs = Coevaluacion.objects.filter(curso=curso).order_by('-fin')
    for c in coevs:
        actualizar_coevaluacion(c)
    if roli.rol == "Alumno":
        queryset = CoevEstud.objects.none()
        for i in range(len(coevs)):
            queryset |= CoevEstud.objects.filter(user=user, coevaluacion__exact=coevs[i])
        return render(request, "coevaluaciones/curso-vista-alumno.html",
                      {'user': user, 'curso': curso, 'usercoev': queryset})
    elif roli.rol == "Profesor" or roli.rol == "Auxiliar" or roli.rol == "Ayudante":
        return render(request, "coevaluaciones/curso-vista-docente.html",{'user': user,'rol':roli.rol,'mensaje':MENSAJE[mensaje],
                                                                          'curso': curso,'coevaluaciones':coevs})
    else:
        return redirect('')


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
    elif roli.rol == "Profesor" or roli.rol == "Auxiliar" or roli.rol == "Ayudante":
        return render(request, "coevaluaciones/coevaluacion-vista-docente.html")
    else:
        return redirect('')


@login_required(login_url='/login')
def subir_coevaluacion(request, coev_id):
    if request.method == 'POST':
        form = AddResultadoForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('ficha_coevaluacion', coev_id=coev_id)


@login_required(login_url='/login')
def agregar_coevaluacion(request, curso_id):
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


def actualizar_coevaluacion(coevaluacion):
    fecha_termino = coevaluacion.fin
    fecha_actual = timezone.now()
    if fecha_termino < fecha_actual:
        coevaluacion.estado = "Cerrada"
        coevaluacion.save()
    else:  # Para prueba de funcion
        coevaluacion.estado = "Abierta"
        coevaluacion.save()
