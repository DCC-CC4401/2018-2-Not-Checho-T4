from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from coevaluaciones.models import Roles


def login_user(request):
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
def landing_page(request):
    username = request.user.username
    roles = Roles.objects.filter(user__username=username)
    context = {"roles_usuario": roles}
    return render(request, "coevaluaciones/landing-page.html", context)
