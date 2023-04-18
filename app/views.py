from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from app.models import Professor
from app.models import Coordenadoria
from app.forms import ProfessorForm
from app.forms import SerieForm
from app.forms import TurmaForm
from app.forms import MateriaForm
from django.urls import reverse
from app.models import Bimestre
from app.forms import BimestreForm
from app.models import Pergunta
from app.forms import PerguntaForm
from app.models import Resposta
from app.forms import RespostaForm
from app.models import Escola, Turno , Serie, Turma, Materia, Serief, Materiaf, Bimestref
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from io import BytesIO
import xlsxwriter




def home(requests):
    return render(requests, 'sobre.html')

class ModeloView(TemplateView):
    template_name = "model.html"

def sobre(requests):
     return render(requests, 'sobre.html')





#precisa autenticar o usuario
@login_required
def painel(request):

    return render(request, 'painel.html')



@login_required
def getRelatorio(request):
    return render(request, 'relatorio.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

#Função para cadastrar professor e redirecionar para a página de perguntas
@login_required
def formulario(request):
    if request.method == "GET":
        form_professor = ProfessorForm()

        context = {
            'form_professor': form_professor,
    }
        return render(request, "form.html", context = context)

    elif request.method == "POST":
        form_professor = ProfessorForm(request.POST)
        if form_professor.is_valid():
            form_professor.save()
            serie = Serie.objects.get(id=int(request.POST.get('serie')))
            materia= Materia.objects.get(id = int(request.POST.get('materia')))
            serief = Serief.objects.get(serie = serie.serie)
            materiasf = Materiaf.objects.filter(serief_id = serief.id)

            if materia.materia == "Matemática":
                if materiasf[0].materia == "Matemática":
                    materiaf = materiasf[0]
                else:
                    materiaf = materiasf[1]
            else :
                if materiasf[0].materia == "Português":
                    materiaf = materiasf[0]
                else:
                    materiaf = materiasf[1]

            bimestres = Bimestref.objects.filter(materiaf_id = materiaf.id)
            pb1 = Pergunta.objects.filter(bimestref_id = bimestres[0].id).order_by('id')
            pb2 = Pergunta.objects.filter(bimestref_id = bimestres[1].id).order_by('id')
            pb3 = Pergunta.objects.filter(bimestref_id = bimestres[2].id).order_by('id')
            pb4 = Pergunta.objects.filter(bimestref_id = bimestres[3].id).order_by('id')
            context ={
                'professor_instance': form_professor,
                'perguntas_b1': pb1,
                'perguntas_b2': pb2,
                'perguntas_b3': pb3,
                'perguntas_b4': pb4,
                'b1_id':bimestres[0].id,
                'b2_id':bimestres[1].id,
                'b3_id':bimestres[2].id,
                'b4_id':bimestres[3].id,
                'materia': materia.materia,
            }

            return render (request, "pergunta.html", context)



    else:
            context = {
            'form_professor': form_professor,
            }

            return render (request, "form.html", context)


#Função para salvar as respostas
@login_required
def salvarResposta(request):


    if request.method == "POST":
        if request.POST.get('bimestre_1') == '1':
            b1 = request.POST.get('bimestre1')
            perguntas = Pergunta.objects.filter(bimestref_id = b1).order_by('id')
            for pergunta in perguntas:
                form_resposta = RespostaForm(request.POST)
                if form_resposta.is_valid():
                    f_cont = form_resposta.save(commit=False)
                    f_cont.professor = Professor.objects.get(id=int(request.POST.get('professor')))
                    f_cont.pergunta = Pergunta.objects.get(id = int(pergunta.id))
                if request.POST.get('foi_possivelb1') == 'sim':
                    f_cont.foi_possivel = True
                else:
                    f_cont.foi_possivel = False
                    if request.POST.get('motivob1') == 'Outros':
                        f_cont.motivo = "Outros"
                        f_cont.outros = request.POST.get('outrob1')
                    else:
                        f_cont.motivo = request.POST.get('motivob1')

                if request.POST.get('p'+str(pergunta.id)) == 'on':
                    f_cont.resposta = True
                else:
                    f_cont.resposta = False
                f_cont.save()


        if request.POST.get('bimestre_2') == '2':
            b2 = request.POST.get('bimestre2')
            perguntas = Pergunta.objects.filter(bimestref_id = b2).order_by('id')
            for pergunta in perguntas:
                form_resposta = RespostaForm(request.POST)
                if form_resposta.is_valid():
                    f_cont = form_resposta.save(commit=False)
                    f_cont.professor = Professor.objects.get(id=int(request.POST.get('professor')))
                    f_cont.pergunta = Pergunta.objects.get(id = int(pergunta.id))
                if request.POST.get('foi_possivelb2') == 'sim':
                    f_cont.foi_possivel = True
                else:
                    f_cont.foi_possivel = False
                    if request.POST.get('motivob2') == 'Outros':
                        f_cont.motivo = "Outros"
                        f_cont.outros = request.POST.get('outrob2')
                    else:
                        f_cont.motivo = request.POST.get('motivob2')

                if request.POST.get('p'+str(pergunta.id)) == 'on':
                    f_cont.resposta = True
                else:
                    f_cont.resposta = False
                f_cont.save()


        if request.POST.get('bimestre_3') == '3':
            b3 = request.POST.get('bimestre3')
            perguntas = Pergunta.objects.filter(bimestref_id = b3).order_by('id')
            for pergunta in perguntas:
                form_resposta = RespostaForm(request.POST)
                if form_resposta.is_valid():
                    f_cont = form_resposta.save(commit=False)
                    f_cont.professor = Professor.objects.get(id=int(request.POST.get('professor')))
                    f_cont.pergunta = Pergunta.objects.get(id = int(pergunta.id))
                if request.POST.get('foi_possivelb3') == 'sim':
                    f_cont.foi_possivel = True
                else:
                    f_cont.foi_possivel = False
                    if request.POST.get('motivob3') == 'Outros':
                        f_cont.motivo = "Outros"
                        f_cont.outros = request.POST.get('outrob3')
                    else:
                        f_cont.motivo = request.POST.get('motivob3')

                if request.POST.get('p'+str(pergunta.id)) == 'on':
                    f_cont.resposta = True
                else:
                    f_cont.resposta = False
                f_cont.save()

        if request.POST.get('bimestre_4') == '4':

            b4 = request.POST.get('bimestre4')
            perguntas = Pergunta.objects.filter(bimestref_id = b4).order_by('id')
            for pergunta in perguntas:
                form_resposta = RespostaForm(request.POST)
                if form_resposta.is_valid():
                    f_cont = form_resposta.save(commit=False)
                    f_cont.professor = Professor.objects.get(id=int(request.POST.get('professor')))
                    f_cont.pergunta = Pergunta.objects.get(id = int(pergunta.id))
                if request.POST.get('foi_possivelb4') == 'sim':
                    f_cont.foi_possivel = True
                else:
                    f_cont.foi_possivel = False
                    if request.POST.get('motivob4') == 'Outros':
                        f_cont.motivo = "Outros"
                        f_cont.outros = request.POST.get('outrob4')
                    else:
                        f_cont.motivo = request.POST.get('motivob4')

                if request.POST.get('p'+str(pergunta.id)) == 'on':
                    f_cont.resposta = True
                else:
                    f_cont.resposta = False
                f_cont.save()


        return render(request, "painel.html")
    else:
        return render(request, "painel.html")

#Funções para carregar os selects dinamicamente
@login_required
def getCoordenadorias(request):
    data = json.loads(request.body)
    jurisdicao_id = data["id"]
    coordenadorias = Coordenadoria.objects.filter(jurisdicao_id=jurisdicao_id)
    return JsonResponse(list(coordenadorias.values("id", "coordenadoria")), safe=False)

@login_required
def getEscolas(request):
    data = json.loads(request.body)
    coordenadoria_id = data["id"]
    escolas = Escola.objects.filter(coordenadoria_id=coordenadoria_id)
    return JsonResponse(list(escolas.values("id", "escola")), safe=False)

@login_required
def getTurnos(request):
    data = json.loads(request.body)
    escola_id = data["id"]
    turnos = Turno.objects.filter(escola_id=escola_id)
    return JsonResponse(list(turnos.values("id", "turno")), safe=False)

@login_required
def getSeries(request):
    data = json.loads(request.body)
    turno_id = data["id"]
    series = Serie.objects.filter(turno_id=turno_id)
    return JsonResponse(list(series.values("id", "serie")), safe=False)

@login_required
def getTurmas(request):
    data = json.loads(request.body)
    serie_id = data["id"]
    turmas = Turma.objects.filter(serie_id=serie_id)
    return JsonResponse(list(turmas.values("id", "turma")), safe=False)

@login_required
def getMaterias(request):

    data = json.loads(request.body)
    serie_id = data["id"]
    materias = Materia.objects.filter(serie_id=serie_id)
    return JsonResponse(list(materias.values("id", "materia")), safe=False)


@login_required
def getCumprimento(request):

    #serie 2
    serie_id_2 = 1
    materia_id_2= [1,2]

    #serie 2 b1
    s2_b1 = Bimestref.objects.raw('SELECT * FROM app_bimestref as b  where materiaf_id = %s and bimestre = "1"   or materiaf_id = %s and bimestre = "1"', [materia_id_2[0], materia_id_2[1]])
    perguntas_2_b1_1 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s2_b1[0].id])
    perguntas_2_b1_2 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s2_b1[1].id])
    qtd_perguntas_2_b1 = len(perguntas_2_b1_1) + len(perguntas_2_b1_2)
    respostas_2_b1 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b1_1[0].id,perguntas_2_b1_1[-1].id,perguntas_2_b1_2[0].id,perguntas_2_b1_2[-1].id])
    qtd_respostas_2_b1 = len(respostas_2_b1)
    professores_2_b1 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b1_1[0].id,perguntas_2_b1_1[-1].id,perguntas_2_b1_2[0].id,perguntas_2_b1_2[-1].id])
    qtd_professores_2_b1 = len(professores_2_b1)



    #serie 2 b2
    s2_b2 = Bimestref.objects.raw('SELECT * FROM app_bimestref as b  where materiaf_id = %s and bimestre = "2"   or materiaf_id = %s and bimestre = "2"', [materia_id_2[0], materia_id_2[1]])
    perguntas_2_b2_1 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s2_b2[0].id])
    perguntas_2_b2_2 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s2_b2[1].id])
    qtd_perguntas_2_b2 = len(perguntas_2_b2_1) + len(perguntas_2_b2_2)
    respostas_2_b2 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b2_1[0].id,perguntas_2_b2_1[-1].id,perguntas_2_b2_2[0].id,perguntas_2_b2_2[-1].id])
    qtd_respostas_2_b2 = len(respostas_2_b2)
    professores_2_b2 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b2_1[0].id,perguntas_2_b2_1[-1].id,perguntas_2_b2_2[0].id,perguntas_2_b2_2[-1].id])
    qtd_professores_2_b2 = len(professores_2_b2)



    #serie 2 b3
    s2_b3 = Bimestref.objects.raw('SELECT * FROM app_bimestref as b  where materiaf_id = %s and bimestre = "3"   or materiaf_id = %s and bimestre = "3"', [materia_id_2[0], materia_id_2[1]])
    perguntas_2_b3_1 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s2_b3[0].id])
    perguntas_2_b3_2 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s2_b3[1].id])
    qtd_perguntas_2_b3 = len(perguntas_2_b3_1) + len(perguntas_2_b3_2)
    respostas_2_b3 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b3_1[0].id,perguntas_2_b3_1[-1].id,perguntas_2_b3_2[0].id,perguntas_2_b3_2[-1].id])
    qtd_respostas_2_b3 = len(respostas_2_b3)
    professores_2_b3 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b3_1[0].id,perguntas_2_b3_1[-1].id,perguntas_2_b3_2[0].id,perguntas_2_b3_2[-1].id])
    qtd_professores_2_b3 = len(professores_2_b3)



    #serie 2 b4
    s2_b4 = Bimestref.objects.raw('SELECT * FROM app_bimestref as b  where materiaf_id = %s and bimestre = "4"   or materiaf_id = %s and bimestre = "4"', [materia_id_2[0], materia_id_2[1]])
    perguntas_2_b4_1 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s2_b4[0].id])
    perguntas_2_b4_2 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s2_b4[1].id])
    qtd_perguntas_2_b4 = len(perguntas_2_b4_1) + len(perguntas_2_b4_2)
    respostas_2_b4 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b4_1[0].id,perguntas_2_b4_1[-1].id,perguntas_2_b4_2[0].id,perguntas_2_b4_2[-1].id])
    qtd_respostas_2_b4 = len(respostas_2_b4)
    professores_2_b4 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b4_1[0].id,perguntas_2_b4_1[-1].id,perguntas_2_b4_2[0].id,perguntas_2_b4_2[-1].id])
    qtd_professores_2_b4 = len(professores_2_b4)



    #serie 5
    serie_id_5 = 2
    materia_id_5= [3,4]

    #serie 5 b1
    s5_b1 = Bimestref.objects.raw('SELECT * FROM app_bimestref as b  where materiaf_id = %s and bimestre = "1"   or materiaf_id = %s and bimestre = "1"', [materia_id_5[0], materia_id_5[1]])
    perguntas_5_b1_1 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s5_b1[0].id])
    perguntas_5_b1_2 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s5_b1[1].id])
    qtd_perguntas_5_b1 = len(perguntas_5_b1_1) + len(perguntas_5_b1_2)
    respostas_5_b1 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b1_1[0].id,perguntas_5_b1_1[-1].id,perguntas_5_b1_2[0].id,perguntas_5_b1_2[-1].id])
    qtd_respostas_5_b1 = len(respostas_5_b1)
    professores_5_b1 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b1_1[0].id,perguntas_5_b1_1[-1].id,perguntas_5_b1_2[0].id,perguntas_5_b1_2[-1].id])
    qtd_professores_5_b1 = len(professores_5_b1)



    #serie 5 b2
    s5_b2 = Bimestref.objects.raw('SELECT * FROM app_bimestref as b  where materiaf_id = %s and bimestre = "2"   or materiaf_id = %s and bimestre = "2"', [materia_id_5[0], materia_id_5[1]])
    perguntas_5_b2_1 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s5_b2[0].id])
    perguntas_5_b2_2 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s5_b2[1].id])
    qtd_perguntas_5_b2 = len(perguntas_5_b2_1) + len(perguntas_5_b2_2)
    respostas_5_b2 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b2_1[0].id,perguntas_5_b2_1[-1].id,perguntas_5_b2_2[0].id,perguntas_5_b2_2[-1].id])
    qtd_respostas_5_b2 = len(respostas_5_b2)
    professores_5_b2 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b2_1[0].id,perguntas_5_b2_1[-1].id,perguntas_5_b2_2[0].id,perguntas_5_b2_2[-1].id])
    qtd_professores_5_b2 = len(professores_5_b2)



    #serie 5 b3
    s5_b3 = Bimestref.objects.raw('SELECT * FROM app_bimestref as b  where materiaf_id = %s and bimestre = "3"   or materiaf_id = %s and bimestre = "3"', [materia_id_5[0], materia_id_5[1]])
    perguntas_5_b3_1 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s5_b3[0].id])
    perguntas_5_b3_2 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s5_b3[1].id])
    qtd_perguntas_5_b3 = len(perguntas_5_b3_1) + len(perguntas_5_b3_2)
    respostas_5_b3 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b3_1[0].id,perguntas_5_b3_1[-1].id,perguntas_5_b3_2[0].id,perguntas_5_b3_2[-1].id])
    qtd_respostas_5_b3 = len(respostas_5_b3)
    professores_5_b3 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b3_1[0].id,perguntas_5_b3_1[-1].id,perguntas_5_b3_2[0].id,perguntas_5_b3_2[-1].id])
    qtd_professores_5_b3 = len(professores_5_b3)



    #serie 5 b4
    s5_b4 = Bimestref.objects.raw('SELECT * FROM app_bimestref as b  where materiaf_id = %s and bimestre = "4"   or materiaf_id = %s and bimestre = "4"', [materia_id_5[0], materia_id_5[1]])
    perguntas_5_b4_1 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s5_b4[0].id])
    perguntas_5_b4_2 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s5_b4[1].id])
    qtd_perguntas_5_b4 = len(perguntas_5_b4_1) + len(perguntas_5_b4_2)
    respostas_5_b4 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b4_1[0].id,perguntas_5_b4_1[-1].id,perguntas_5_b4_2[0].id,perguntas_5_b4_2[-1].id])
    qtd_respostas_5_b4 = len(respostas_5_b4)
    professores_5_b4 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b4_1[0].id,perguntas_5_b4_1[-1].id,perguntas_5_b4_2[0].id,perguntas_5_b4_2[-1].id])
    qtd_professores_5_b4 = len(professores_5_b4)



    #serie 9
    serie_id_9 = 3
    materia_id_9= [5,6]

    #serie 9 b1
    s9_b1 = Bimestref.objects.raw('SELECT * FROM app_bimestref as b  where materiaf_id = %s and bimestre = "1"   or materiaf_id = %s and bimestre = "1"', [materia_id_9[0], materia_id_9[1]])
    perguntas_9_b1_1 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s9_b1[0].id])
    perguntas_9_b1_2 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s9_b1[1].id])
    qtd_perguntas_9_b1 = len(perguntas_9_b1_1) + len(perguntas_9_b1_2)
    respostas_9_b1 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b1_1[0].id,perguntas_9_b1_1[-1].id,perguntas_9_b1_2[0].id,perguntas_9_b1_2[-1].id])
    qtd_respostas_9_b1 = len(respostas_9_b1)
    professores_9_b1 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b1_1[0].id,perguntas_9_b1_1[-1].id,perguntas_9_b1_2[0].id,perguntas_9_b1_2[-1].id])
    qtd_professores_9_b1 = len(professores_9_b1)



    #serie 9 b2
    s9_b2 = Bimestref.objects.raw('SELECT * FROM app_bimestref as b  where materiaf_id = %s and bimestre = "2"   or materiaf_id = %s and bimestre = "2"', [materia_id_9[0], materia_id_9[1]])
    perguntas_9_b2_1 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s9_b2[0].id])
    perguntas_9_b2_2 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s9_b2[1].id])
    qtd_perguntas_9_b2 = len(perguntas_9_b2_1) + len(perguntas_9_b2_2)
    respostas_9_b2 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b2_1[0].id,perguntas_9_b2_1[-1].id,perguntas_9_b2_2[0].id,perguntas_9_b2_2[-1].id])
    qtd_respostas_9_b2 = len(respostas_9_b2)
    professores_9_b2 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b2_1[0].id,perguntas_9_b2_1[-1].id,perguntas_9_b2_2[0].id,perguntas_9_b2_2[-1].id])
    qtd_professores_9_b2 = len(professores_9_b2)



    #serie 9 b3
    s9_b3 = Bimestref.objects.raw('SELECT * FROM app_bimestref as b  where materiaf_id = %s and bimestre = "3"   or materiaf_id = %s and bimestre = "3"', [materia_id_9[0], materia_id_9[1]])
    perguntas_9_b3_1 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s9_b3[0].id])
    perguntas_9_b3_2 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s9_b3[1].id])
    qtd_perguntas_9_b3 = len(perguntas_9_b3_1) + len(perguntas_9_b3_2)
    respostas_9_b3 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b3_1[0].id,perguntas_9_b3_1[-1].id,perguntas_9_b3_2[0].id,perguntas_9_b3_2[-1].id])
    qtd_respostas_9_b3 = len(respostas_9_b3)
    professores_9_b3 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b3_1[0].id,perguntas_9_b3_1[-1].id,perguntas_9_b3_2[0].id,perguntas_9_b3_2[-1].id])
    qtd_professores_9_b3 = len(professores_9_b3)



    #serie 9 b4
    s9_b4 = Bimestref.objects.raw('SELECT * FROM app_bimestref as b  where materiaf_id = %s and bimestre = "4"   or materiaf_id = %s and bimestre = "4"', [materia_id_9[0], materia_id_9[1]])
    perguntas_9_b4_1 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s9_b4[0].id])
    perguntas_9_b4_2 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s9_b4[1].id])
    qtd_perguntas_9_b4 = len(perguntas_9_b4_1) + len(perguntas_9_b4_2)
    respostas_9_b4 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b4_1[0].id,perguntas_9_b4_1[-1].id,perguntas_9_b4_2[0].id,perguntas_9_b4_2[-1].id])
    qtd_respostas_9_b4 = len(respostas_9_b4)
    professores_9_b4 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b4_1[0].id,perguntas_9_b4_1[-1].id,perguntas_9_b4_2[0].id,perguntas_9_b4_2[-1].id])
    qtd_professores_9_b4 = len(professores_9_b4)




        #serie 3
    serie_id_3 = 4
    materia_id_3= [7,8]

    #serie 3 b1
    s3_b1 = Bimestref.objects.raw('SELECT * FROM app_bimestref as b  where materiaf_id = %s and bimestre = "1"   or materiaf_id = %s and bimestre = "1"', [materia_id_3[0], materia_id_3[1]])
    perguntas_3_b1_1 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s3_b1[0].id])
    perguntas_3_b1_2 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s3_b1[1].id])
    qtd_perguntas_3_b1 = len(perguntas_3_b1_1) + len(perguntas_3_b1_2)
    respostas_3_b1 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b1_1[0].id,perguntas_3_b1_1[-1].id,perguntas_3_b1_2[0].id,perguntas_3_b1_2[-1].id])
    qtd_respostas_3_b1 = len(respostas_3_b1)
    professores_3_b1 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b1_1[0].id,perguntas_3_b1_1[-1].id,perguntas_3_b1_2[0].id,perguntas_3_b1_2[-1].id])
    qtd_professores_3_b1 = len(professores_3_b1)




    #serie 3 b2
    s3_b2 = Bimestref.objects.raw('SELECT * FROM app_bimestref as b  where materiaf_id = %s and bimestre = "2"   or materiaf_id = %s and bimestre = "2"', [materia_id_3[0], materia_id_3[1]])
    perguntas_3_b2_1 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s3_b2[0].id])
    perguntas_3_b2_2 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s3_b2[1].id])
    qtd_perguntas_3_b2 = len(perguntas_3_b2_1) + len(perguntas_3_b2_2)
    respostas_3_b2 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b2_1[0].id,perguntas_3_b2_1[-1].id,perguntas_3_b2_2[0].id,perguntas_3_b2_2[-1].id])
    qtd_respostas_3_b2 = len(respostas_3_b2)
    professores_3_b2 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b2_1[0].id,perguntas_3_b2_1[-1].id,perguntas_3_b2_2[0].id,perguntas_3_b2_2[-1].id])
    qtd_professores_3_b2 = len(professores_3_b2)




    #serie 3 b3
    s3_b3 = Bimestref.objects.raw('SELECT * FROM app_bimestref as b  where materiaf_id = %s and bimestre = "3"   or materiaf_id = %s and bimestre = "3"', [materia_id_3[0], materia_id_3[1]])
    perguntas_3_b3_1 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s3_b3[0].id])
    perguntas_3_b3_2 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s3_b3[1].id])
    qtd_perguntas_3_b3 = len(perguntas_3_b3_1) + len(perguntas_3_b3_2)
    respostas_3_b3 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b3_1[0].id,perguntas_3_b3_1[-1].id,perguntas_3_b3_2[0].id,perguntas_3_b3_2[-1].id])
    qtd_respostas_3_b3 = len(respostas_3_b3)
    professores_3_b3 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b3_1[0].id,perguntas_3_b3_1[-1].id,perguntas_3_b3_2[0].id,perguntas_3_b3_2[-1].id])
    qtd_professores_3_b3 = len(professores_3_b3)



    #serie 3 b4
    s3_b4 = Bimestref.objects.raw('SELECT * FROM app_bimestref as b  where materiaf_id = %s and bimestre = "4"   or materiaf_id = %s and bimestre = "4"', [materia_id_3[0], materia_id_3[1]])
    perguntas_3_b4_1 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s3_b4[0].id])
    perguntas_3_b4_2 = Pergunta.objects.raw('SELECT * FROM app_pergunta as p  where p.bimestref_id = %s ', [s3_b4[1].id])
    qtd_perguntas_3_b4 = len(perguntas_3_b4_1) + len(perguntas_3_b4_2)
    respostas_3_b4 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b4_1[0].id,perguntas_3_b4_1[-1].id,perguntas_3_b4_2[0].id,perguntas_3_b4_2[-1].id])
    qtd_respostas_3_b4 = len(respostas_3_b4)
    professores_3_b4 = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1  or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b4_1[0].id,perguntas_3_b4_1[-1].id,perguntas_3_b4_2[0].id,perguntas_3_b4_2[-1].id])
    qtd_professores_3_b4 = len(professores_3_b4)


    #Cumprimento por Turnos

    #serie 2

    respostas_2_b1_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b1_1[0].id,perguntas_2_b1_1[-1].id,perguntas_2_b1_2[0].id,perguntas_2_b1_2[-1].id])
    qtd_respostas_2_b1_mat = len(respostas_2_b1_mat)
    professores_2_b1_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b1_1[0].id,perguntas_2_b1_1[-1].id,perguntas_2_b1_2[0].id,perguntas_2_b1_2[-1].id])
    qtd_professores_2_b1_mat = len(professores_2_b1_mat)

    respostas_2_b2_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b2_1[0].id,perguntas_2_b2_1[-1].id,perguntas_2_b2_2[0].id,perguntas_2_b2_2[-1].id])
    qtd_respostas_2_b2_mat = len(respostas_2_b2_mat)
    professores_2_b2_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b2_1[0].id,perguntas_2_b2_1[-1].id,perguntas_2_b2_2[0].id,perguntas_2_b2_2[-1].id])
    qtd_professores_2_b2_mat = len(professores_2_b2_mat)

    respostas_2_b3_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b3_1[0].id,perguntas_2_b3_1[-1].id,perguntas_2_b3_2[0].id,perguntas_2_b3_2[-1].id])
    qtd_respostas_2_b3_mat = len(respostas_2_b3_mat)
    professores_2_b3_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b3_1[0].id,perguntas_2_b3_1[-1].id,perguntas_2_b3_2[0].id,perguntas_2_b3_2[-1].id])
    qtd_professores_2_b3_mat = len(professores_2_b3_mat)

    respostas_2_b4_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b4_1[0].id,perguntas_2_b4_1[-1].id,perguntas_2_b4_2[0].id,perguntas_2_b4_2[-1].id])
    qtd_respostas_2_b4_mat = len(respostas_2_b4_mat)
    professores_2_b4_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b4_1[0].id,perguntas_2_b4_1[-1].id,perguntas_2_b4_2[0].id,perguntas_2_b4_2[-1].id])
    qtd_professores_2_b4_mat = len(professores_2_b4_mat)

    respostas_2_b1_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b1_1[0].id,perguntas_2_b1_1[-1].id,perguntas_2_b1_2[0].id,perguntas_2_b1_2[-1].id])
    qtd_respostas_2_b1_vesp = len(respostas_2_b1_vesp)
    professores_2_b1_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b1_1[0].id,perguntas_2_b1_1[-1].id,perguntas_2_b1_2[0].id,perguntas_2_b1_2[-1].id])
    qtd_professores_2_b1_vesp = len(professores_2_b1_vesp)

    respostas_2_b2_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b2_1[0].id,perguntas_2_b2_1[-1].id,perguntas_2_b2_2[0].id,perguntas_2_b2_2[-1].id])
    qtd_respostas_2_b2_vesp = len(respostas_2_b2_vesp)
    professores_2_b2_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b2_1[0].id,perguntas_2_b2_1[-1].id,perguntas_2_b2_2[0].id,perguntas_2_b2_2[-1].id])
    qtd_professores_2_b2_vesp = len(professores_2_b2_vesp)

    respostas_2_b3_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b3_1[0].id,perguntas_2_b3_1[-1].id,perguntas_2_b3_2[0].id,perguntas_2_b3_2[-1].id])
    qtd_respostas_2_b3_vesp = len(respostas_2_b3_vesp)
    professores_2_b3_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b3_1[0].id,perguntas_2_b3_1[-1].id,perguntas_2_b3_2[0].id,perguntas_2_b3_2[-1].id])
    qtd_professores_2_b3_vesp = len(professores_2_b3_vesp)

    respostas_2_b4_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b4_1[0].id,perguntas_2_b4_1[-1].id,perguntas_2_b4_2[0].id,perguntas_2_b4_2[-1].id])
    qtd_respostas_2_b4_vesp = len(respostas_2_b4_vesp)
    professores_2_b4_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b4_1[0].id,perguntas_2_b4_1[-1].id,perguntas_2_b4_2[0].id,perguntas_2_b4_2[-1].id])
    qtd_professores_2_b4_vesp = len(professores_2_b4_vesp)

    respostas_2_b1_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b1_1[0].id,perguntas_2_b1_1[-1].id,perguntas_2_b1_2[0].id,perguntas_2_b1_2[-1].id])
    qtd_respostas_2_b1_not = len(respostas_2_b1_not)
    professores_2_b1_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b1_1[0].id,perguntas_2_b1_1[-1].id,perguntas_2_b1_2[0].id,perguntas_2_b1_2[-1].id])
    qtd_professores_2_b1_not = len(professores_2_b1_not)

    respostas_2_b2_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b2_1[0].id,perguntas_2_b2_1[-1].id,perguntas_2_b2_2[0].id,perguntas_2_b2_2[-1].id])
    qtd_respostas_2_b2_not = len(respostas_2_b2_not)
    professores_2_b2_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b2_1[0].id,perguntas_2_b2_1[-1].id,perguntas_2_b2_2[0].id,perguntas_2_b2_2[-1].id])
    qtd_professores_2_b2_not = len(professores_2_b2_not)

    respostas_2_b3_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b3_1[0].id,perguntas_2_b3_1[-1].id,perguntas_2_b3_2[0].id,perguntas_2_b3_2[-1].id])
    qtd_respostas_2_b3_not = len(respostas_2_b3_not)
    professores_2_b3_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b3_1[0].id,perguntas_2_b3_1[-1].id,perguntas_2_b3_2[0].id,perguntas_2_b3_2[-1].id])
    qtd_professores_2_b3_not = len(professores_2_b3_not)

    respostas_2_b4_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b4_1[0].id,perguntas_2_b4_1[-1].id,perguntas_2_b4_2[0].id,perguntas_2_b4_2[-1].id])
    qtd_respostas_2_b4_not = len(respostas_2_b4_not)
    professores_2_b4_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b4_1[0].id,perguntas_2_b4_1[-1].id,perguntas_2_b4_2[0].id,perguntas_2_b4_2[-1].id])
    qtd_professores_2_b4_not = len(professores_2_b4_not)

    respostas_2_b1_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b1_1[0].id,perguntas_2_b1_1[-1].id,perguntas_2_b1_2[0].id,perguntas_2_b1_2[-1].id])
    qtd_respostas_2_b1_integ = len(respostas_2_b1_integ)
    professores_2_b1_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b1_1[0].id,perguntas_2_b1_1[-1].id,perguntas_2_b1_2[0].id,perguntas_2_b1_2[-1].id])
    qtd_professores_2_b1_integ = len(professores_2_b1_integ)

    respostas_2_b2_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b2_1[0].id,perguntas_2_b2_1[-1].id,perguntas_2_b2_2[0].id,perguntas_2_b2_2[-1].id])
    qtd_respostas_2_b2_integ = len(respostas_2_b2_integ)
    professores_2_b2_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b2_1[0].id,perguntas_2_b2_1[-1].id,perguntas_2_b2_2[0].id,perguntas_2_b2_2[-1].id])
    qtd_professores_2_b2_integ = len(professores_2_b2_integ)

    respostas_2_b3_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b3_1[0].id,perguntas_2_b3_1[-1].id,perguntas_2_b3_2[0].id,perguntas_2_b3_2[-1].id])
    qtd_respostas_2_b3_integ = len(respostas_2_b3_integ)
    professores_2_b3_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b3_1[0].id,perguntas_2_b3_1[-1].id,perguntas_2_b3_2[0].id,perguntas_2_b3_2[-1].id])
    qtd_professores_2_b3_integ = len(professores_2_b3_integ)

    respostas_2_b4_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b4_1[0].id,perguntas_2_b4_1[-1].id,perguntas_2_b4_2[0].id,perguntas_2_b4_2[-1].id])
    qtd_respostas_2_b4_integ = len(respostas_2_b4_integ)
    professores_2_b4_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b4_1[0].id,perguntas_2_b4_1[-1].id,perguntas_2_b4_2[0].id,perguntas_2_b4_2[-1].id])
    qtd_professores_2_b4_integ = len(professores_2_b4_integ)

