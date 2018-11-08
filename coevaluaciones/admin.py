from django.contrib import admin

from coevaluaciones.models import Curso, Equipo, Roles, PersonaEquipo, Preguntas, Coevaluacion, Resultado, CoevEstud

admin.site.register(Curso)
admin.site.register(Equipo)
admin.site.register(Roles)
admin.site.register(PersonaEquipo)
admin.site.register(Preguntas)
admin.site.register(Coevaluacion)
admin.site.register(Resultado)
admin.site.register(CoevEstud)
