from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=10)
    seccion = models.IntegerField(default=1)
    anho = models.IntegerField()
    semestre = models.IntegerField()

    class Meta:
        unique_together = (("codigo", "seccion", "anho", "semestre"),)


class Equipo(models.Model):
    nombre = models.CharField(max_length=250)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)


class Roles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=50)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)


class PersonaEquipo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)


class Preguntas(models.Model):
    q1 = models.CharField(max_length=500)
    q2 = models.CharField(max_length=500)
    q3 = models.CharField(max_length=500)
    q4 = models.CharField(max_length=500)
    q5 = models.CharField(max_length=500)
    q6 = models.CharField(max_length=500)
    q7 = models.CharField(max_length=500)
    q8 = models.CharField(max_length=500)
    q9 = models.CharField(max_length=500)
    q10 = models.CharField(max_length=500)
    q11 = models.CharField(max_length=500)


class Coevaluacion(models.Model):
    nombre = models.CharField(max_length=200)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    inicio = models.DateField()
    fin = models.DateField()
    # textos de las preguntas
    preguntas = models.ForeignKey(Preguntas, on_delete=models.CASCADE)
    # ponderaciones de las preguntas
    p1 = models.DecimalField()
    p2 = models.DecimalField()
    p3 = models.DecimalField()
    p4 = models.DecimalField()
    p5 = models.DecimalField()
    p6 = models.DecimalField()
    p7 = models.DecimalField()
    p8 = models.DecimalField()


class Resultado(models.Model):
    coevaluacion = models.ForeignKey(Coevaluacion, on_delete=models.CASCADE)
    evaluador = models.ForeignKey(User, on_delete=models.CASCADE)
    evaluado = models.ForeignKey(User, on_delete=models.CASCADE)
    a1 = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(7)])
    a2 = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(7)])
    a3 = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(7)])
    a4 = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(7)])
    a5 = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(7)])
    a6 = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(7)])
    a7 = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(7)])
    a8 = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(7)])
    a9 = models.CharField(max_length=300)
    a10 = models.CharField(max_length=300)
    a11 = models.CharField(max_length=300)


class CoevEstud(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coevaluacion = models.ForeignKey(Coevaluacion, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    estado = models.CharField(max_length=30)
    r1 = models.DecimalField(validators=[MinValueValidator(1),MaxValueValidator(7)],)
    r2 = models.DecimalField(validators=[MinValueValidator(1),MaxValueValidator(7)],)
    r3 = models.DecimalField(validators=[MinValueValidator(1),MaxValueValidator(7)],)
    r4 = models.DecimalField(validators=[MinValueValidator(1),MaxValueValidator(7)],)
    r5 = models.DecimalField(validators=[MinValueValidator(1),MaxValueValidator(7)],)
    r6 = models.DecimalField(validators=[MinValueValidator(1),MaxValueValidator(7)],)
    r7 = models.DecimalField(validators=[MinValueValidator(1),MaxValueValidator(7)],)
    r8 = models.DecimalField(validators=[MinValueValidator(1),MaxValueValidator(7)],)

