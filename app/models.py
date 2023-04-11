from django.db import models
from django.db.models import CASCADE
import mysql.connector

class Professor(models.Model):

    jurisdicao = models.ForeignKey('Jurisdicao', on_delete=CASCADE,verbose_name='Jurisdição')
    coordenadoria = models.ForeignKey('Coordenadoria', on_delete=CASCADE)
    escola = models.ForeignKey('Escola', on_delete=CASCADE)
    turno = models.ForeignKey('Turno', on_delete=CASCADE)
    serie = models.ForeignKey('Serie', on_delete=CASCADE,verbose_name='Série | Ano')
    turma = models.ForeignKey('Turma', on_delete=CASCADE)
    materia = models.ForeignKey('Materia', on_delete=CASCADE,verbose_name='Componente Curricular')
    nome = models.CharField(max_length=50, verbose_name='Nome do Professor(a)')

    def __str__(self):
        return self.nome


class Jurisdicao(models.Model):

    jurisdicao = models.CharField(max_length=20, verbose_name='Jurisdição')

    def __str__(self):
        return self.jurisdicao

class Coordenadoria(models.Model):

    coordenadoria = models.CharField(max_length=50, verbose_name='Coordenadoria')
    #coordenacao = models.CharField(max_length=10)
    jurisdicao = models.ForeignKey(Jurisdicao, on_delete=CASCADE)

    def __str__(self):
        return self.coordenadoria


class Escola(models.Model):

    escola = models.CharField(max_length=100, verbose_name='Escola')
    coordenadoria = models.ForeignKey(Coordenadoria, on_delete=CASCADE)

    def __str__(self):
        return self.escola

class Turno(models.Model):

    turno = models.CharField(max_length=20, verbose_name='Turno')
    escola = models.ForeignKey(Escola, on_delete=CASCADE)

    def __str__(self):
        return self.turno

class Serie(models.Model):

    serie = models.CharField(max_length=20, verbose_name='Série/Ano')
    turno = models.ForeignKey(Turno, on_delete=CASCADE)

    def __str__(self):
        return self.serie


class Turma(models.Model):

    turma = models.CharField(max_length=20, verbose_name='Turma')
    serie = models.ForeignKey(Serie, on_delete=CASCADE)

    def __str__(self):
        return self.turma

class Materia(models.Model):

    materia = models.CharField(max_length=25, verbose_name='Componente Curricular')
    serie = models.ForeignKey(Serie, on_delete=CASCADE)

    def __str__(self):
        return self.materia

class Bimestre(models.Model):
    bimestre = models.CharField(max_length=25, verbose_name='Bimestre')
    materia = models.ForeignKey(Materia, on_delete=CASCADE)

    def __str__(self):
        return self.bimestre

class Pergunta(models.Model):
    bimestref = models.ForeignKey('Bimestref', on_delete=CASCADE)
    pergunta = models.CharField(max_length=500)


    def __str__(self):
        return self.pergunta

class Resposta(models.Model):
    resposta = models.BooleanField()
    professor = models.ForeignKey(Professor, on_delete=CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete=CASCADE)
    foi_possivel = models.BooleanField()
    motivo = models.CharField(max_length=100,null=True)
    outros = models.CharField(max_length=150,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.resposta


class Serief(models.Model):

    serie = models.CharField(max_length=20, verbose_name='Série/Ano')

    def __str__(self):
        return self.serie


class Materiaf(models.Model):

    materia = models.CharField(max_length=25, verbose_name='Componente Curricular')
    serief = models.ForeignKey(Serief, on_delete=CASCADE)

    def __str__(self):
        return self.materia

class Bimestref(models.Model):
    bimestre = models.CharField(max_length=25, verbose_name='Bimestre')
    materiaf = models.ForeignKey(Materiaf, on_delete=CASCADE)

    def __str__(self):
        return self.bimestre
#class Escola_professor(models.Model):
 #   escola = models.ForeignKey(Escola, on_delete=CASCADE )
 #   professor = models.ForeignKey(Professor, on_delete=CASCADE)

#class Materia_professor(models.Model):
    #alterar turma para checklist
#    materia = models.ForeignKey(Materias, on_delete=CASCADE)
#    professor = models.ForeignKey(Professor, on_delete=CASCADE)
#    escola = models.ForeignKey(Escola, on_delete=CASCADE)
#    turno = models.ForeignKey(Turno, on_delete=CASCADE)
#    serie = models.ForeignKey(Serie, on_delete=CASCADE)
#    turma = models.ForeignKey(Turma, on_delete=CASCADE)

# construir formulário para a matéria class Matemática(models.Model)