# serie 5

    respostas_5_b1_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b1_1[0].id,perguntas_5_b1_1[-1].id,perguntas_5_b1_2[0].id,perguntas_5_b1_2[-1].id])
    qtd_respostas_5_b1_mat = len(respostas_5_b1_mat)
    professores_5_b1_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b1_1[0].id,perguntas_5_b1_1[-1].id,perguntas_5_b1_2[0].id,perguntas_5_b1_2[-1].id])
    qtd_professores_5_b1_mat = len(professores_5_b1_mat)

    respostas_5_b2_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b2_1[0].id,perguntas_5_b2_1[-1].id,perguntas_5_b2_2[0].id,perguntas_5_b2_2[-1].id])
    qtd_respostas_5_b2_mat = len(respostas_5_b2_mat)
    professores_5_b2_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b2_1[0].id,perguntas_5_b2_1[-1].id,perguntas_5_b2_2[0].id,perguntas_5_b2_2[-1].id])
    qtd_professores_5_b2_mat = len(professores_5_b2_mat)

    respostas_5_b3_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b3_1[0].id,perguntas_5_b3_1[-1].id,perguntas_5_b3_2[0].id,perguntas_5_b3_2[-1].id])
    qtd_respostas_5_b3_mat = len(respostas_5_b3_mat)
    professores_5_b3_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b3_1[0].id,perguntas_5_b3_1[-1].id,perguntas_5_b3_2[0].id,perguntas_5_b3_2[-1].id])
    qtd_professores_5_b3_mat = len(professores_5_b3_mat)

    respostas_5_b4_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b4_1[0].id,perguntas_5_b4_1[-1].id,perguntas_5_b4_2[0].id,perguntas_5_b4_2[-1].id])
    qtd_respostas_5_b4_mat = len(respostas_5_b4_mat)
    professores_5_b4_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b4_1[0].id,perguntas_5_b4_1[-1].id,perguntas_5_b4_2[0].id,perguntas_5_b4_2[-1].id])
    qtd_professores_5_b4_mat = len(professores_5_b4_mat)

    respostas_5_b1_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b1_1[0].id,perguntas_5_b1_1[-1].id,perguntas_5_b1_2[0].id,perguntas_5_b1_2[-1].id])
    qtd_respostas_5_b1_vesp = len(respostas_5_b1_vesp)
    professores_5_b1_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b1_1[0].id,perguntas_5_b1_1[-1].id,perguntas_5_b1_2[0].id,perguntas_5_b1_2[-1].id])
    qtd_professores_5_b1_vesp = len(professores_5_b1_vesp)

    respostas_5_b2_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b2_1[0].id,perguntas_5_b2_1[-1].id,perguntas_5_b2_2[0].id,perguntas_5_b2_2[-1].id])
    qtd_respostas_5_b2_vesp = len(respostas_5_b2_vesp)
    professores_5_b2_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b2_1[0].id,perguntas_5_b2_1[-1].id,perguntas_5_b2_2[0].id,perguntas_5_b2_2[-1].id])
    qtd_professores_5_b2_vesp = len(professores_5_b2_vesp)

    respostas_5_b3_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b3_1[0].id,perguntas_5_b3_1[-1].id,perguntas_5_b3_2[0].id,perguntas_5_b3_2[-1].id])
    qtd_respostas_5_b3_vesp = len(respostas_5_b3_vesp)
    professores_5_b3_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b3_1[0].id,perguntas_5_b3_1[-1].id,perguntas_5_b3_2[0].id,perguntas_5_b3_2[-1].id])
    qtd_professores_5_b3_vesp = len(professores_5_b3_vesp)

    respostas_5_b4_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b4_1[0].id,perguntas_5_b4_1[-1].id,perguntas_5_b4_2[0].id,perguntas_5_b4_2[-1].id])
    qtd_respostas_5_b4_vesp = len(respostas_5_b4_vesp)
    professores_5_b4_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b4_1[0].id,perguntas_5_b4_1[-1].id,perguntas_5_b4_2[0].id,perguntas_5_b4_2[-1].id])
    qtd_professores_5_b4_vesp = len(professores_5_b4_vesp)

    respostas_5_b1_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b1_1[0].id,perguntas_5_b1_1[-1].id,perguntas_5_b1_2[0].id,perguntas_5_b1_2[-1].id])
    qtd_respostas_5_b1_not = len(respostas_5_b1_not)
    professores_5_b1_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b1_1[0].id,perguntas_5_b1_1[-1].id,perguntas_5_b1_2[0].id,perguntas_5_b1_2[-1].id])
    qtd_professores_5_b1_not = len(professores_5_b1_not)

    respostas_5_b2_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b2_1[0].id,perguntas_5_b2_1[-1].id,perguntas_5_b2_2[0].id,perguntas_5_b2_2[-1].id])
    qtd_respostas_5_b2_not = len(respostas_5_b2_not)
    professores_5_b2_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b2_1[0].id,perguntas_5_b2_1[-1].id,perguntas_5_b2_2[0].id,perguntas_5_b2_2[-1].id])
    qtd_professores_5_b2_not = len(professores_5_b2_not)

    respostas_5_b3_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b3_1[0].id,perguntas_5_b3_1[-1].id,perguntas_5_b3_2[0].id,perguntas_5_b3_2[-1].id])
    qtd_respostas_5_b3_not = len(respostas_5_b3_not)
    professores_5_b3_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b3_1[0].id,perguntas_5_b3_1[-1].id,perguntas_5_b3_2[0].id,perguntas_5_b3_2[-1].id])
    qtd_professores_5_b3_not = len(professores_5_b3_not)

    respostas_5_b4_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b4_1[0].id,perguntas_5_b4_1[-1].id,perguntas_5_b4_2[0].id,perguntas_5_b4_2[-1].id])
    qtd_respostas_5_b4_not = len(respostas_5_b4_not)
    professores_5_b4_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b4_1[0].id,perguntas_5_b4_1[-1].id,perguntas_5_b4_2[0].id,perguntas_5_b4_2[-1].id])
    qtd_professores_5_b4_not = len(professores_5_b4_not)

    respostas_5_b1_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b1_1[0].id,perguntas_5_b1_1[-1].id,perguntas_5_b1_2[0].id,perguntas_5_b1_2[-1].id])
    qtd_respostas_5_b1_integ = len(respostas_5_b1_integ)
    professores_5_b1_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b1_1[0].id,perguntas_5_b1_1[-1].id,perguntas_5_b1_2[0].id,perguntas_5_b1_2[-1].id])
    qtd_professores_5_b1_integ = len(professores_5_b1_integ)

    respostas_5_b2_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b2_1[0].id,perguntas_5_b2_1[-1].id,perguntas_5_b2_2[0].id,perguntas_5_b2_2[-1].id])
    qtd_respostas_5_b2_integ = len(respostas_5_b2_integ)
    professores_5_b2_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b2_1[0].id,perguntas_5_b2_1[-1].id,perguntas_5_b2_2[0].id,perguntas_5_b2_2[-1].id])
    qtd_professores_5_b2_integ = len(professores_5_b2_integ)

    respostas_5_b3_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b3_1[0].id,perguntas_5_b3_1[-1].id,perguntas_5_b3_2[0].id,perguntas_5_b3_2[-1].id])
    qtd_respostas_5_b3_integ = len(respostas_5_b3_integ)
    professores_5_b3_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b3_1[0].id,perguntas_5_b3_1[-1].id,perguntas_5_b3_2[0].id,perguntas_5_b3_2[-1].id])
    qtd_professores_5_b3_integ = len(professores_5_b3_integ)

    respostas_5_b4_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b4_1[0].id,perguntas_5_b4_1[-1].id,perguntas_5_b4_2[0].id,perguntas_5_b4_2[-1].id])
    qtd_respostas_5_b4_integ = len(respostas_5_b4_integ)
    professores_5_b4_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b4_1[0].id,perguntas_5_b4_1[-1].id,perguntas_5_b4_2[0].id,perguntas_5_b4_2[-1].id])
    qtd_professores_5_b4_integ = len(professores_5_b4_integ)

