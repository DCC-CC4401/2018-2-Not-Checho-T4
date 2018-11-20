from django import forms
from .models import Curso, Equipo, Roles, PersonaEquipo, Preguntas, Coevaluacion, Resultado, CoevEstud
from django.contrib.auth.models import User


NOTAS_A_ELEGIR = [(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7')]

class AddResultadoForm(forms.Form):
    preguntas = Preguntas.objects.get(id=4)
    usuario_id = forms.IntegerField(widget=forms.HiddenInput())
    evaluado_id = forms.IntegerField(widget=forms.HiddenInput())
    coevaluacion_id = forms.IntegerField(widget=forms.HiddenInput())
    a1 = forms.IntegerField(label=preguntas.q1,
                            widget=forms.RadioSelect(choices=NOTAS_A_ELEGIR))
    a2 = forms.IntegerField(label=preguntas.q2,
                            widget=forms.RadioSelect(choices=NOTAS_A_ELEGIR))
    a3 = forms.IntegerField(label=preguntas.q3,
                            widget=forms.RadioSelect(choices=NOTAS_A_ELEGIR))
    a4 = forms.IntegerField(label=preguntas.q4,
                            widget=forms.RadioSelect(choices=NOTAS_A_ELEGIR))
    a5 = forms.IntegerField(label=preguntas.q5,
                            widget=forms.RadioSelect(choices=NOTAS_A_ELEGIR))
    a6 = forms.IntegerField(label=preguntas.q6,
                            widget=forms.RadioSelect(choices=NOTAS_A_ELEGIR))
    a7 = forms.IntegerField(label=preguntas.q7,
                            widget=forms.RadioSelect(choices=NOTAS_A_ELEGIR))
    a8 = forms.IntegerField(label=preguntas.q8,
                            widget=forms.RadioSelect(choices=NOTAS_A_ELEGIR))
    a9 = forms.CharField(label=preguntas.q9,max_length=500, required=False,
                         widget=forms.Textarea(attrs={'cols': "80", 'rows': "10", 'class': 'form-control'}))
    a10 = forms.CharField(label=preguntas.q10,max_length=500, required=False,
                          widget=forms.Textarea(attrs={'cols': "80", 'rows': "10", 'class': 'form-control'}))
    a11 = forms.CharField(label=preguntas.q11,max_length=500, required=False,
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


