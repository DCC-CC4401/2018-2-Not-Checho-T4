from django import forms
from .models import Curso, Equipo, Roles, PersonaEquipo, Preguntas, Coevaluacion, Resultado, CoevEstud
from django.contrib.auth.models import User


NOTAS_A_ELEGIR = [(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7')]
PREGUNTAS = ["¿Demuestra compromiso con el proyecto?",
             "¿Cumple de manera adecuada con las tareas que le son asignadas?",
             "¿Demuestra iniciativa para lograr el éxito del proyecto?",
             "¿Mantiene buena comunicación con el resto del equipo?",
             "¿Mantiene buena coordinación entre sus tareas y las de sus pares?",
             "¿La calidad de su trabajo es la apropiada para lograr el éxito del proyecto?",
             "¿Ofrece apoyo en las tareas que van más allá del rol asignado?",
             "¿Es capaz de admitir sus equivocaciones y recibir críticas?",
             "Fortalezas","Debilidades","Comentario"]
class AddResultadoForm(forms.Form):
    usuario_id = forms.IntegerField(widget=forms.HiddenInput())
    evaluado_id = forms.IntegerField(widget=forms.HiddenInput())
    coevaluacion_id = forms.IntegerField(widget=forms.HiddenInput())
    a1 = forms.IntegerField(label=PREGUNTAS[0],
                            widget=forms.RadioSelect(choices=NOTAS_A_ELEGIR, attrs={'class': 'inline'}))
    a2 = forms.IntegerField(label=PREGUNTAS[1],
                            widget=forms.RadioSelect(choices=NOTAS_A_ELEGIR, attrs={'class': 'inline'}))
    a3 = forms.IntegerField(label=PREGUNTAS[2],
                            widget=forms.RadioSelect(choices=NOTAS_A_ELEGIR, attrs={'class': 'inline'}))
    a4 = forms.IntegerField(label=PREGUNTAS[3],
                            widget=forms.RadioSelect(choices=NOTAS_A_ELEGIR, attrs={'class': 'inline'}))
    a5 = forms.IntegerField(label=PREGUNTAS[4],
                            widget=forms.RadioSelect(choices=NOTAS_A_ELEGIR, attrs={'class': 'inline'}))
    a6 = forms.IntegerField(label=PREGUNTAS[5],
                            widget=forms.RadioSelect(choices=NOTAS_A_ELEGIR, attrs={'class': 'inline'}))
    a7 = forms.IntegerField(label=PREGUNTAS[6],
                            widget=forms.RadioSelect(choices=NOTAS_A_ELEGIR, attrs={'class': 'inline'}))
    a8 = forms.IntegerField(label=PREGUNTAS[7],
                            widget=forms.RadioSelect(choices=NOTAS_A_ELEGIR, attrs={'class': 'inline'}))
    a9 = forms.CharField(label=PREGUNTAS[8],max_length=500, required=False,
                         widget=forms.Textarea(attrs={'cols': "80", 'rows': "10", 'class': 'form-control'}))
    a10 = forms.CharField(label=PREGUNTAS[9],max_length=500, required=False,
                          widget=forms.Textarea(attrs={'cols': "80", 'rows': "10", 'class': 'form-control'}))
    a11 = forms.CharField(label=PREGUNTAS[10],max_length=500, required=False,
                          widget=forms.Textarea(attrs={'cols': "80", 'rows': "10", 'class': 'form-control'}))

    def save(self, *args, **kwargs):
        u = User.objects.get(id=self.cleaned_data['usuario_id'])
        e = User.objects.get(id=self.cleaned_data['evaluado_id'])
        c = Coevaluacion.objects.get(id=self.cleaned_data['coevaluacion_id'])

        r = Resultado.objects.filter(coevaluacion=c, evaluador=u,evaluado=e).first()
        if r is None:
            resultado = Resultado(coevaluacion=c, evaluador=u, evaluado=e,
                                  a1=self.cleaned_data['a1'],
                                  a2=self.cleaned_data['a2'],
                                  a3=self.cleaned_data['a3'],
                                  a4=self.cleaned_data['a4'],
                                  a5=self.cleaned_data['a5'],
                                  a6=self.cleaned_data['a6'],
                                  a7=self.cleaned_data['a7'],
                                  a8=self.cleaned_data['a8'],
                                  a9=self.cleaned_data['a9'],
                                  a10=self.cleaned_data['a10'],
                                  a11=self.cleaned_data['a11'])

            resultado.save()
        else:
            r.a1 = self.cleaned_data['a1']
            r.a2 = self.cleaned_data['a2']
            r.a3 = self.cleaned_data['a3']
            r.a4 = self.cleaned_data['a4']
            r.a5 = self.cleaned_data['a5']
            r.a6 = self.cleaned_data['a6']
            r.a7 = self.cleaned_data['a7']
            r.a8 = self.cleaned_data['a8']
            r.a9 = self.cleaned_data['a9']
            r.a10 = self.cleaned_data['a10']
            r.a11 = self.cleaned_data['a11']
            r.save()
        # Cambia el resultado del evaluado
        ce = CoevEstud.objects.get(user=e,coevaluacion=c)
        set_r = Resultado.objects.filter(coevaluacion=c, evaluado=e)
        r1 = 0
        r2 = 0
        r3 = 0
        r4 = 0
        r5 = 0
        r6 = 0
        r7 = 0
        r8 = 0
        for i in set_r:
            r1 += i.a1
            r2 += i.a2
            r3 += i.a3
            r4 += i.a4
            r5 += i.a5
            r6 += i.a6
            r7 += i.a7
            r8 += i.a8
        ce.r1 = r1 / len(set_r)
        ce.r2 = r2 / len(set_r)
        ce.r3 = r3 / len(set_r)
        ce.r4 = r4 / len(set_r)
        ce.r5 = r5 / len(set_r)
        ce.r6 = r6 / len(set_r)
        ce.r7 = r7 / len(set_r)
        ce.r8 = r8 / len(set_r)
        ce.save()