# serie 9

    respostas_9_b1_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b1_1[0].id,perguntas_9_b1_1[-1].id,perguntas_9_b1_2[0].id,perguntas_9_b1_2[-1].id])
    qtd_respostas_9_b1_mat = len(respostas_9_b1_mat)
    professores_9_b1_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b1_1[0].id,perguntas_9_b1_1[-1].id,perguntas_9_b1_2[0].id,perguntas_9_b1_2[-1].id])
    qtd_professores_9_b1_mat = len(professores_9_b1_mat)

    respostas_9_b2_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b2_1[0].id,perguntas_9_b2_1[-1].id,perguntas_9_b2_2[0].id,perguntas_9_b2_2[-1].id])
    qtd_respostas_9_b2_mat = len(respostas_9_b2_mat)
    professores_9_b2_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b2_1[0].id,perguntas_9_b2_1[-1].id,perguntas_9_b2_2[0].id,perguntas_9_b2_2[-1].id])
    qtd_professores_9_b2_mat = len(professores_9_b2_mat)

    respostas_9_b3_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b3_1[0].id,perguntas_9_b3_1[-1].id,perguntas_9_b3_2[0].id,perguntas_9_b3_2[-1].id])
    qtd_respostas_9_b3_mat = len(respostas_9_b3_mat)
    professores_9_b3_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b3_1[0].id,perguntas_9_b3_1[-1].id,perguntas_9_b3_2[0].id,perguntas_9_b3_2[-1].id])
    qtd_professores_9_b3_mat = len(professores_9_b3_mat)

    respostas_9_b4_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b4_1[0].id,perguntas_9_b4_1[-1].id,perguntas_9_b4_2[0].id,perguntas_9_b4_2[-1].id])
    qtd_respostas_9_b4_mat = len(respostas_9_b4_mat)
    professores_9_b4_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b4_1[0].id,perguntas_9_b4_1[-1].id,perguntas_9_b4_2[0].id,perguntas_9_b4_2[-1].id])
    qtd_professores_9_b4_mat = len(professores_9_b4_mat)

    respostas_9_b1_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b1_1[0].id,perguntas_9_b1_1[-1].id,perguntas_9_b1_2[0].id,perguntas_9_b1_2[-1].id])
    qtd_respostas_9_b1_vesp = len(respostas_9_b1_vesp)
    professores_9_b1_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b1_1[0].id,perguntas_9_b1_1[-1].id,perguntas_9_b1_2[0].id,perguntas_9_b1_2[-1].id])
    qtd_professores_9_b1_vesp = len(professores_9_b1_vesp)

    respostas_9_b2_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b2_1[0].id,perguntas_9_b2_1[-1].id,perguntas_9_b2_2[0].id,perguntas_9_b2_2[-1].id])
    qtd_respostas_9_b2_vesp = len(respostas_9_b2_vesp)
    professores_9_b2_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b2_1[0].id,perguntas_9_b2_1[-1].id,perguntas_9_b2_2[0].id,perguntas_9_b2_2[-1].id])
    qtd_professores_9_b2_vesp = len(professores_9_b2_vesp)

    respostas_9_b3_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b3_1[0].id,perguntas_9_b3_1[-1].id,perguntas_9_b3_2[0].id,perguntas_9_b3_2[-1].id])
    qtd_respostas_9_b3_vesp = len(respostas_9_b3_vesp)
    professores_9_b3_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b3_1[0].id,perguntas_9_b3_1[-1].id,perguntas_9_b3_2[0].id,perguntas_9_b3_2[-1].id])
    qtd_professores_9_b3_vesp = len(professores_9_b3_vesp)

    respostas_9_b4_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b4_1[0].id,perguntas_9_b4_1[-1].id,perguntas_9_b4_2[0].id,perguntas_9_b4_2[-1].id])
    qtd_respostas_9_b4_vesp = len(respostas_9_b4_vesp)
    professores_9_b4_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b4_1[0].id,perguntas_9_b4_1[-1].id,perguntas_9_b4_2[0].id,perguntas_9_b4_2[-1].id])
    qtd_professores_9_b4_vesp = len(professores_9_b4_vesp)

    respostas_9_b1_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b1_1[0].id,perguntas_9_b1_1[-1].id,perguntas_9_b1_2[0].id,perguntas_9_b1_2[-1].id])
    qtd_respostas_9_b1_not = len(respostas_9_b1_not)
    professores_9_b1_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b1_1[0].id,perguntas_9_b1_1[-1].id,perguntas_9_b1_2[0].id,perguntas_9_b1_2[-1].id])
    qtd_professores_9_b1_not = len(professores_9_b1_not)

    respostas_9_b2_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b2_1[0].id,perguntas_9_b2_1[-1].id,perguntas_9_b2_2[0].id,perguntas_9_b2_2[-1].id])
    qtd_respostas_9_b2_not = len(respostas_9_b2_not)
    professores_9_b2_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b2_1[0].id,perguntas_9_b2_1[-1].id,perguntas_9_b2_2[0].id,perguntas_9_b2_2[-1].id])
    qtd_professores_9_b2_not = len(professores_9_b2_not)

    respostas_9_b3_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b3_1[0].id,perguntas_9_b3_1[-1].id,perguntas_9_b3_2[0].id,perguntas_9_b3_2[-1].id])
    qtd_respostas_9_b3_not = len(respostas_9_b3_not)
    professores_9_b3_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b3_1[0].id,perguntas_9_b3_1[-1].id,perguntas_9_b3_2[0].id,perguntas_9_b3_2[-1].id])
    qtd_professores_9_b3_not = len(professores_9_b3_not)

    respostas_9_b4_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b4_1[0].id,perguntas_9_b4_1[-1].id,perguntas_9_b4_2[0].id,perguntas_9_b4_2[-1].id])
    qtd_respostas_9_b4_not = len(respostas_9_b4_not)
    professores_9_b4_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b4_1[0].id,perguntas_9_b4_1[-1].id,perguntas_9_b4_2[0].id,perguntas_9_b4_2[-1].id])
    qtd_professores_9_b4_not = len(professores_9_b4_not)

    respostas_9_b1_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b1_1[0].id,perguntas_9_b1_1[-1].id,perguntas_9_b1_2[0].id,perguntas_9_b1_2[-1].id])
    qtd_respostas_9_b1_integ = len(respostas_9_b1_integ)
    professores_9_b1_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b1_1[0].id,perguntas_9_b1_1[-1].id,perguntas_9_b1_2[0].id,perguntas_9_b1_2[-1].id])
    qtd_professores_9_b1_integ = len(professores_9_b1_integ)

    respostas_9_b2_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b2_1[0].id,perguntas_9_b2_1[-1].id,perguntas_9_b2_2[0].id,perguntas_9_b2_2[-1].id])
    qtd_respostas_9_b2_integ = len(respostas_9_b2_integ)
    professores_9_b2_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b2_1[0].id,perguntas_9_b2_1[-1].id,perguntas_9_b2_2[0].id,perguntas_9_b2_2[-1].id])
    qtd_professores_9_b2_integ = len(professores_9_b2_integ)

    respostas_9_b3_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b3_1[0].id,perguntas_9_b3_1[-1].id,perguntas_9_b3_2[0].id,perguntas_9_b3_2[-1].id])
    qtd_respostas_9_b3_integ = len(respostas_9_b3_integ)
    professores_9_b3_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b3_1[0].id,perguntas_9_b3_1[-1].id,perguntas_9_b3_2[0].id,perguntas_9_b3_2[-1].id])
    qtd_professores_9_b3_integ = len(professores_9_b3_integ)

    respostas_9_b4_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b4_1[0].id,perguntas_9_b4_1[-1].id,perguntas_9_b4_2[0].id,perguntas_9_b4_2[-1].id])
    qtd_respostas_9_b4_integ = len(respostas_9_b4_integ)
    professores_9_b4_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b4_1[0].id,perguntas_9_b4_1[-1].id,perguntas_9_b4_2[0].id,perguntas_9_b4_2[-1].id])
    qtd_professores_9_b4_integ = len(professores_9_b4_integ)

