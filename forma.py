from django import forms
from app.models import Regiao
from app.models import Coordenadoria
from app.models import Escola
from app.models import Serie
from app.models import Turma
from app.models import Turno
from app.models import Materia
from app.models import Professor
from app.models import Bimestre
from app.models import Pergunta
from app.models import Resposta



# Create your models here.

class RegiaoForm(forms.ModelForm):
   jurisdição = forms.ModelChoiceField(queryset=Regiao.objects.values_list('jurisdicao', flat= True))
   class Meta:
      verbose_name = 'Jurisdição'
      model = Regiao
      fields = ['jurisdição']

class CoordenadoriaForm(forms.ModelForm):

   coordenadoria = forms.ModelChoiceField(queryset=Coordenadoria.objects.values_list('coordenadoria', flat= True))
   class Meta:
      model = Coordenadoria
      fields = ['coordenadoria']

class EscolaForm(forms.ModelForm):
   escola = forms.ModelChoiceField(queryset=Escola.objects.values_list('escola', flat= True))
   class Meta:
      model = Escola
      fields = ['escola']

class TurnoForm(forms.ModelForm):
   turno = forms.ModelChoiceField(queryset=Turno.objects.values_list('turno', flat= True))
   class Meta:
      model = Turno
      fields = ['turno']

class SerieForm(forms.ModelForm):
   série_ou_ano = forms.ModelChoiceField(queryset=Serie.objects.values_list('serie', flat=True))
   #serie = forms.ModelChoiceField(queryset=Serie.objects.values_list('serie'))
   class Meta:
      model = Serie
      fields = ['série_ou_ano']

class TurmaForm(forms.ModelForm):
   turma = forms.ModelChoiceField(queryset=Turma.objects.values_list('turma', flat= True))
   class Meta:
      model = Turma
      fields = ['turma']

class MateriaForm(forms.ModelForm):
   componente_curricular = forms.ModelChoiceField(queryset=Materia.objects.values_list('materia', flat= True))
   class Meta:
      model = Materia
      fields = ['componente_curricular']

class ProfessorForm(forms.ModelForm):
   # turmas = forms.ModelMultipleChoiceField(queryset=Turma.objects.values_list('turma', flat= True), widget=forms.CheckboxSelectMultiple)
   #turnos = forms.ModelMultipleChoiceField(queryset=Turno.objects.values_list('turno', flat= True), widget=forms.CheckboxSelectMultiple)
   class Meta:
      model = Professor
      fields = ['nome']

class BimestreForm(forms.ModelForm):
   class Meta:
      model = Bimestre
      fields = ['bimestre']

class PerguntaForm(forms.ModelForm):
   class Meta:
      model = Pergunta
      fields = ['pergunta']


class RespostaForm(forms.ModelForm):
   class Meta:
      model = Resposta
      fields = ['resposta']
#class Escola_professorForm(forms.ModelForm):
#   class Meta:
#      model = Escola_professor
#      fields = []

#class Materia_professorForm(forms.ModelForm):
#   class Meta:
#      model = Materia_professor
#      fields = []
