from django.db import models
from django.contrib.auth.models import User


class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=10)
    seccion = models.IntegerField(default=1)
    anho = models.IntegerField()
    semestre = models.IntegerField()

    class Meta:
        unique_together = (("codigo", "seccion", "anho", "semestre"),)


class Roles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=50)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