# serie 3

    respostas_3_b1_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b1_1[0].id,perguntas_3_b1_1[-1].id,perguntas_3_b1_2[0].id,perguntas_3_b1_2[-1].id])
    qtd_respostas_3_b1_mat = len(respostas_3_b1_mat)
    professores_3_b1_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b1_1[0].id,perguntas_3_b1_1[-1].id,perguntas_3_b1_2[0].id,perguntas_3_b1_2[-1].id])
    qtd_professores_3_b1_mat = len(professores_3_b1_mat)

    respostas_3_b2_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b2_1[0].id,perguntas_3_b2_1[-1].id,perguntas_3_b2_2[0].id,perguntas_3_b2_2[-1].id])
    qtd_respostas_3_b2_mat = len(respostas_3_b2_mat)
    professores_3_b2_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b2_1[0].id,perguntas_3_b2_1[-1].id,perguntas_3_b2_2[0].id,perguntas_3_b2_2[-1].id])
    qtd_professores_3_b2_mat = len(professores_3_b2_mat)

    respostas_3_b3_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b3_1[0].id,perguntas_3_b3_1[-1].id,perguntas_3_b3_2[0].id,perguntas_3_b3_2[-1].id])
    qtd_respostas_3_b3_mat = len(respostas_3_b3_mat)
    professores_3_b3_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b3_1[0].id,perguntas_3_b3_1[-1].id,perguntas_3_b3_2[0].id,perguntas_3_b3_2[-1].id])
    qtd_professores_3_b3_mat = len(professores_3_b3_mat)

    respostas_3_b4_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b4_1[0].id,perguntas_3_b4_1[-1].id,perguntas_3_b4_2[0].id,perguntas_3_b4_2[-1].id])
    qtd_respostas_3_b4_mat = len(respostas_3_b4_mat)
    professores_3_b4_mat = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Matutino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b4_1[0].id,perguntas_3_b4_1[-1].id,perguntas_3_b4_2[0].id,perguntas_3_b4_2[-1].id])
    qtd_professores_3_b4_mat = len(professores_3_b4_mat)

    respostas_3_b1_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b1_1[0].id,perguntas_3_b1_1[-1].id,perguntas_3_b1_2[0].id,perguntas_3_b1_2[-1].id])
    qtd_respostas_3_b1_vesp = len(respostas_3_b1_vesp)
    professores_3_b1_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b1_1[0].id,perguntas_3_b1_1[-1].id,perguntas_3_b1_2[0].id,perguntas_3_b1_2[-1].id])
    qtd_professores_3_b1_vesp = len(professores_3_b1_vesp)

    respostas_3_b2_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b2_1[0].id,perguntas_3_b2_1[-1].id,perguntas_3_b2_2[0].id,perguntas_3_b2_2[-1].id])
    qtd_respostas_3_b2_vesp = len(respostas_3_b2_vesp)
    professores_3_b2_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b2_1[0].id,perguntas_3_b2_1[-1].id,perguntas_3_b2_2[0].id,perguntas_3_b2_2[-1].id])
    qtd_professores_3_b2_vesp = len(professores_3_b2_vesp)

    respostas_3_b3_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b3_1[0].id,perguntas_3_b3_1[-1].id,perguntas_3_b3_2[0].id,perguntas_3_b3_2[-1].id])
    qtd_respostas_3_b3_vesp = len(respostas_3_b3_vesp)
    professores_3_b3_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b3_1[0].id,perguntas_3_b3_1[-1].id,perguntas_3_b3_2[0].id,perguntas_3_b3_2[-1].id])
    qtd_professores_3_b3_vesp = len(professores_3_b3_vesp)

    respostas_3_b4_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b4_1[0].id,perguntas_3_b4_1[-1].id,perguntas_3_b4_2[0].id,perguntas_3_b4_2[-1].id])
    qtd_respostas_3_b4_vesp = len(respostas_3_b4_vesp)
    professores_3_b4_vesp = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Vespertino" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b4_1[0].id,perguntas_3_b4_1[-1].id,perguntas_3_b4_2[0].id,perguntas_3_b4_2[-1].id])
    qtd_professores_3_b4_vesp = len(professores_3_b4_vesp)

    respostas_3_b1_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b1_1[0].id,perguntas_3_b1_1[-1].id,perguntas_3_b1_2[0].id,perguntas_3_b1_2[-1].id])
    qtd_respostas_3_b1_not = len(respostas_3_b1_not)
    professores_3_b1_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b1_1[0].id,perguntas_3_b1_1[-1].id,perguntas_3_b1_2[0].id,perguntas_3_b1_2[-1].id])
    qtd_professores_3_b1_not = len(professores_3_b1_not)

    respostas_3_b2_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b2_1[0].id,perguntas_3_b2_1[-1].id,perguntas_3_b2_2[0].id,perguntas_3_b2_2[-1].id])
    qtd_respostas_3_b2_not = len(respostas_3_b2_not)
    professores_3_b2_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b2_1[0].id,perguntas_3_b2_1[-1].id,perguntas_3_b2_2[0].id,perguntas_3_b2_2[-1].id])
    qtd_professores_3_b2_not = len(professores_3_b2_not)

    respostas_3_b3_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b3_1[0].id,perguntas_3_b3_1[-1].id,perguntas_3_b3_2[0].id,perguntas_3_b3_2[-1].id])
    qtd_respostas_3_b3_not = len(respostas_3_b3_not)
    professores_3_b3_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b3_1[0].id,perguntas_3_b3_1[-1].id,perguntas_3_b3_2[0].id,perguntas_3_b3_2[-1].id])
    qtd_professores_3_b3_not = len(professores_3_b3_not)

    respostas_3_b4_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b4_1[0].id,perguntas_3_b4_1[-1].id,perguntas_3_b4_2[0].id,perguntas_3_b4_2[-1].id])
    qtd_respostas_3_b4_not = len(respostas_3_b4_not)
    professores_3_b4_not = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Noturno" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b4_1[0].id,perguntas_3_b4_1[-1].id,perguntas_3_b4_2[0].id,perguntas_3_b4_2[-1].id])
    qtd_professores_3_b4_not = len(professores_3_b4_not)

    respostas_3_b1_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b1_1[0].id,perguntas_3_b1_1[-1].id,perguntas_3_b1_2[0].id,perguntas_3_b1_2[-1].id])
    qtd_respostas_3_b1_integ = len(respostas_3_b1_integ)
    professores_3_b1_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b1_1[0].id,perguntas_3_b1_1[-1].id,perguntas_3_b1_2[0].id,perguntas_3_b1_2[-1].id])
    qtd_professores_3_b1_integ = len(professores_3_b1_integ)

    respostas_3_b2_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b2_1[0].id,perguntas_3_b2_1[-1].id,perguntas_3_b2_2[0].id,perguntas_3_b2_2[-1].id])
    qtd_respostas_3_b2_integ = len(respostas_3_b2_integ)
    professores_3_b2_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b2_1[0].id,perguntas_3_b2_1[-1].id,perguntas_3_b2_2[0].id,perguntas_3_b2_2[-1].id])
    qtd_professores_3_b2_integ = len(professores_3_b2_integ)

    respostas_3_b3_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b3_1[0].id,perguntas_3_b3_1[-1].id,perguntas_3_b3_2[0].id,perguntas_3_b3_2[-1].id])
    qtd_respostas_3_b3_integ = len(respostas_3_b3_integ)
    professores_3_b3_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b3_1[0].id,perguntas_3_b3_1[-1].id,perguntas_3_b3_2[0].id,perguntas_3_b3_2[-1].id])
    qtd_professores_3_b3_integ = len(professores_3_b3_integ)

    respostas_3_b4_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b4_1[0].id,perguntas_3_b4_1[-1].id,perguntas_3_b4_2[0].id,perguntas_3_b4_2[-1].id])
    qtd_respostas_3_b4_integ = len(respostas_3_b4_integ)
    professores_3_b4_integ = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id join app_turno as t on t.id = p.turno_id where t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 or t.turno = "Integral" and r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b4_1[0].id,perguntas_3_b4_1[-1].id,perguntas_3_b4_2[0].id,perguntas_3_b4_2[-1].id])
    qtd_professores_3_b4_integ = len(professores_3_b4_integ)


    #cumprimento jurisdicao

    respostas_2_b1_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 order by professor_id',[perguntas_2_b1_1[0].id,perguntas_2_b1_1[-1].id,perguntas_2_b1_2[0].id,perguntas_2_b1_2[-1].id])
    qtd_respostas_2_b1_cap = len(respostas_2_b1_cap)
    professores_2_b1_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 group by professor_id',[perguntas_2_b1_1[0].id,perguntas_2_b1_1[-1].id,perguntas_2_b1_2[0].id,perguntas_2_b1_2[-1].id])
    qtd_professores_2_b1_cap = len(professores_2_b1_cap)

    respostas_2_b1_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 order by professor_id',[perguntas_2_b1_1[0].id,perguntas_2_b1_1[-1].id,perguntas_2_b1_2[0].id,perguntas_2_b1_2[-1].id])
    qtd_respostas_2_b1_int = len(respostas_2_b1_int)
    professores_2_b1_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 group by professor_id',[perguntas_2_b1_1[0].id,perguntas_2_b1_1[-1].id,perguntas_2_b1_2[0].id,perguntas_2_b1_2[-1].id])
    qtd_professores_2_b1_int = len(professores_2_b1_int)

    respostas_2_b2_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 order by professor_id',[perguntas_2_b2_1[0].id,perguntas_2_b2_1[-1].id,perguntas_2_b2_2[0].id,perguntas_2_b2_2[-1].id])
    qtd_respostas_2_b2_cap = len(respostas_2_b2_cap)
    professores_2_b2_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 group by professor_id',[perguntas_2_b2_1[0].id,perguntas_2_b2_1[-1].id,perguntas_2_b2_2[0].id,perguntas_2_b2_2[-1].id])
    qtd_professores_2_b2_cap = len(professores_2_b2_cap)

    respostas_2_b2_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 order by professor_id',[perguntas_2_b2_1[0].id,perguntas_2_b2_1[-1].id,perguntas_2_b2_2[0].id,perguntas_2_b2_2[-1].id])
    qtd_respostas_2_b2_int = len(respostas_2_b2_int)
    professores_2_b2_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 group by professor_id',[perguntas_2_b2_1[0].id,perguntas_2_b2_1[-1].id,perguntas_2_b2_2[0].id,perguntas_2_b2_2[-1].id])
    qtd_professores_2_b2_int = len(professores_2_b2_int)

    respostas_2_b3_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 order by professor_id',[perguntas_2_b3_1[0].id,perguntas_2_b3_1[-1].id,perguntas_2_b3_2[0].id,perguntas_2_b3_2[-1].id])
    qtd_respostas_2_b3_cap = len(respostas_2_b3_cap)
    professores_2_b3_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 group by professor_id',[perguntas_2_b3_1[0].id,perguntas_2_b3_1[-1].id,perguntas_2_b3_2[0].id,perguntas_2_b3_2[-1].id])
    qtd_professores_2_b3_cap = len(professores_2_b3_cap)

    respostas_2_b3_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 order by professor_id',[perguntas_2_b3_1[0].id,perguntas_2_b3_1[-1].id,perguntas_2_b3_2[0].id,perguntas_2_b3_2[-1].id])
    qtd_respostas_2_b3_int = len(respostas_2_b3_int)
    professores_2_b3_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 group by professor_id',[perguntas_2_b3_1[0].id,perguntas_2_b3_1[-1].id,perguntas_2_b3_2[0].id,perguntas_2_b3_2[-1].id])
    qtd_professores_2_b3_int = len(professores_2_b3_int)

    respostas_2_b4_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 order by professor_id',[perguntas_2_b4_1[0].id,perguntas_2_b4_1[-1].id,perguntas_2_b4_2[0].id,perguntas_2_b4_2[-1].id])
    qtd_respostas_2_b4_cap = len(respostas_2_b4_cap)
    professores_2_b4_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 group by professor_id',[perguntas_2_b4_1[0].id,perguntas_2_b4_1[-1].id,perguntas_2_b4_2[0].id,perguntas_2_b4_2[-1].id])
    qtd_professores_2_b4_cap = len(professores_2_b4_cap)

    respostas_2_b4_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 order by professor_id',[perguntas_2_b4_1[0].id,perguntas_2_b4_1[-1].id,perguntas_2_b4_2[0].id,perguntas_2_b4_2[-1].id])
    qtd_respostas_2_b4_int = len(respostas_2_b4_int)
    professores_2_b4_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 group by professor_id',[perguntas_2_b4_1[0].id,perguntas_2_b4_1[-1].id,perguntas_2_b4_2[0].id,perguntas_2_b4_2[-1].id])
    qtd_professores_2_b4_int = len(professores_2_b4_int)



    respostas_5_b1_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 order by professor_id',[perguntas_5_b1_1[0].id,perguntas_5_b1_1[-1].id,perguntas_5_b1_2[0].id,perguntas_5_b1_2[-1].id])
    qtd_respostas_5_b1_cap = len(respostas_5_b1_cap)
    professores_5_b1_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 group by professor_id',[perguntas_5_b1_1[0].id,perguntas_5_b1_1[-1].id,perguntas_5_b1_2[0].id,perguntas_5_b1_2[-1].id])
    qtd_professores_5_b1_cap = len(professores_5_b1_cap)

    respostas_5_b1_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 order by professor_id',[perguntas_5_b1_1[0].id,perguntas_5_b1_1[-1].id,perguntas_5_b1_2[0].id,perguntas_5_b1_2[-1].id])
    qtd_respostas_5_b1_int = len(respostas_5_b1_int)
    professores_5_b1_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 group by professor_id',[perguntas_5_b1_1[0].id,perguntas_5_b1_1[-1].id,perguntas_5_b1_2[0].id,perguntas_5_b1_2[-1].id])
    qtd_professores_5_b1_int = len(professores_5_b1_int)

    respostas_5_b2_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 order by professor_id',[perguntas_5_b2_1[0].id,perguntas_5_b2_1[-1].id,perguntas_5_b2_2[0].id,perguntas_5_b2_2[-1].id])
    qtd_respostas_5_b2_cap = len(respostas_5_b2_cap)
    professores_5_b2_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 group by professor_id',[perguntas_5_b2_1[0].id,perguntas_5_b2_1[-1].id,perguntas_5_b2_2[0].id,perguntas_5_b2_2[-1].id])
    qtd_professores_5_b2_cap = len(professores_5_b2_cap)

    respostas_5_b2_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 order by professor_id',[perguntas_5_b2_1[0].id,perguntas_5_b2_1[-1].id,perguntas_5_b2_2[0].id,perguntas_5_b2_2[-1].id])
    qtd_respostas_5_b2_int = len(respostas_5_b2_int)
    professores_5_b2_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 group by professor_id',[perguntas_5_b2_1[0].id,perguntas_5_b2_1[-1].id,perguntas_5_b2_2[0].id,perguntas_5_b2_2[-1].id])
    qtd_professores_5_b2_int = len(professores_5_b2_int)

    respostas_5_b3_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 order by professor_id',[perguntas_5_b3_1[0].id,perguntas_5_b3_1[-1].id,perguntas_5_b3_2[0].id,perguntas_5_b3_2[-1].id])
    qtd_respostas_5_b3_cap = len(respostas_5_b3_cap)
    professores_5_b3_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 group by professor_id',[perguntas_5_b3_1[0].id,perguntas_5_b3_1[-1].id,perguntas_5_b3_2[0].id,perguntas_5_b3_2[-1].id])
    qtd_professores_5_b3_cap = len(professores_5_b3_cap)

    respostas_5_b3_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 order by professor_id',[perguntas_5_b3_1[0].id,perguntas_5_b3_1[-1].id,perguntas_5_b3_2[0].id,perguntas_5_b3_2[-1].id])
    qtd_respostas_5_b3_int = len(respostas_5_b3_int)
    professores_5_b3_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 group by professor_id',[perguntas_5_b3_1[0].id,perguntas_5_b3_1[-1].id,perguntas_5_b3_2[0].id,perguntas_5_b3_2[-1].id])
    qtd_professores_5_b3_int = len(professores_5_b3_int)

    respostas_5_b4_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 order by professor_id',[perguntas_5_b4_1[0].id,perguntas_5_b4_1[-1].id,perguntas_5_b4_2[0].id,perguntas_5_b4_2[-1].id])
    qtd_respostas_5_b4_cap = len(respostas_5_b4_cap)
    professores_5_b4_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 group by professor_id',[perguntas_5_b4_1[0].id,perguntas_5_b4_1[-1].id,perguntas_5_b4_2[0].id,perguntas_5_b4_2[-1].id])
    qtd_professores_5_b4_cap = len(professores_5_b4_cap)

    respostas_5_b4_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 order by professor_id',[perguntas_5_b4_1[0].id,perguntas_5_b4_1[-1].id,perguntas_5_b4_2[0].id,perguntas_5_b4_2[-1].id])
    qtd_respostas_5_b4_int = len(respostas_5_b4_int)
    professores_5_b4_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 group by professor_id',[perguntas_5_b4_1[0].id,perguntas_5_b4_1[-1].id,perguntas_5_b4_2[0].id,perguntas_5_b4_2[-1].id])
    qtd_professores_5_b4_int = len(professores_5_b4_int)


    respostas_9_b1_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 order by professor_id',[perguntas_9_b1_1[0].id,perguntas_9_b1_1[-1].id,perguntas_9_b1_2[0].id,perguntas_9_b1_2[-1].id])
    qtd_respostas_9_b1_cap = len(respostas_9_b1_cap)
    professores_9_b1_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 group by professor_id',[perguntas_9_b1_1[0].id,perguntas_9_b1_1[-1].id,perguntas_9_b1_2[0].id,perguntas_9_b1_2[-1].id])
    qtd_professores_9_b1_cap = len(professores_9_b1_cap)

    respostas_9_b1_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 order by professor_id',[perguntas_9_b1_1[0].id,perguntas_9_b1_1[-1].id,perguntas_9_b1_2[0].id,perguntas_9_b1_2[-1].id])
    qtd_respostas_9_b1_int = len(respostas_9_b1_int)
    professores_9_b1_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 group by professor_id',[perguntas_9_b1_1[0].id,perguntas_9_b1_1[-1].id,perguntas_9_b1_2[0].id,perguntas_9_b1_2[-1].id])
    qtd_professores_9_b1_int = len(professores_9_b1_int)

    respostas_9_b2_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 order by professor_id',[perguntas_9_b2_1[0].id,perguntas_9_b2_1[-1].id,perguntas_9_b2_2[0].id,perguntas_9_b2_2[-1].id])
    qtd_respostas_9_b2_cap = len(respostas_9_b2_cap)
    professores_9_b2_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 group by professor_id',[perguntas_9_b2_1[0].id,perguntas_9_b2_1[-1].id,perguntas_9_b2_2[0].id,perguntas_9_b2_2[-1].id])
    qtd_professores_9_b2_cap = len(professores_9_b2_cap)

    respostas_9_b2_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 order by professor_id',[perguntas_9_b2_1[0].id,perguntas_9_b2_1[-1].id,perguntas_9_b2_2[0].id,perguntas_9_b2_2[-1].id])
    qtd_respostas_9_b2_int = len(respostas_9_b2_int)
    professores_9_b2_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 group by professor_id',[perguntas_9_b2_1[0].id,perguntas_9_b2_1[-1].id,perguntas_9_b2_2[0].id,perguntas_9_b2_2[-1].id])
    qtd_professores_9_b2_int = len(professores_9_b2_int)

    respostas_9_b3_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 order by professor_id',[perguntas_9_b3_1[0].id,perguntas_9_b3_1[-1].id,perguntas_9_b3_2[0].id,perguntas_9_b3_2[-1].id])
    qtd_respostas_9_b3_cap = len(respostas_9_b3_cap)
    professores_9_b3_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 group by professor_id',[perguntas_9_b3_1[0].id,perguntas_9_b3_1[-1].id,perguntas_9_b3_2[0].id,perguntas_9_b3_2[-1].id])
    qtd_professores_9_b3_cap = len(professores_9_b3_cap)

    respostas_9_b3_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 order by professor_id',[perguntas_9_b3_1[0].id,perguntas_9_b3_1[-1].id,perguntas_9_b3_2[0].id,perguntas_9_b3_2[-1].id])
    qtd_respostas_9_b3_int = len(respostas_9_b3_int)
    professores_9_b3_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 group by professor_id',[perguntas_9_b3_1[0].id,perguntas_9_b3_1[-1].id,perguntas_9_b3_2[0].id,perguntas_9_b3_2[-1].id])
    qtd_professores_9_b3_int = len(professores_9_b3_int)

    respostas_9_b4_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 order by professor_id',[perguntas_9_b4_1[0].id,perguntas_9_b4_1[-1].id,perguntas_9_b4_2[0].id,perguntas_9_b4_2[-1].id])
    qtd_respostas_9_b4_cap = len(respostas_9_b4_cap)
    professores_9_b4_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 group by professor_id',[perguntas_9_b4_1[0].id,perguntas_9_b4_1[-1].id,perguntas_9_b4_2[0].id,perguntas_9_b4_2[-1].id])
    qtd_professores_9_b4_cap = len(professores_9_b4_cap)

    respostas_9_b4_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 order by professor_id',[perguntas_9_b4_1[0].id,perguntas_9_b4_1[-1].id,perguntas_9_b4_2[0].id,perguntas_9_b4_2[-1].id])
    qtd_respostas_9_b4_int = len(respostas_9_b4_int)
    professores_9_b4_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 group by professor_id',[perguntas_9_b4_1[0].id,perguntas_9_b4_1[-1].id,perguntas_9_b4_2[0].id,perguntas_9_b4_2[-1].id])
    qtd_professores_9_b4_int = len(professores_9_b4_int)

    respostas_3_b1_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 order by professor_id',[perguntas_3_b1_1[0].id,perguntas_3_b1_1[-1].id,perguntas_3_b1_2[0].id,perguntas_3_b1_2[-1].id])
    qtd_respostas_3_b1_cap = len(respostas_3_b1_cap)
    professores_3_b1_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 group by professor_id',[perguntas_3_b1_1[0].id,perguntas_3_b1_1[-1].id,perguntas_3_b1_2[0].id,perguntas_3_b1_2[-1].id])
    qtd_professores_3_b1_cap = len(professores_3_b1_cap)

    respostas_3_b1_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 order by professor_id',[perguntas_3_b1_1[0].id,perguntas_3_b1_1[-1].id,perguntas_3_b1_2[0].id,perguntas_3_b1_2[-1].id])
    qtd_respostas_3_b1_int = len(respostas_3_b1_int)
    professores_3_b1_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 group by professor_id',[perguntas_3_b1_1[0].id,perguntas_3_b1_1[-1].id,perguntas_3_b1_2[0].id,perguntas_3_b1_2[-1].id])
    qtd_professores_3_b1_int = len(professores_3_b1_int)

    respostas_3_b2_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 order by professor_id',[perguntas_3_b2_1[0].id,perguntas_3_b2_1[-1].id,perguntas_3_b2_2[0].id,perguntas_3_b2_2[-1].id])
    qtd_respostas_3_b2_cap = len(respostas_3_b2_cap)
    professores_3_b2_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 group by professor_id',[perguntas_3_b2_1[0].id,perguntas_3_b2_1[-1].id,perguntas_3_b2_2[0].id,perguntas_3_b2_2[-1].id])
    qtd_professores_3_b2_cap = len(professores_3_b2_cap)

    respostas_3_b2_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 order by professor_id',[perguntas_3_b2_1[0].id,perguntas_3_b2_1[-1].id,perguntas_3_b2_2[0].id,perguntas_3_b2_2[-1].id])
    qtd_respostas_3_b2_int = len(respostas_3_b2_int)
    professores_3_b2_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 group by professor_id',[perguntas_3_b2_1[0].id,perguntas_3_b2_1[-1].id,perguntas_3_b2_2[0].id,perguntas_3_b2_2[-1].id])
    qtd_professores_3_b2_int = len(professores_3_b2_int)

    respostas_3_b3_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 order by professor_id',[perguntas_3_b3_1[0].id,perguntas_3_b3_1[-1].id,perguntas_3_b3_2[0].id,perguntas_3_b3_2[-1].id])
    qtd_respostas_3_b3_cap = len(respostas_3_b3_cap)
    professores_3_b3_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 group by professor_id',[perguntas_3_b3_1[0].id,perguntas_3_b3_1[-1].id,perguntas_3_b3_2[0].id,perguntas_3_b3_2[-1].id])
    qtd_professores_3_b3_cap = len(professores_3_b3_cap)

    respostas_3_b3_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 order by professor_id',[perguntas_3_b3_1[0].id,perguntas_3_b3_1[-1].id,perguntas_3_b3_2[0].id,perguntas_3_b3_2[-1].id])
    qtd_respostas_3_b3_int = len(respostas_3_b3_int)
    professores_3_b3_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 group by professor_id',[perguntas_3_b3_1[0].id,perguntas_3_b3_1[-1].id,perguntas_3_b3_2[0].id,perguntas_3_b3_2[-1].id])
    qtd_professores_3_b3_int = len(professores_3_b3_int)

    respostas_3_b4_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 order by professor_id',[perguntas_3_b4_1[0].id,perguntas_3_b4_1[-1].id,perguntas_3_b4_2[0].id,perguntas_3_b4_2[-1].id])
    qtd_respostas_3_b4_cap = len(respostas_3_b4_cap)
    professores_3_b4_cap = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =1 group by professor_id',[perguntas_3_b4_1[0].id,perguntas_3_b4_1[-1].id,perguntas_3_b4_2[0].id,perguntas_3_b4_2[-1].id])
    qtd_professores_3_b4_cap = len(professores_3_b4_cap)

    respostas_3_b4_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 order by professor_id',[perguntas_3_b4_1[0].id,perguntas_3_b4_1[-1].id,perguntas_3_b4_2[0].id,perguntas_3_b4_2[-1].id])
    qtd_respostas_3_b4_int = len(respostas_3_b4_int)
    professores_3_b4_int = Resposta.objects.raw('SELECT * FROM app_resposta as r join app_professor as p on p.id = r.professor_id where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 or r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 and p.jurisdicao_id =2 group by professor_id',[perguntas_3_b4_1[0].id,perguntas_3_b4_1[-1].id,perguntas_3_b4_2[0].id,perguntas_3_b4_2[-1].id])
    qtd_professores_3_b4_int = len(professores_3_b4_int)





    #cumprimento do curricupo por disciplina
    respostas_2_b1_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b1_1[0].id,perguntas_2_b1_1[-1].id])
    qtd_respostas_2_b1_mt = len(respostas_2_b1_mt)
    respostas_2_b1_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b1_2[0].id,perguntas_2_b1_2[-1].id])
    qtd_respostas_2_b1_pt = len(respostas_2_b1_pt)
    professores_2_b1_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b1_1[0].id,perguntas_2_b1_1[-1].id])
    qtd_professores_2_b1_mt = len(professores_2_b1_mt)
    professores_2_b1_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b1_2[0].id,perguntas_2_b1_2[-1].id])
    qtd_professores_2_b1_pt = len(professores_2_b1_pt)
    qtd_perguntas_2_b1_mt =  len(perguntas_2_b1_1)
    qtd_perguntas_2_b1_pt =  len(perguntas_2_b1_2)

    respostas_2_b2_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b2_1[0].id,perguntas_2_b2_1[-1].id])
    qtd_respostas_2_b2_mt = len(respostas_2_b2_mt)
    respostas_2_b2_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b2_2[0].id,perguntas_2_b2_2[-1].id])
    qtd_respostas_2_b2_pt = len(respostas_2_b2_pt)
    professores_2_b2_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b2_1[0].id,perguntas_2_b2_1[-1].id])
    qtd_professores_2_b2_mt = len(professores_2_b2_mt)
    professores_2_b2_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b2_2[0].id,perguntas_2_b2_2[-1].id])
    qtd_professores_2_b2_pt = len(professores_2_b2_pt)
    qtd_perguntas_2_b2_mt =  len(perguntas_2_b2_1)
    qtd_perguntas_2_b2_pt =  len(perguntas_2_b2_2)

    respostas_2_b3_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b3_1[0].id,perguntas_2_b3_1[-1].id])
    qtd_respostas_2_b3_mt = len(respostas_2_b3_mt)
    respostas_2_b3_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b3_2[0].id,perguntas_2_b3_2[-1].id])
    qtd_respostas_2_b3_pt = len(respostas_2_b3_pt)
    professores_2_b3_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b3_1[0].id,perguntas_2_b3_1[-1].id])
    qtd_professores_2_b3_mt = len(professores_2_b3_mt)
    professores_2_b3_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b3_2[0].id,perguntas_2_b3_2[-1].id])
    qtd_professores_2_b3_pt = len(professores_2_b3_pt)
    qtd_perguntas_2_b3_mt =  len(perguntas_2_b3_1)
    qtd_perguntas_2_b3_pt =  len(perguntas_2_b3_2)

    respostas_2_b4_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b4_1[0].id,perguntas_2_b4_1[-1].id])
    qtd_respostas_2_b4_mt = len(respostas_2_b4_mt)
    respostas_2_b4_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_2_b4_2[0].id,perguntas_2_b4_2[-1].id])
    qtd_respostas_2_b4_pt = len(respostas_2_b4_pt)
    professores_2_b4_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b4_1[0].id,perguntas_2_b4_1[-1].id])
    qtd_professores_2_b4_mt = len(professores_2_b4_mt)
    professores_2_b4_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_2_b4_2[0].id,perguntas_2_b4_2[-1].id])
    qtd_professores_2_b4_pt = len(professores_2_b4_pt)
    qtd_perguntas_2_b4_mt =  len(perguntas_2_b4_1)
    qtd_perguntas_2_b4_pt =  len(perguntas_2_b4_2)



    respostas_5_b1_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b1_1[0].id,perguntas_5_b1_1[-1].id])
    qtd_respostas_5_b1_mt = len(respostas_5_b1_mt)
    respostas_5_b1_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b1_2[0].id,perguntas_5_b1_2[-1].id])
    qtd_respostas_5_b1_pt = len(respostas_5_b1_pt)
    professores_5_b1_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b1_1[0].id,perguntas_5_b1_1[-1].id])
    qtd_professores_5_b1_mt = len(professores_5_b1_mt)
    professores_5_b1_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b1_2[0].id,perguntas_5_b1_2[-1].id])
    qtd_professores_5_b1_pt = len(professores_5_b1_pt)
    qtd_perguntas_5_b1_mt =  len(perguntas_5_b1_1)
    qtd_perguntas_5_b1_pt =  len(perguntas_5_b1_2)

    respostas_5_b2_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b2_1[0].id,perguntas_5_b2_1[-1].id])
    qtd_respostas_5_b2_mt = len(respostas_5_b2_mt)
    respostas_5_b2_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b2_2[0].id,perguntas_5_b2_2[-1].id])
    qtd_respostas_5_b2_pt = len(respostas_5_b2_pt)
    professores_5_b2_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b2_1[0].id,perguntas_5_b2_1[-1].id])
    qtd_professores_5_b2_mt = len(professores_5_b2_mt)
    professores_5_b2_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b2_2[0].id,perguntas_5_b2_2[-1].id])
    qtd_professores_5_b2_pt = len(professores_5_b2_pt)
    qtd_perguntas_5_b2_mt =  len(perguntas_5_b2_1)
    qtd_perguntas_5_b2_pt =  len(perguntas_5_b2_2)

    respostas_5_b3_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b3_1[0].id,perguntas_5_b3_1[-1].id])
    qtd_respostas_5_b3_mt = len(respostas_5_b3_mt)
    respostas_5_b3_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b3_2[0].id,perguntas_5_b3_2[-1].id])
    qtd_respostas_5_b3_pt = len(respostas_5_b3_pt)
    professores_5_b3_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b3_1[0].id,perguntas_5_b3_1[-1].id])
    qtd_professores_5_b3_mt = len(professores_5_b3_mt)
    professores_5_b3_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b3_2[0].id,perguntas_5_b3_2[-1].id])
    qtd_professores_5_b3_pt = len(professores_5_b3_pt)
    qtd_perguntas_5_b3_mt =  len(perguntas_5_b3_1)
    qtd_perguntas_5_b3_pt =  len(perguntas_5_b3_2)

    respostas_5_b4_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b4_1[0].id,perguntas_5_b4_1[-1].id])
    qtd_respostas_5_b4_mt = len(respostas_5_b4_mt)
    respostas_5_b4_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_5_b4_2[0].id,perguntas_5_b4_2[-1].id])
    qtd_respostas_5_b4_pt = len(respostas_5_b4_pt)
    professores_5_b4_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b4_1[0].id,perguntas_5_b4_1[-1].id])
    qtd_professores_5_b4_mt = len(professores_5_b4_mt)
    professores_5_b4_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_5_b4_2[0].id,perguntas_5_b4_2[-1].id])
    qtd_professores_5_b4_pt = len(professores_5_b4_pt)
    qtd_perguntas_5_b4_mt =  len(perguntas_5_b4_1)
    qtd_perguntas_5_b4_pt =  len(perguntas_5_b4_2)

    respostas_9_b1_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b1_1[0].id,perguntas_9_b1_1[-1].id])
    qtd_respostas_9_b1_mt = len(respostas_9_b1_mt)
    respostas_9_b1_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b1_2[0].id,perguntas_9_b1_2[-1].id])
    qtd_respostas_9_b1_pt = len(respostas_9_b1_pt)
    professores_9_b1_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b1_1[0].id,perguntas_9_b1_1[-1].id])
    qtd_professores_9_b1_mt = len(professores_9_b1_mt)
    professores_9_b1_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b1_2[0].id,perguntas_9_b1_2[-1].id])
    qtd_professores_9_b1_pt = len(professores_9_b1_pt)
    qtd_perguntas_9_b1_mt =  len(perguntas_9_b1_1)
    qtd_perguntas_9_b1_pt =  len(perguntas_9_b1_2)

    respostas_9_b2_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b2_1[0].id,perguntas_9_b2_1[-1].id])
    qtd_respostas_9_b2_mt = len(respostas_9_b2_mt)
    respostas_9_b2_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b2_2[0].id,perguntas_9_b2_2[-1].id])
    qtd_respostas_9_b2_pt = len(respostas_9_b2_pt)
    professores_9_b2_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b2_1[0].id,perguntas_9_b2_1[-1].id])
    qtd_professores_9_b2_mt = len(professores_9_b2_mt)
    professores_9_b2_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b2_2[0].id,perguntas_9_b2_2[-1].id])
    qtd_professores_9_b2_pt = len(professores_9_b2_pt)
    qtd_perguntas_9_b2_mt =  len(perguntas_9_b2_1)
    qtd_perguntas_9_b2_pt =  len(perguntas_9_b2_2)

    respostas_9_b3_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b3_1[0].id,perguntas_9_b3_1[-1].id])
    qtd_respostas_9_b3_mt = len(respostas_9_b3_mt)
    respostas_9_b3_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b3_2[0].id,perguntas_9_b3_2[-1].id])
    qtd_respostas_9_b3_pt = len(respostas_9_b3_pt)
    professores_9_b3_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b3_1[0].id,perguntas_9_b3_1[-1].id])
    qtd_professores_9_b3_mt = len(professores_9_b3_mt)
    professores_9_b3_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b3_2[0].id,perguntas_9_b3_2[-1].id])
    qtd_professores_9_b3_pt = len(professores_9_b3_pt)
    qtd_perguntas_9_b3_mt =  len(perguntas_9_b3_1)
    qtd_perguntas_9_b3_pt =  len(perguntas_9_b3_2)

    respostas_9_b4_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b4_1[0].id,perguntas_9_b4_1[-1].id])
    qtd_respostas_9_b4_mt = len(respostas_9_b4_mt)
    respostas_9_b4_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_9_b4_2[0].id,perguntas_9_b4_2[-1].id])
    qtd_respostas_9_b4_pt = len(respostas_9_b4_pt)
    professores_9_b4_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b4_1[0].id,perguntas_9_b4_1[-1].id])
    qtd_professores_9_b4_mt = len(professores_9_b4_mt)
    professores_9_b4_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_9_b4_2[0].id,perguntas_9_b4_2[-1].id])
    qtd_professores_9_b4_pt = len(professores_9_b4_pt)
    qtd_perguntas_9_b4_mt =  len(perguntas_9_b4_1)
    qtd_perguntas_9_b4_pt =  len(perguntas_9_b4_2)

    respostas_3_b1_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b1_1[0].id,perguntas_3_b1_1[-1].id])
    qtd_respostas_3_b1_mt = len(respostas_3_b1_mt)
    respostas_3_b1_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b1_2[0].id,perguntas_3_b1_2[-1].id])
    qtd_respostas_3_b1_pt = len(respostas_3_b1_pt)
    professores_3_b1_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b1_1[0].id,perguntas_3_b1_1[-1].id])
    qtd_professores_3_b1_mt = len(professores_3_b1_mt)
    professores_3_b1_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b1_2[0].id,perguntas_3_b1_2[-1].id])
    qtd_professores_3_b1_pt = len(professores_3_b1_pt)
    qtd_perguntas_3_b1_mt =  len(perguntas_3_b1_1)
    qtd_perguntas_3_b1_pt =  len(perguntas_3_b1_2)

    respostas_3_b2_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b2_1[0].id,perguntas_3_b2_1[-1].id])
    qtd_respostas_3_b2_mt = len(respostas_3_b2_mt)
    respostas_3_b2_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b2_2[0].id,perguntas_3_b2_2[-1].id])
    qtd_respostas_3_b2_pt = len(respostas_3_b2_pt)
    professores_3_b2_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b2_1[0].id,perguntas_3_b2_1[-1].id])
    qtd_professores_3_b2_mt = len(professores_3_b2_mt)
    professores_3_b2_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b2_2[0].id,perguntas_3_b2_2[-1].id])
    qtd_professores_3_b2_pt = len(professores_3_b2_pt)
    qtd_perguntas_3_b2_mt =  len(perguntas_3_b2_1)
    qtd_perguntas_3_b2_pt =  len(perguntas_3_b2_2)

    respostas_3_b3_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b3_1[0].id,perguntas_3_b3_1[-1].id])
    qtd_respostas_3_b3_mt = len(respostas_3_b3_mt)
    respostas_3_b3_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b3_2[0].id,perguntas_3_b3_2[-1].id])
    qtd_respostas_3_b3_pt = len(respostas_3_b3_pt)
    professores_3_b3_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b3_1[0].id,perguntas_3_b3_1[-1].id])
    qtd_professores_3_b3_mt = len(professores_3_b3_mt)
    professores_3_b3_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b3_2[0].id,perguntas_3_b3_2[-1].id])
    qtd_professores_3_b3_pt = len(professores_3_b3_pt)
    qtd_perguntas_3_b3_mt =  len(perguntas_3_b3_1)
    qtd_perguntas_3_b3_pt =  len(perguntas_3_b3_2)

    respostas_3_b4_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b4_1[0].id,perguntas_3_b4_1[-1].id])
    qtd_respostas_3_b4_mt = len(respostas_3_b4_mt)
    respostas_3_b4_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 order by professor_id',[perguntas_3_b4_2[0].id,perguntas_3_b4_2[-1].id])
    qtd_respostas_3_b4_pt = len(respostas_3_b4_pt)
    professores_3_b4_mt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b4_1[0].id,perguntas_3_b4_1[-1].id])
    qtd_professores_3_b4_mt = len(professores_3_b4_mt)
    professores_3_b4_pt = Resposta.objects.raw('SELECT * FROM app_resposta as r  where r.pergunta_id >= %s and r.pergunta_id <= %s and r.resposta = 1 and foi_possivel = 1 group by professor_id',[perguntas_3_b4_2[0].id,perguntas_3_b4_2[-1].id])
    qtd_professores_3_b4_pt = len(professores_3_b4_pt)
    qtd_perguntas_3_b4_mt =  len(perguntas_3_b4_1)
    qtd_perguntas_3_b4_pt =  len(perguntas_3_b4_2)


    #calculo turno mat serie 2

    total_perguntas_2_mat = (qtd_perguntas_2_b1* qtd_professores_2_b1_mat) + (qtd_perguntas_2_b2* qtd_professores_2_b2_mat) + (qtd_perguntas_2_b3* qtd_professores_2_b3_mat) + (qtd_perguntas_2_b4* qtd_professores_2_b4_mat)
    total_respostas_2_mat = qtd_respostas_2_b1_mat + qtd_respostas_2_b2_mat + qtd_respostas_2_b3_mat + qtd_respostas_2_b4_mat

    if total_perguntas_2_mat == 0:
        por_2_mat = 0
    else:
        por_2_mat = (total_respostas_2_mat * 100) / total_perguntas_2_mat

    #calculo turno mat serie 5

    total_perguntas_5_mat = (qtd_perguntas_5_b1* qtd_professores_5_b1_mat) + (qtd_perguntas_5_b2* qtd_professores_5_b2_mat) + (qtd_perguntas_5_b3* qtd_professores_5_b3_mat) + (qtd_perguntas_5_b4* qtd_professores_5_b4_mat)
    total_respostas_5_mat = qtd_respostas_5_b1_mat + qtd_respostas_5_b2_mat + qtd_respostas_5_b3_mat + qtd_respostas_5_b4_mat

    if total_perguntas_5_mat == 0:
        por_5_mat = 0
    else:
        por_5_mat = (total_respostas_5_mat * 100) / total_perguntas_5_mat

    #calculo turno mat serie 9

    total_perguntas_9_mat = (qtd_perguntas_9_b1* qtd_professores_9_b1_mat) + (qtd_perguntas_9_b2* qtd_professores_9_b2_mat) + (qtd_perguntas_9_b3* qtd_professores_9_b3_mat) + (qtd_perguntas_9_b4* qtd_professores_9_b4_mat)
    total_respostas_9_mat = qtd_respostas_9_b1_mat + qtd_respostas_9_b2_mat + qtd_respostas_9_b3_mat + qtd_respostas_9_b4_mat

    if total_perguntas_9_mat == 0:
        por_9_mat = 0
    else:
        por_9_mat = (total_respostas_9_mat * 100) / total_perguntas_9_mat

    #calculo turno mat serie 3

    total_perguntas_3_mat = (qtd_perguntas_3_b1* qtd_professores_3_b1_mat) + (qtd_perguntas_3_b2* qtd_professores_3_b2_mat) + (qtd_perguntas_3_b3* qtd_professores_3_b3_mat) + (qtd_perguntas_3_b4* qtd_professores_3_b4_mat)
    total_respostas_3_mat = qtd_respostas_3_b1_mat + qtd_respostas_3_b2_mat + qtd_respostas_3_b3_mat + qtd_respostas_3_b4_mat

    if total_perguntas_3_mat == 0:
        por_3_mat = 0
    else:
        por_3_mat = (total_respostas_3_mat * 100) / total_perguntas_3_mat

    #calculo turno vesp serie 2

    total_perguntas_2_vesp = (qtd_perguntas_2_b1* qtd_professores_2_b1_vesp) + (qtd_perguntas_2_b2* qtd_professores_2_b2_vesp) + (qtd_perguntas_2_b3* qtd_professores_2_b3_vesp) + (qtd_perguntas_2_b4* qtd_professores_2_b4_vesp)
    total_respostas_2_vesp = qtd_respostas_2_b1_vesp + qtd_respostas_2_b2_vesp + qtd_respostas_2_b3_vesp + qtd_respostas_2_b4_vesp


    if total_perguntas_2_vesp == 0:
        por_2_vesp = 0
    else:
        por_2_vesp = (total_respostas_2_vesp * 100) / total_perguntas_2_vesp

    #calculo turno vesp serie 5

    total_perguntas_5_vesp = (qtd_perguntas_5_b1* qtd_professores_5_b1_vesp) + (qtd_perguntas_5_b2* qtd_professores_5_b2_vesp) + (qtd_perguntas_5_b3* qtd_professores_5_b3_vesp) + (qtd_perguntas_5_b4* qtd_professores_5_b4_vesp)
    total_respostas_5_vesp = qtd_respostas_5_b1_vesp + qtd_respostas_5_b2_vesp + qtd_respostas_5_b3_vesp + qtd_respostas_5_b4_vesp

    if total_perguntas_5_vesp == 0:
        por_5_vesp = 0
    else:
        por_5_vesp = (total_respostas_5_vesp * 100) / total_perguntas_5_vesp

    #calculo turno vesp serie 9

    total_perguntas_9_vesp = (qtd_perguntas_9_b1* qtd_professores_9_b1_vesp) + (qtd_perguntas_9_b2* qtd_professores_9_b2_vesp) + (qtd_perguntas_9_b3* qtd_professores_9_b3_vesp) + (qtd_perguntas_9_b4* qtd_professores_9_b4_vesp)
    total_respostas_9_vesp = qtd_respostas_9_b1_vesp + qtd_respostas_9_b2_vesp + qtd_respostas_9_b3_vesp + qtd_respostas_9_b4_vesp

    if total_perguntas_9_vesp == 0:
        por_9_vesp = 0
    else:
        por_9_vesp = (total_respostas_9_vesp * 100) / total_perguntas_9_vesp

    #calculo turno vesp serie 3

    total_perguntas_3_vesp = (qtd_perguntas_3_b1* qtd_professores_3_b1_vesp) + (qtd_perguntas_3_b2* qtd_professores_3_b2_vesp) + (qtd_perguntas_3_b3* qtd_professores_3_b3_vesp) + (qtd_perguntas_3_b4* qtd_professores_3_b4_vesp)
    total_respostas_3_vesp = qtd_respostas_3_b1_vesp + qtd_respostas_3_b2_vesp + qtd_respostas_3_b3_vesp + qtd_respostas_3_b4_vesp

    if total_perguntas_3_vesp == 0:
        por_3_vesp = 0
    else:
        por_3_vesp = (total_respostas_3_vesp * 100) / total_perguntas_3_vesp

    #calculo turno not serie 2

    total_perguntas_2_not = (qtd_perguntas_2_b1* qtd_professores_2_b1_not) + (qtd_perguntas_2_b2* qtd_professores_2_b2_not) + (qtd_perguntas_2_b3* qtd_professores_2_b3_not) + (qtd_perguntas_2_b4* qtd_professores_2_b4_not)
    total_respostas_2_not = qtd_respostas_2_b1_not + qtd_respostas_2_b2_not + qtd_respostas_2_b3_not + qtd_respostas_2_b4_not

    if total_perguntas_2_not == 0 :
        por_2_not = 0
    else:
        por_2_not = (total_respostas_2_not * 100) / total_perguntas_2_not
    #calculo turno not serie 5

    total_perguntas_5_not = (qtd_perguntas_5_b1* qtd_professores_5_b1_not) + (qtd_perguntas_5_b2* qtd_professores_5_b2_not) + (qtd_perguntas_5_b3* qtd_professores_5_b3_not) + (qtd_perguntas_5_b4* qtd_professores_5_b4_not)
    total_respostas_5_not = qtd_respostas_5_b1_not + qtd_respostas_5_b2_not + qtd_respostas_5_b3_not + qtd_respostas_5_b4_not
    if total_perguntas_5_not == 0 :
        por_5_not = 0
    else:
        por_5_not = (total_respostas_5_not * 100) / total_perguntas_5_not



    #calculo turno not serie 9

    total_perguntas_9_not = (qtd_perguntas_9_b1* qtd_professores_9_b1_not) + (qtd_perguntas_9_b2* qtd_professores_9_b2_not) + (qtd_perguntas_9_b3* qtd_professores_9_b3_not) + (qtd_perguntas_9_b4* qtd_professores_9_b4_not)
    total_respostas_9_not = qtd_respostas_9_b1_not + qtd_respostas_9_b2_not + qtd_respostas_9_b3_not + qtd_respostas_9_b4_not
    if total_perguntas_9_not == 0 :
        por_9_not = 0
    else:
        por_9_not = (total_respostas_9_not * 100) / total_perguntas_9_not


    #calculo turno not serie 3

    total_perguntas_3_not = (qtd_perguntas_3_b1* qtd_professores_3_b1_not) + (qtd_perguntas_3_b2* qtd_professores_3_b2_not) + (qtd_perguntas_3_b3* qtd_professores_3_b3_not) + (qtd_perguntas_3_b4* qtd_professores_3_b4_not)
    total_respostas_3_not = qtd_respostas_3_b1_not + qtd_respostas_3_b2_not + qtd_respostas_3_b3_not + qtd_respostas_3_b4_not
    if total_perguntas_3_not == 0 :
        por_3_not = 0
    else:
        por_3_not = (total_respostas_3_not * 100) / total_perguntas_3_not
    #calculo turno integ serie 2

    total_perguntas_2_integ = (qtd_perguntas_2_b1* qtd_professores_2_b1_integ) + (qtd_perguntas_2_b2* qtd_professores_2_b2_integ) + (qtd_perguntas_2_b3* qtd_professores_2_b3_integ) + (qtd_perguntas_2_b4* qtd_professores_2_b4_integ)
    total_respostas_2_integ = qtd_respostas_2_b1_integ + qtd_respostas_2_b2_integ + qtd_respostas_2_b3_integ + qtd_respostas_2_b4_integ
    if total_perguntas_2_integ == 0 :
        por_2_integ = 0
    else:
        por_2_integ = (total_respostas_2_integ * 100) / total_perguntas_2_integ



    #calculo turno integ serie 5

    total_perguntas_5_integ = (qtd_perguntas_5_b1* qtd_professores_5_b1_integ) + (qtd_perguntas_5_b2* qtd_professores_5_b2_integ) + (qtd_perguntas_5_b3* qtd_professores_5_b3_integ) + (qtd_perguntas_5_b4* qtd_professores_5_b4_integ)
    total_respostas_5_integ = qtd_respostas_5_b1_integ + qtd_respostas_5_b2_integ + qtd_respostas_5_b3_integ + qtd_respostas_5_b4_integ
    if total_perguntas_5_integ == 0 :
        por_5_integ = 0
    else:
        por_5_integ = (total_respostas_5_integ * 100) / total_perguntas_5_integ



    #calculo turno integ serie 9

    total_perguntas_9_integ = (qtd_perguntas_9_b1* qtd_professores_9_b1_integ) + (qtd_perguntas_9_b2* qtd_professores_9_b2_integ) + (qtd_perguntas_9_b3* qtd_professores_9_b3_integ) + (qtd_perguntas_9_b4* qtd_professores_9_b4_integ)
    total_respostas_9_integ = qtd_respostas_9_b1_integ + qtd_respostas_9_b2_integ + qtd_respostas_9_b3_integ + qtd_respostas_9_b4_integ
    if total_perguntas_9_integ == 0 :
        por_9_integ = 0
    else:
        por_9_integ = (total_respostas_9_integ * 100) / total_perguntas_9_integ


    #calculo turno integ serie 3

    total_perguntas_3_integ = (qtd_perguntas_3_b1* qtd_professores_3_b1_integ) + (qtd_perguntas_3_b2* qtd_professores_3_b2_integ) + (qtd_perguntas_3_b3* qtd_professores_3_b3_integ) + (qtd_perguntas_3_b4* qtd_professores_3_b4_integ)
    total_respostas_3_integ = qtd_respostas_3_b1_integ + qtd_respostas_3_b2_integ + qtd_respostas_3_b3_integ + qtd_respostas_3_b4_integ
    if total_perguntas_3_integ == 0 :
        por_3_integ = 0
    else:
        por_3_integ = (total_respostas_3_integ * 100) / total_perguntas_3_integ

    #calculo turno mat geral

    total_perguntas_mat = total_perguntas_2_mat + total_perguntas_5_mat + total_perguntas_9_mat + total_perguntas_3_mat
    total_respostas_mat = total_respostas_2_mat + total_respostas_5_mat + total_respostas_9_mat + total_respostas_3_mat
    if total_perguntas_mat == 0:
        por_mat = 0
    else:
        por_mat = (total_respostas_mat * 100) / total_perguntas_mat
    #calculo turno vesp geral

    total_perguntas_vesp = total_perguntas_2_vesp + total_perguntas_5_vesp + total_perguntas_9_vesp + total_perguntas_3_vesp
    total_respostas_vesp = total_respostas_2_vesp + total_respostas_5_vesp + total_respostas_9_vesp + total_respostas_3_vesp
    if total_perguntas_vesp == 0:
        por_vesp = 0
    else:
        por_vesp = (total_respostas_vesp * 100) / total_perguntas_vesp



    #calculo turno not geral

    total_perguntas_not = total_perguntas_2_not + total_perguntas_5_not + total_perguntas_9_not + total_perguntas_3_not
    total_respostas_not = total_respostas_2_not + total_respostas_5_not + total_respostas_9_not + total_respostas_3_not
    if total_perguntas_not == 0:
        por_not = 0
    else:
        por_not = (total_respostas_not * 100) / total_perguntas_not

    #calculo turno integ geral

    total_perguntas_integ = total_perguntas_2_integ + total_perguntas_5_integ + total_perguntas_9_integ + total_perguntas_3_integ
    total_respostas_integ = total_respostas_2_integ + total_respostas_5_integ + total_respostas_9_integ + total_respostas_3_integ
    if total_perguntas_integ == 0:
        por_integ = 0
    else:
        por_integ = (total_respostas_integ * 100) / total_perguntas_integ


    #calculo b1
    total_perguntas_b1 = (qtd_perguntas_2_b1 * qtd_professores_2_b1) + (qtd_perguntas_5_b1 * qtd_professores_5_b1) + (qtd_perguntas_9_b1 * qtd_professores_9_b1) + (qtd_perguntas_3_b1 * qtd_professores_3_b1)
    total_respostas_b1 = qtd_respostas_2_b1 + qtd_respostas_5_b1 + qtd_respostas_9_b1 + qtd_respostas_3_b1

    if total_perguntas_b1 == 0:
        por_b1 = 0
    else:
        por_b1 = (total_respostas_b1 * 100) / total_perguntas_b1

    #calculo b2
    total_perguntas_b2 = (qtd_perguntas_2_b2 * qtd_professores_2_b2) + (qtd_perguntas_5_b2 * qtd_professores_5_b2) + (qtd_perguntas_9_b2 * qtd_professores_9_b2) + (qtd_perguntas_3_b2 * qtd_professores_3_b2)
    total_respostas_b2 = qtd_respostas_2_b2 + qtd_respostas_5_b2 + qtd_respostas_9_b2 + qtd_respostas_3_b2
    if total_perguntas_b2 == 0:
        por_b2 = 0
    else:
        por_b2 = (total_respostas_b2 * 100) / total_perguntas_b2



    #calculo b3
    total_perguntas_b3 = (qtd_perguntas_2_b3 * qtd_professores_2_b3) + (qtd_perguntas_5_b3 * qtd_professores_5_b3) + (qtd_perguntas_9_b3 * qtd_professores_9_b3) + (qtd_perguntas_3_b3 * qtd_professores_3_b3)
    total_respostas_b3 = qtd_respostas_2_b3 + qtd_respostas_5_b3 + qtd_respostas_9_b3 + qtd_respostas_3_b3
    if total_perguntas_b3 == 0:
        por_b3 = 0
    else:
        por_b3 = (total_respostas_b3 * 100) / total_perguntas_b3



    #calculo b4
    total_perguntas_b4 = (qtd_perguntas_2_b4 * qtd_professores_2_b4) + (qtd_perguntas_5_b4 * qtd_professores_5_b4) + (qtd_perguntas_9_b4 * qtd_professores_9_b4) + (qtd_perguntas_3_b4 * qtd_professores_3_b4)
    total_respostas_b4 = qtd_respostas_2_b4 + qtd_respostas_5_b4 + qtd_respostas_9_b4 + qtd_respostas_3_b4
    if total_perguntas_b4 == 0:
        por_b4 = 0
    else:
        por_b4 = (total_respostas_b4 * 100) / total_perguntas_b4

    #calculo geral
    total_perguntas_geral = total_perguntas_b1 + total_perguntas_b2 + total_perguntas_b3 + total_perguntas_b4
    total_respostas_geral = total_respostas_b1 + total_respostas_b2 + total_respostas_b3 + total_respostas_b4

    if total_perguntas_geral == 0:
        por_geral = 0
    else:
        por_geral = (total_respostas_geral * 100) / total_perguntas_geral

    #calculo das series
    total_perguntas_2 = (qtd_perguntas_2_b1 * qtd_professores_2_b1) + (qtd_perguntas_2_b2 * qtd_professores_2_b2) + (qtd_perguntas_2_b3 * qtd_professores_2_b3) + (qtd_perguntas_2_b4 * qtd_professores_2_b4)
    total_respostas_2 = qtd_respostas_2_b1 + qtd_respostas_2_b2 + qtd_respostas_2_b3 + qtd_respostas_2_b4

    if total_perguntas_2 == 0:
        por_2 = 0
    else:
        por_2 = (total_respostas_2 * 100) / total_perguntas_2

    total_perguntas_5 = (qtd_perguntas_5_b1 * qtd_professores_5_b1) + (qtd_perguntas_5_b2 * qtd_professores_5_b2) + (qtd_perguntas_5_b3 * qtd_professores_5_b3) + (qtd_perguntas_5_b4 * qtd_professores_5_b4)
    total_respostas_5 = qtd_respostas_5_b1 + qtd_respostas_5_b2 + qtd_respostas_5_b3 + qtd_respostas_5_b4
    if total_perguntas_5 == 0:
        por_5 = 0
    else:
        por_5 = (total_respostas_5 * 100) / total_perguntas_5



    total_perguntas_9 = (qtd_perguntas_9_b1 * qtd_professores_9_b1) + (qtd_perguntas_9_b2 * qtd_professores_9_b2) + (qtd_perguntas_9_b3 * qtd_professores_9_b3) + (qtd_perguntas_9_b4 * qtd_professores_9_b4)
    total_respostas_9 = qtd_respostas_9_b1 + qtd_respostas_9_b2 + qtd_respostas_9_b3 + qtd_respostas_9_b4
    if total_perguntas_9 == 0:
        por_9 = 0
    else:
        por_9 = (total_respostas_9 * 100) / total_perguntas_9


    total_perguntas_3 = (qtd_perguntas_3_b1 * qtd_professores_3_b1) + (qtd_perguntas_3_b2 * qtd_professores_3_b2) + (qtd_perguntas_3_b3 * qtd_professores_3_b3) + (qtd_perguntas_3_b4 * qtd_professores_3_b4)
    total_respostas_3 = qtd_respostas_3_b1 + qtd_respostas_3_b2 + qtd_respostas_3_b3 + qtd_respostas_3_b4
    if total_perguntas_3 == 0:
        por_3 = 0
    else:
        por_3 = (total_respostas_3 * 100) / total_perguntas_3

    #Calculo por serie/bimestre

    total_perguntas_2_b1 = qtd_perguntas_2_b1 * qtd_professores_2_b1
    if total_perguntas_2_b1 == 0:
        por_2_b1 = 0
    else:
        por_2_b1 = (qtd_respostas_2_b1 * 100) / total_perguntas_2_b1

    total_perguntas_2_b2 = qtd_perguntas_2_b2 * qtd_professores_2_b2
    if total_perguntas_2_b2 == 0:
        por_2_b2 = 0
    else:
        por_2_b2 = (qtd_respostas_2_b2 * 100) / total_perguntas_2_b2



    total_perguntas_2_b3 = qtd_perguntas_2_b3 * qtd_professores_2_b3
    if total_perguntas_2_b3 == 0:
        por_2_b3 = 0
    else:
        por_2_b3 = (qtd_respostas_2_b3 * 100) / total_perguntas_2_b3



    total_perguntas_2_b4 = qtd_perguntas_2_b4 * qtd_professores_2_b4
    if total_perguntas_2_b4 == 0:
        por_2_b4 = 0
    else:
        por_2_b4 = (qtd_respostas_2_b4 * 100) / total_perguntas_2_b4


    total_perguntas_5_b1 = qtd_perguntas_5_b1 * qtd_professores_5_b1
    if total_perguntas_5_b1 == 0:
        por_5_b1 = 0
    else:
        por_5_b1 = (qtd_respostas_5_b1 * 100) / total_perguntas_5_b1


    total_perguntas_5_b2 = qtd_perguntas_5_b2 * qtd_professores_5_b2
    if total_perguntas_5_b2 == 0:
        por_5_b2 = 0
    else:
        por_5_b2 = (qtd_respostas_5_b2 * 100) / total_perguntas_5_b2


    total_perguntas_5_b3 = qtd_perguntas_5_b3 * qtd_professores_5_b3
    if total_perguntas_5_b3 == 0:
        por_5_b3 = 0
    else:
        por_5_b3 = (qtd_respostas_5_b3 * 100) / total_perguntas_5_b3



    total_perguntas_5_b4 = qtd_perguntas_5_b4 * qtd_professores_5_b4
    if total_perguntas_5_b4 == 0:
        por_5_b4 = 0
    else:
        por_5_b4 = (qtd_respostas_5_b4 * 100) / total_perguntas_5_b4


    total_perguntas_9_b1 = qtd_perguntas_9_b1 * qtd_professores_9_b1
    if total_perguntas_9_b1 == 0:
        por_9_b1 = 0
    else:
        por_9_b1 = (qtd_respostas_9_b1 * 100) / total_perguntas_9_b1



    total_perguntas_9_b2 = qtd_perguntas_9_b2 * qtd_professores_9_b2
    if total_perguntas_9_b2 == 0:
        por_9_b2 = 0
    else:
        por_9_b2 = (qtd_respostas_9_b2 * 100) / total_perguntas_9_b2



    total_perguntas_9_b3 = qtd_perguntas_9_b3 * qtd_professores_9_b3
    if total_perguntas_9_b3 == 0:
        por_9_b3 = 0
    else:
        por_9_b3 = (qtd_respostas_9_b3 * 100) / total_perguntas_9_b3


    total_perguntas_9_b4 = qtd_perguntas_9_b4 * qtd_professores_9_b4
    if total_perguntas_9_b4 == 0:
        por_9_b4 = 0
    else:
        por_9_b4 = (qtd_respostas_9_b4 * 100) / total_perguntas_9_b4



    total_perguntas_3_b1 = qtd_perguntas_3_b1 * qtd_professores_3_b1
    if total_perguntas_3_b1 == 0:
        por_3_b1 = 0
    else:
        por_3_b1 = (qtd_respostas_3_b1 * 100) / total_perguntas_3_b1



    total_perguntas_3_b2 = qtd_perguntas_3_b2 * qtd_professores_3_b2
    if total_perguntas_3_b2 == 0:
        por_3_b2 = 0
    else:
        por_3_b2 = (qtd_respostas_3_b2 * 100) / total_perguntas_3_b2



    total_perguntas_3_b3 = qtd_perguntas_3_b3 * qtd_professores_3_b3
    if total_perguntas_3_b3 == 0:
        por_3_b3 = 0
    else:
        por_3_b3 = (qtd_respostas_3_b3 * 100) / total_perguntas_3_b3



    total_perguntas_3_b4 = qtd_perguntas_3_b4 * qtd_professores_3_b4
    if total_perguntas_3_b4 == 0:
        por_3_b4 = 0
    else:
        por_3_b4 = (qtd_respostas_3_b4 * 100) / total_perguntas_3_b4


    #Calculo por jurisdicao
    total_perguntas_2_cap = (qtd_perguntas_2_b1*qtd_professores_2_b1_cap)+(qtd_perguntas_2_b2*qtd_professores_2_b2_cap)+(qtd_perguntas_2_b3*qtd_professores_2_b3_cap)+(qtd_perguntas_2_b4*qtd_professores_2_b4_cap)
    total_perguntas_5_cap = (qtd_perguntas_5_b1*qtd_professores_5_b1_cap)+(qtd_perguntas_5_b2*qtd_professores_5_b2_cap)+(qtd_perguntas_5_b3*qtd_professores_5_b3_cap)+(qtd_perguntas_5_b4*qtd_professores_5_b4_cap)
    total_perguntas_9_cap = (qtd_perguntas_9_b1*qtd_professores_9_b1_cap)+(qtd_perguntas_9_b2*qtd_professores_9_b2_cap)+(qtd_perguntas_9_b3*qtd_professores_9_b3_cap)+(qtd_perguntas_9_b4*qtd_professores_9_b4_cap)
    total_perguntas_3_cap = (qtd_perguntas_3_b1*qtd_professores_3_b1_cap)+(qtd_perguntas_3_b2*qtd_professores_3_b2_cap)+(qtd_perguntas_3_b3*qtd_professores_3_b3_cap)+(qtd_perguntas_3_b4*qtd_professores_3_b4_cap)
    total_perguntas_cap = total_perguntas_2_cap + total_perguntas_5_cap + total_perguntas_9_cap + total_perguntas_3_cap
    total_respostas_2_cap = qtd_respostas_2_b1_cap + qtd_respostas_2_b2_cap + qtd_respostas_2_b3_cap + qtd_respostas_2_b4_cap
    total_respostas_5_cap = qtd_respostas_5_b1_cap + qtd_respostas_5_b2_cap + qtd_respostas_5_b3_cap + qtd_respostas_5_b4_cap
    total_respostas_9_cap = qtd_respostas_9_b1_cap + qtd_respostas_9_b2_cap + qtd_respostas_9_b3_cap + qtd_respostas_9_b4_cap
    total_respostas_3_cap = qtd_respostas_3_b1_cap + qtd_respostas_3_b2_cap + qtd_respostas_3_b3_cap + qtd_respostas_3_b4_cap
    total_respostas_cap = total_respostas_2_cap + total_respostas_5_cap + total_respostas_9_cap + total_respostas_3_cap

    if total_perguntas_cap == 0 :
        por_cap = 0
    else:
        por_cap = (total_respostas_cap * 100) / total_perguntas_cap


    total_perguntas_2_int = (qtd_perguntas_2_b1*qtd_professores_2_b1_int)+(qtd_perguntas_2_b2*qtd_professores_2_b2_int)+(qtd_perguntas_2_b3*qtd_professores_2_b3_int)+(qtd_perguntas_2_b4*qtd_professores_2_b4_int)
    total_perguntas_5_int = (qtd_perguntas_5_b1*qtd_professores_5_b1_int)+(qtd_perguntas_5_b2*qtd_professores_5_b2_int)+(qtd_perguntas_5_b3*qtd_professores_5_b3_int)+(qtd_perguntas_5_b4*qtd_professores_5_b4_int)
    total_perguntas_9_int = (qtd_perguntas_9_b1*qtd_professores_9_b1_int)+(qtd_perguntas_9_b2*qtd_professores_9_b2_int)+(qtd_perguntas_9_b3*qtd_professores_9_b3_int)+(qtd_perguntas_9_b4*qtd_professores_9_b4_int)
    total_perguntas_3_int = (qtd_perguntas_3_b1*qtd_professores_3_b1_int)+(qtd_perguntas_3_b2*qtd_professores_3_b2_int)+(qtd_perguntas_3_b3*qtd_professores_3_b3_int)+(qtd_perguntas_3_b4*qtd_professores_3_b4_int)
    total_perguntas_int = total_perguntas_2_int + total_perguntas_5_int + total_perguntas_9_int + total_perguntas_3_int
    total_respostas_2_int = qtd_respostas_2_b1_int + qtd_respostas_2_b2_int + qtd_respostas_2_b3_int + qtd_respostas_2_b4_int
    total_respostas_5_int = qtd_respostas_5_b1_int + qtd_respostas_5_b2_int + qtd_respostas_5_b3_int + qtd_respostas_5_b4_int
    total_respostas_9_int = qtd_respostas_9_b1_int + qtd_respostas_9_b2_int + qtd_respostas_9_b3_int + qtd_respostas_9_b4_int
    total_respostas_3_int = qtd_respostas_3_b1_int + qtd_respostas_3_b2_int + qtd_respostas_3_b3_int + qtd_respostas_3_b4_int
    total_respostas_int = total_respostas_2_int + total_respostas_5_int + total_respostas_9_int + total_respostas_3_int
    if total_perguntas_int == 0:
        por_int = 0
    else:
        por_int = (total_respostas_int * 100) / total_perguntas_int

    if (total_respostas_cap + total_respostas_int) == 0:
        por_juris_cap = 0
    else:
        por_juris_cap = (total_respostas_cap * 100) / (total_respostas_cap + total_respostas_int)

    #cumprimento do curriculo por nivel de ensino
    total_perguntas_em = total_perguntas_3_b1 + total_perguntas_3_b2 + total_perguntas_3_b3 + total_perguntas_3_b4
    total_perguntas_ef = total_perguntas_2_b1 + total_perguntas_2_b2 + total_perguntas_2_b3 + total_perguntas_2_b4 + total_perguntas_5_b1 + total_perguntas_5_b2 + total_perguntas_5_b3 + total_perguntas_5_b4 + total_perguntas_9_b1 + total_perguntas_9_b2 + total_perguntas_9_b3 + total_perguntas_9_b4
    total_respostas_em = qtd_respostas_3_b1 + qtd_respostas_3_b2 + qtd_respostas_3_b3 + qtd_respostas_3_b4
    total_respostas_ef = qtd_respostas_2_b1 + qtd_respostas_2_b2 + qtd_respostas_2_b3 + qtd_respostas_2_b4 + qtd_respostas_5_b1 + qtd_respostas_5_b2 + qtd_respostas_5_b3 + qtd_respostas_5_b4 + qtd_respostas_9_b1 + qtd_respostas_9_b2 + qtd_respostas_9_b3 + qtd_respostas_9_b4

    if total_perguntas_em == 0:
        por_cumprimento_em = 0
    else:
        por_cumprimento_em = (total_respostas_em * 100) / total_perguntas_em
    if total_perguntas_ef == 0:
        por_cumprimento_ef = 0
    else:
        por_cumprimento_ef = (total_respostas_ef * 100) / total_perguntas_ef




    total_perguntas_2_mt = (qtd_perguntas_2_b1_mt * qtd_professores_2_b1_mt) + (qtd_perguntas_2_b2_mt * qtd_professores_2_b2_mt) + (qtd_perguntas_2_b3_mt * qtd_professores_2_b3_mt) + (qtd_perguntas_2_b4_mt * qtd_professores_2_b4_mt)
    total_perguntas_2_pt = (qtd_perguntas_2_b1_pt * qtd_professores_2_b1_pt) + (qtd_perguntas_2_b2_pt * qtd_professores_2_b2_pt) + (qtd_perguntas_2_b3_pt * qtd_professores_2_b3_pt) + (qtd_perguntas_2_b4_pt * qtd_professores_2_b4_pt)
    total_perguntas_5_mt = (qtd_perguntas_5_b1_mt * qtd_professores_5_b1_mt) + (qtd_perguntas_5_b2_mt * qtd_professores_5_b2_mt) + (qtd_perguntas_5_b3_mt * qtd_professores_5_b3_mt) + (qtd_perguntas_5_b4_mt * qtd_professores_5_b4_mt)
    total_perguntas_5_pt = (qtd_perguntas_5_b1_pt * qtd_professores_5_b1_pt) + (qtd_perguntas_5_b2_pt * qtd_professores_5_b2_pt) + (qtd_perguntas_5_b3_pt * qtd_professores_5_b3_pt) + (qtd_perguntas_5_b4_pt * qtd_professores_5_b4_pt)
    total_perguntas_9_mt = (qtd_perguntas_9_b1_mt * qtd_professores_9_b1_mt) + (qtd_perguntas_9_b2_mt * qtd_professores_9_b2_mt) + (qtd_perguntas_9_b3_mt * qtd_professores_9_b3_mt) + (qtd_perguntas_9_b4_mt * qtd_professores_9_b4_mt)
    total_perguntas_9_pt = (qtd_perguntas_9_b1_pt * qtd_professores_9_b1_pt) + (qtd_perguntas_9_b2_pt * qtd_professores_9_b2_pt) + (qtd_perguntas_9_b3_pt * qtd_professores_9_b3_pt) + (qtd_perguntas_9_b4_pt * qtd_professores_9_b4_pt)
    total_perguntas_3_mt = (qtd_perguntas_3_b1_mt * qtd_professores_3_b1_mt) + (qtd_perguntas_3_b2_mt * qtd_professores_3_b2_mt) + (qtd_perguntas_3_b3_mt * qtd_professores_3_b3_mt) + (qtd_perguntas_3_b4_mt * qtd_professores_3_b4_mt)
    total_perguntas_3_pt = (qtd_perguntas_3_b1_pt * qtd_professores_3_b1_pt) + (qtd_perguntas_3_b2_pt * qtd_professores_3_b2_pt) + (qtd_perguntas_3_b3_pt * qtd_professores_3_b3_pt) + (qtd_perguntas_3_b4_pt * qtd_professores_3_b4_pt)
    total_perguntas_mt = total_perguntas_2_mt + total_perguntas_5_mt + total_perguntas_9_mt + total_perguntas_3_mt
    total_perguntas_pt = total_perguntas_2_pt + total_perguntas_5_pt + total_perguntas_9_pt + total_perguntas_3_pt

    total_respostas_2_mt = qtd_respostas_2_b1_mt + qtd_respostas_2_b2_mt + qtd_respostas_2_b3_mt + qtd_respostas_2_b4_mt
    total_respostas_2_pt = qtd_respostas_2_b1_pt + qtd_respostas_2_b2_pt + qtd_respostas_2_b3_pt + qtd_respostas_2_b4_pt
    total_respostas_5_mt = qtd_respostas_5_b1_mt + qtd_respostas_5_b2_mt + qtd_respostas_5_b3_mt + qtd_respostas_5_b4_mt
    total_respostas_5_pt = qtd_respostas_5_b1_pt + qtd_respostas_5_b2_pt + qtd_respostas_5_b3_pt + qtd_respostas_5_b4_pt
    total_respostas_9_mt = qtd_respostas_9_b1_mt + qtd_respostas_9_b2_mt + qtd_respostas_9_b3_mt + qtd_respostas_9_b4_mt
    total_respostas_9_pt = qtd_respostas_9_b1_pt + qtd_respostas_9_b2_pt + qtd_respostas_9_b3_pt + qtd_respostas_9_b4_pt
    total_respostas_3_mt = qtd_respostas_3_b1_mt + qtd_respostas_3_b2_mt + qtd_respostas_3_b3_mt + qtd_respostas_3_b4_mt
    total_respostas_3_pt = qtd_respostas_3_b1_pt + qtd_respostas_3_b2_pt + qtd_respostas_3_b3_pt + qtd_respostas_3_b4_pt
    total_respostas_mt = total_respostas_2_mt + total_respostas_5_mt + total_respostas_9_mt + total_respostas_3_mt
    total_respostas_pt = total_respostas_2_pt + total_respostas_5_pt + total_respostas_9_pt + total_respostas_3_pt

    if total_perguntas_mt == 0 :
        por_mt = 0
    else:
        por_mt = (total_respostas_mt * 100) / total_perguntas_mt
    if total_perguntas_pt == 0 :
        por_pt = 0
    else:
        por_pt = (total_respostas_pt * 100) / total_perguntas_pt



    data_json={
        'totalV': "%.2f" % por_geral,
        'totalF': "%.2f" % (100 - por_geral),
        'total_serie_2': "%.2f" % por_2,
        'total_serie_5': "%.2f" % por_5,
        'total_serie_9': "%.2f" % por_9,
        'total_serie_3': "%.2f" % por_3,
        'total_b1': "%.2f" % por_b1,
        'total_b2': "%.2f" % por_b2,
        'total_b3': "%.2f" % por_b3,
        'total_b4': "%.2f" % por_b4,
        'por_2_b1': "%.2f" % por_2_b1,
        'por_2_b2': "%.2f" % por_2_b2,
        'por_2_b3': "%.2f" % por_2_b3,
        'por_2_b4': "%.2f" % por_2_b4,
        'por_5_b1': "%.2f" % por_5_b1,
        'por_5_b2': "%.2f" % por_5_b2,
        'por_5_b3': "%.2f" % por_5_b3,
        'por_5_b4': "%.2f" % por_5_b4,
        'por_9_b1': "%.2f" % por_9_b1,
        'por_9_b2': "%.2f" % por_9_b2,
        'por_9_b3': "%.2f" % por_9_b3,
        'por_9_b4': "%.2f" % por_9_b4,
        'por_3_b1': "%.2f" % por_3_b1,
        'por_3_b2': "%.2f" % por_3_b2,
        'por_3_b3': "%.2f" % por_3_b3,
        'por_3_b4': "%.2f" % por_3_b4,
        'por_juris_cap': "%.2f" % por_juris_cap,
        'por_juris_int': "%.2f" % (100 - por_juris_cap),
        'por_int': "%.2f" % por_int,
        'por_cap': "%.2f" % por_cap,
        'por_cumprimento_em': "%.2f" % por_cumprimento_em,
        'por_cumprimento_ef': "%.2f" % por_cumprimento_ef,
        'por_mt' : "%.2f" % por_mt,
        'por_pt' : "%.2f" % por_pt,
        'por_2_mat': "%.2f" % por_2_mat,
        'por_2_vesp': "%.2f" % por_2_vesp,
        'por_2_not': "%.2f" % por_2_not,
        'por_2_integ': "%.2f" % por_2_integ,
        'por_5_mat': "%.2f" % por_5_mat,
        'por_5_vesp': "%.2f" % por_5_vesp,
        'por_5_not': "%.2f" % por_5_not,
        'por_5_integ': "%.2f" % por_5_integ,
        'por_9_mat': "%.2f" % por_9_mat,
        'por_9_vesp': "%.2f" % por_9_vesp,
        'por_9_not': "%.2f" % por_9_not,
        'por_9_integ': "%.2f" % por_9_integ,
        'por_3_mat': "%.2f" % por_3_mat,
        'por_3_vesp': "%.2f" % por_3_vesp,
        'por_3_not': "%.2f" % por_3_not,
        'por_3_integ': "%.2f" % por_3_integ,
        'por_mat': "%.2f" % por_mat,
        'por_vesp': "%.2f" % por_vesp,
        'por_not': "%.2f" % por_not,
        'por_integ': "%.2f" % por_integ,
    }


    return JsonResponse(data_json)


