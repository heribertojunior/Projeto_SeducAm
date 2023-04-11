from django import forms
from app.models import Jurisdicao
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

class ProfessorForm(forms.ModelForm):
   class Meta:
      model = Professor
      fields = "__all__"

   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['coordenadoria'].queryset = Coordenadoria.objects.none()
        self.fields['escola'].queryset = Escola.objects.none()
        self.fields['turno'].queryset = Turno.objects.none()
        self.fields['serie'].queryset = Serie.objects.none()
        self.fields['turma'].queryset = Turma.objects.none()
        self.fields['materia'].queryset = Turma.objects.none()

        if 'jurisdicao' in self.data:
            try:
               jurisdicao_id = int(self.data.get('jurisdicao'))
               self.fields['coordenadoria'].queryset = Coordenadoria.objects.filter(jurisdicao_id=jurisdicao_id).order_by('coordenadoria')
            except (ValueError, TypeError):
               pass
        elif self.instance.pk:
            self.fields['coordenadoria'].queryset = self.instance.jurisdicao.coordenadoria_set.order_by('coordenadoria')

        if 'coordenadoria' in self.data:
            try:
               coordenadoria_id = int(self.data.get('coordenadoria'))
               self.fields['escola'].queryset = Escola.objects.filter(coordenadoria_id=coordenadoria_id).order_by('escola')
            except (ValueError, TypeError):
               pass
        elif self.instance.pk:
            self.fields['escola'].queryset = self.instance.coordenadoria.escola_set.order_by('escola')

        if 'escola' in self.data:
            try:
               escola_id = int(self.data.get('escola'))
               self.fields['turno'].queryset = Turno.objects.filter(escola_id=escola_id).order_by('turno')
            except (ValueError, TypeError):
               pass
        elif self.instance.pk:
            self.fields['turno'].queryset = self.instance.escola.turno_set.order_by('turno')

        if 'turno' in self.data:
            try:
               turno_id = int(self.data.get('turno'))
               self.fields['serie'].queryset = Serie.objects.filter(turno_id=turno_id).order_by('serie')
            except (ValueError, TypeError):
               pass
        elif self.instance.pk:
            self.fields['serie'].queryset = self.instance.turno.serie_set.order_by('serie')


        if 'serie' in self.data:
            try:
               serie_id = int(self.data.get('serie'))
               self.fields['turma'].queryset = Turma.objects.filter(serie_id=serie_id).order_by('turma')
               self.fields['materia'].queryset = Materia.objects.filter(serie_id=serie_id).order_by('materia')
            except (ValueError, TypeError):
               pass
        elif self.instance.pk:
            self.fields['turma'].queryset = self.instance.serie.turma_set.order_by('turma')
            self.fields['materia'].queryset = self.instance.serie.materia_set.order_by('materia')



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

class SerieForm(forms.ModelForm):
   class Meta:
      model = Serie
      fields = '__all__'

class TurmaForm(forms.ModelForm):
   class Meta:
      model = Turma
      fields = '__all__'


class MateriaForm(forms.ModelForm):
   class Meta:
      model = Materia
      fields = '__all__'
