from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Curso(models.Model):
    nombre = models.CharField(max_length=300)
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
    q1 = models.CharField(max_length=1000)
    q2 = models.CharField(max_length=1000)
    q3 = models.CharField(max_length=1000)
    q4 = models.CharField(max_length=1000)
    q5 = models.CharField(max_length=1000)
    q6 = models.CharField(max_length=1000)
    q7 = models.CharField(max_length=1000)
    q8 = models.CharField(max_length=1000)
    q9 = models.CharField(max_length=1000)
    q10 = models.CharField(max_length=1000)
    q11 = models.CharField(max_length=1000)


class Coevaluacion(models.Model):
    ESTADOS = [('Publicada','Publicada'),('Cerrada','Cerrada'),('Abierta','Abierta')]
    nombre = models.CharField(max_length=200)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    estado = models.CharField(max_length=25,choices=ESTADOS,default='Abierta')
    # textos de las preguntas
    preguntas = models.ForeignKey(Preguntas, on_delete=models.CASCADE)
    # ponderaciones de las preguntas
    p1 = models.DecimalField(max_digits=5, decimal_places=3)
    p2 = models.DecimalField(max_digits=5, decimal_places=3)
    p3 = models.DecimalField(max_digits=5, decimal_places=3)
    p4 = models.DecimalField(max_digits=5, decimal_places=3)
    p5 = models.DecimalField(max_digits=5, decimal_places=3)
    p6 = models.DecimalField(max_digits=5, decimal_places=3)
    p7 = models.DecimalField(max_digits=5, decimal_places=3)
    p8 = models.DecimalField(max_digits=5, decimal_places=3)


class Resultado(models.Model):
    coevaluacion = models.ForeignKey(Coevaluacion, on_delete=models.CASCADE)
    evaluador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evalua')
    evaluado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluado')
    a1 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    a2 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    a3 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    a4 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    a5 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    a6 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    a7 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    a8 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    a9 = models.CharField(max_length=500)
    a10 = models.CharField(max_length=500)
    a11 = models.CharField(max_length=500)


class CoevEstud(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coevaluacion = models.ForeignKey(Coevaluacion, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    estado = models.CharField(max_length=30)
    r1 = models.DecimalField(default=None, validators=[MinValueValidator(1), MaxValueValidator(7)], max_digits=5,
                             decimal_places=3)
    r2 = models.DecimalField(default=None, validators=[MinValueValidator(1), MaxValueValidator(7)], max_digits=5,
                             decimal_places=3)
    r3 = models.DecimalField(default=None, validators=[MinValueValidator(1), MaxValueValidator(7)], max_digits=5,
                             decimal_places=3)
    r4 = models.DecimalField(default=None, validators=[MinValueValidator(1), MaxValueValidator(7)], max_digits=5,
                             decimal_places=3)
    r5 = models.DecimalField(default=None, validators=[MinValueValidator(1), MaxValueValidator(7)], max_digits=5,
                             decimal_places=3)
    r6 = models.DecimalField(default=None, validators=[MinValueValidator(1), MaxValueValidator(7)], max_digits=5,
                             decimal_places=3)
    r7 = models.DecimalField(default=None, validators=[MinValueValidator(1), MaxValueValidator(7)], max_digits=5,
                             decimal_places=3)
    r8 = models.DecimalField(default=None, validators=[MinValueValidator(1), MaxValueValidator(7)], max_digits=5,
                             decimal_places=3)