# coordenadoria cumprimento
@login_required
def coordenadoria_cumprimento(request):
    coordenadorias =Coordenadoria.objects.all().order_by('id')
    respostas = []
    professores = []
    qtd_perguntas = []
    qtd_respostas = []
    qtd_professores = []
    cont_res = 0
    cont_prof = 0
    cont_res_v = 0
    for coordenadoria in coordenadorias:
        professores_coord = Professor.objects.filter(coordenadoria_id=coordenadoria.id)
        for professor in professores_coord:
            resposta = Resposta.objects.filter(professor_id=professor.id)
            if resposta.count() != 0:
                professores.append(professor)
                respostas.append(resposta)
    for coordenadoria in coordenadorias:
        cont_res =0
        cont_res_v = 0
        for professor in professores:
            if professor.coordenadoria_id == coordenadoria.id:
                for resposta in respostas:
                    for res in resposta:
                        if res.professor_id == professor.id:
                            if res.foi_possivel == 1:
                                cont_res += 1
                                if res.resposta == 1:
                                    cont_res_v += 1
        qtd_respostas.append(cont_res_v)
        qtd_perguntas.append(cont_res)


    for coordenadoria in coordenadorias:
        cont_prof = 0
        for professor in professores:
            if professor.coordenadoria_id == coordenadoria.id:
                for resposta in respostas:
                    for res in resposta:
                        if res.professor_id == professor.id:
                            if res.foi_possivel == 1:
                                cont_prof += 1
                            break
        qtd_professores.append(cont_prof)

    print("qtd total de perguntas: ", qtd_perguntas[0])
    print("qtd total de respostas verdadeiras: ", qtd_respostas[0])
    print("qtd total de professores que responderam: ", qtd_professores[0])

    por_coord = []
    for i in range(68):
        if qtd_professores[i] == 0 or qtd_perguntas[i] == 0:
            calculo = 0
            por_coord.append(calculo)
        else:
            if (qtd_perguntas[i] * qtd_professores[i]) == 0 :
                calculo = 0
            else :
                calculo = (qtd_respostas[i] * 100) / (qtd_perguntas[i] * qtd_professores[i])
            por_coord.append("%.2f" % calculo)

    cap_coord = []
    for i in range (7):
        print("cont : ", i)
        cap_coord.append(por_coord[i])

    int_coord = []
    for i in range (68):
        print("cont2 : ", i+7)
        int_coord.append(por_coord[i+7])

    data_json={
        'por_coord':  por_coord,
        'cap_coord': cap_coord,
        'int_coord': int_coord,
    }
    return JsonResponse(data_json)

#escolas controle
@login_required
def grap_escolas(request):

    escolas = Escola.objects.raw('SELECT * FROM app_escola')
    qtd_escolas = len(escolas)
    escolas_visitadas_v = Resposta.objects.raw('SELECT * FROM app_resposta as r JOIN app_professor as p on p.id = r.professor_id JOIN app_escola as e on e.id = escola_id WHERE r.resposta = 1 and foi_possivel = 1 group by escola_id;')
    escolas_visitadas_falso = Resposta.objects.raw('SELECT * FROM app_resposta as r JOIN app_professor as p on p.id = r.professor_id JOIN app_escola as e on e.id = escola_id WHERE r.resposta = 0 and foi_possivel = 0 group by escola_id;')
    qtd_escolas_visitadas = len(escolas_visitadas_v)
    escolas_visitadas = Resposta.objects.raw('SELECT * FROM app_resposta as r JOIN app_professor as p on p.id = r.professor_id JOIN app_escola as e on e.id = escola_id  group by escola_id;')
    qtd_escolas_visitadas_v_f = len(escolas_visitadas)
    por_escolas_visitadas = (qtd_escolas_visitadas_v_f* 100)/qtd_escolas
    por_escolas_visitadas_sim = (qtd_escolas_visitadas*100)/qtd_escolas_visitadas_v_f
    qtd_escolas_visitadas_f = len(escolas_visitadas_falso)

    motivos = ["Escola exclusivamente em atividade remota","Escola no período de coleta sem atividade presencial","Professor ausente ou de atestado/licença","Professor afastado","Professor se recusou a participar da entrevista","Outros"]
    qtd_motivos =[]
    for motivo in motivos:
        qtd_motivo =0
        for escola in escolas_visitadas_falso:
            if motivo == escola.motivo:
                qtd_motivo += 1
        qtd_motivos.append(qtd_motivo)
    por_motivo = []
    for i in range(6):
        if qtd_escolas_visitadas_f == 0 :
            calculo_por = 0
        else :
            calculo_por = (qtd_motivos[i]*100)/qtd_escolas_visitadas_f
        por_motivo.append("%.2f" % calculo_por)



    data_json={
        'por_escolas_visitadas': "%.2f" % por_escolas_visitadas,
        'por_escolas_nao_visitadas': "%.2f" % (100 - por_escolas_visitadas),
        'por_escolas_visitadas_sim': "%.2f" % por_escolas_visitadas_sim,
        'por_escolas_visitadas_nao': "%.2f" % (100 - por_escolas_visitadas_sim),
        'motivos': motivos,
        'por_motivo': por_motivo,
    }

    return JsonResponse(data_json)

@login_required
def getRelatorio(request):
    escolas_visitadas = Resposta.objects.raw('SELECT * FROM app_resposta as r JOIN app_professor as p on p.id = r.professor_id JOIN app_escola as e on e.id = escola_id group by escola_id;')
    escolas_visitadas_falso = Resposta.objects.raw('SELECT * FROM app_resposta as r JOIN app_professor as p on p.id = r.professor_id JOIN app_escola as e on e.id = escola_id WHERE  foi_possivel = 0 group by professor_id;')
    qtd_escolas_visitadas = len(escolas_visitadas)
    qtd_escolas_visitadas_f = len(escolas_visitadas_falso)
    context ={
        'qtd_escolas_visitadas': qtd_escolas_visitadas,
        'qtd_escolas_visitadas_f': qtd_escolas_visitadas_f,
    }
    return render(request, "relatorio.html", context)

@login_required
def lista_escolas(request):

    # Conexão com o banco de dados MySQL
    cnx = mysql.connector.connect(user='root', password='1234',
                                  host='localhost', database='agora_vai')
    cursor = cnx.cursor()

    # Execução da consulta
    query = 'SELECT escola FROM agora_vai.app_resposta as r JOIN agora_vai.app_professor as p on p.id =r.professor_id JOIN agora_vai.app_escola as e on e.id = escola_id group by escola;'
    cursor.execute(query)
    result = cursor.fetchall()

    # Criação do objeto DataFrame
    df = pd.DataFrame(result, columns=['Escola'])

    # Salva a tabela em um arquivo Excel
    writer = pd.ExcelWriter('tabela_escolas_visitadas.xlsx', engine='openpyxl')
    df.to_excel(writer, index=False)
    writer.close()

    # Retorna o arquivo Excel como um HttpResponse
    with open('tabela_escolas_visitadas.xlsx', 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=tabela_escolas_visitadas.xlsx'
        return response

@login_required
def lista_escolas_recusadas(request):
    # Conexão com o banco de dados MySQL
    cnx = mysql.connector.connect(user='root', password='1234',
                                  host='localhost', database='agora_vai')
    cursor = cnx.cursor()

    # Execução da consulta
    query = 'SELECT nome,motivo,escola FROM agora_vai.app_resposta as r JOIN agora_vai.app_professor as p on p.id =r.professor_id JOIN agora_vai.app_escola as e on e.id = escola_id WHERE foi_possivel = 0 group by professor_id;'
    cursor.execute(query)
    result = cursor.fetchall()

    # Criação do objeto DataFrame
    df = pd.DataFrame(result, columns=['Professor','Motivo','Escola'])

    # Salva a tabela em um arquivo Excel
    writer = pd.ExcelWriter('tabela_Professores_nao_responderam.xlsx', engine='openpyxl')
    df.to_excel(writer, index=False)
    writer.close()

    # Retorna o arquivo Excel como um HttpResponse
    with open('tabela_Professores_nao_responderam.xlsx', 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=tabela_Professores_nao_responderam.xlsx'
        return response

