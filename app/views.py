from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
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


class IndexView(TemplateView):
    template_name = "index.html"

class ModeloView(TemplateView):
    template_name = "model.html"

class SobreView(TemplateView):
    template_name = "sobre.html"



#Função para autenticar o login
def login(request):
    if request.method == "GET":
        return render(request, 'index.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user =authenticate(username=username, password=senha)

        if user:
            return render(request, 'login.html')
        else:
            return render(request, 'negado.html')

def painel(request):
    return render(request, 'login.html')


@login_required
def plataforma(request):
    if request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        return render('negado.html')

def dashboard(request):
    return render(request, 'dashboard.html')

#Função para cadastrar professor e redirecionar para a página de perguntas
def index(request):
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


        return render(request, "login.html")
    else:
        return render(request, "login.html")

#Funções para carregar os selects dinamicamente
def getCoordenadorias(request):
    data = json.loads(request.body)
    jurisdicao_id = data["id"]
    coordenadorias = Coordenadoria.objects.filter(jurisdicao_id=jurisdicao_id)
    return JsonResponse(list(coordenadorias.values("id", "coordenadoria")), safe=False)

def getEscolas(request):
    data = json.loads(request.body)
    coordenadoria_id = data["id"]
    escolas = Escola.objects.filter(coordenadoria_id=coordenadoria_id)
    return JsonResponse(list(escolas.values("id", "escola")), safe=False)

def getTurnos(request):
    data = json.loads(request.body)
    escola_id = data["id"]
    turnos = Turno.objects.filter(escola_id=escola_id)
    return JsonResponse(list(turnos.values("id", "turno")), safe=False)

def getSeries(request):
    data = json.loads(request.body)
    turno_id = data["id"]
    series = Serie.objects.filter(turno_id=turno_id)
    return JsonResponse(list(series.values("id", "serie")), safe=False)

def getTurmas(request):
    data = json.loads(request.body)
    serie_id = data["id"]
    turmas = Turma.objects.filter(serie_id=serie_id)
    return JsonResponse(list(turmas.values("id", "turma")), safe=False)

def getMaterias(request):

    data = json.loads(request.body)
    serie_id = data["id"]
    materias = Materia.objects.filter(serie_id=serie_id)
    return JsonResponse(list(materias.values("id", "materia")), safe=False)



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




    #calculo b1
    total_perguntas_b1 = (qtd_perguntas_2_b1 * qtd_professores_2_b1) + (qtd_perguntas_5_b1 * qtd_professores_5_b1) + (qtd_perguntas_9_b1 * qtd_professores_9_b1) + (qtd_perguntas_3_b1 * qtd_professores_3_b1)
    total_respostas_b1 = qtd_respostas_2_b1 + qtd_respostas_5_b1 + qtd_respostas_9_b1 + qtd_respostas_3_b1
    por_b1 = (total_respostas_b1 * 100) / total_perguntas_b1

    #calculo b2
    total_perguntas_b2 = (qtd_perguntas_2_b2 * qtd_professores_2_b2) + (qtd_perguntas_5_b2 * qtd_professores_5_b2) + (qtd_perguntas_9_b2 * qtd_professores_9_b2) + (qtd_perguntas_3_b2 * qtd_professores_3_b2)
    total_respostas_b2 = qtd_respostas_2_b2 + qtd_respostas_5_b2 + qtd_respostas_9_b2 + qtd_respostas_3_b2
    por_b2 = (total_respostas_b2 * 100) / total_perguntas_b2

    #calculo b3
    total_perguntas_b3 = (qtd_perguntas_2_b3 * qtd_professores_2_b3) + (qtd_perguntas_5_b3 * qtd_professores_5_b3) + (qtd_perguntas_9_b3 * qtd_professores_9_b3) + (qtd_perguntas_3_b3 * qtd_professores_3_b3)
    total_respostas_b3 = qtd_respostas_2_b3 + qtd_respostas_5_b3 + qtd_respostas_9_b3 + qtd_respostas_3_b3
    por_b3 = (total_respostas_b3 * 100) / total_perguntas_b3

    #calculo b4
    total_perguntas_b4 = (qtd_perguntas_2_b4 * qtd_professores_2_b4) + (qtd_perguntas_5_b4 * qtd_professores_5_b4) + (qtd_perguntas_9_b4 * qtd_professores_9_b4) + (qtd_perguntas_3_b4 * qtd_professores_3_b4)
    total_respostas_b4 = qtd_respostas_2_b4 + qtd_respostas_5_b4 + qtd_respostas_9_b4 + qtd_respostas_3_b4
    por_b4 = (total_respostas_b4 * 100) / total_perguntas_b4

    #calculo geral
    total_perguntas_geral = total_perguntas_b1 + total_perguntas_b2 + total_perguntas_b3 + total_perguntas_b4
    total_respostas_geral = total_respostas_b1 + total_respostas_b2 + total_respostas_b3 + total_respostas_b4
    por_geral = (total_respostas_geral * 100) / total_perguntas_geral

    #calculo das series
    total_perguntas_2 = (qtd_perguntas_2_b1 * qtd_professores_2_b1) + (qtd_perguntas_2_b2 * qtd_professores_2_b2) + (qtd_perguntas_2_b3 * qtd_professores_2_b3) + (qtd_perguntas_2_b4 * qtd_professores_2_b4)
    total_respostas_2 = qtd_respostas_2_b1 + qtd_respostas_2_b2 + qtd_respostas_2_b3 + qtd_respostas_2_b4
    por_2 = (total_respostas_2 * 100) / total_perguntas_2

    total_perguntas_5 = (qtd_perguntas_5_b1 * qtd_professores_5_b1) + (qtd_perguntas_5_b2 * qtd_professores_5_b2) + (qtd_perguntas_5_b3 * qtd_professores_5_b3) + (qtd_perguntas_5_b4 * qtd_professores_5_b4)
    total_respostas_5 = qtd_respostas_5_b1 + qtd_respostas_5_b2 + qtd_respostas_5_b3 + qtd_respostas_5_b4
    por_5 = (total_respostas_5 * 100) / total_perguntas_5

    total_perguntas_9 = (qtd_perguntas_9_b1 * qtd_professores_9_b1) + (qtd_perguntas_9_b2 * qtd_professores_9_b2) + (qtd_perguntas_9_b3 * qtd_professores_9_b3) + (qtd_perguntas_9_b4 * qtd_professores_9_b4)
    total_respostas_9 = qtd_respostas_9_b1 + qtd_respostas_9_b2 + qtd_respostas_9_b3 + qtd_respostas_9_b4
    por_9 = (total_respostas_9 * 100) / total_perguntas_9

    total_perguntas_3 = (qtd_perguntas_3_b1 * qtd_professores_3_b1) + (qtd_perguntas_3_b2 * qtd_professores_3_b2) + (qtd_perguntas_3_b3 * qtd_professores_3_b3) + (qtd_perguntas_3_b4 * qtd_professores_3_b4)
    total_respostas_3 = qtd_respostas_3_b1 + qtd_respostas_3_b2 + qtd_respostas_3_b3 + qtd_respostas_3_b4
    por_3 = (total_respostas_3 * 100) / total_perguntas_3

    #Calculo por serie/bimestre

    total_perguntas_2_b1 = qtd_perguntas_2_b1 * qtd_professores_2_b1
    por_2_b1 = (qtd_respostas_2_b1 * 100) / total_perguntas_2_b1

    total_perguntas_2_b2 = qtd_perguntas_2_b2 * qtd_professores_2_b2
    por_2_b2 = (qtd_respostas_2_b2 * 100) / total_perguntas_2_b2

    total_perguntas_2_b3 = qtd_perguntas_2_b3 * qtd_professores_2_b3
    por_2_b3 = (qtd_respostas_2_b3 * 100) / total_perguntas_2_b3

    total_perguntas_2_b4 = qtd_perguntas_2_b4 * qtd_professores_2_b4
    por_2_b4 = (qtd_respostas_2_b4 * 100) / total_perguntas_2_b4


    total_perguntas_5_b1 = qtd_perguntas_5_b1 * qtd_professores_5_b1
    por_5_b1 = (qtd_respostas_5_b1 * 100) / total_perguntas_5_b1

    total_perguntas_5_b2 = qtd_perguntas_5_b2 * qtd_professores_5_b2
    por_5_b2 = (qtd_respostas_5_b2 * 100) / total_perguntas_5_b2

    total_perguntas_5_b3 = qtd_perguntas_5_b3 * qtd_professores_5_b3
    por_5_b3 = (qtd_respostas_5_b3 * 100) / total_perguntas_5_b3

    total_perguntas_5_b4 = qtd_perguntas_5_b4 * qtd_professores_5_b4
    por_5_b4 = (qtd_respostas_5_b4 * 100) / total_perguntas_5_b4


    total_perguntas_9_b1 = qtd_perguntas_9_b1 * qtd_professores_9_b1
    por_9_b1 = (qtd_respostas_9_b1 * 100) / total_perguntas_9_b1

    total_perguntas_9_b2 = qtd_perguntas_9_b2 * qtd_professores_9_b2
    por_9_b2 = (qtd_respostas_9_b2 * 100) / total_perguntas_9_b2

    total_perguntas_9_b3 = qtd_perguntas_9_b3 * qtd_professores_9_b3
    por_9_b3 = (qtd_respostas_9_b3 * 100) / total_perguntas_9_b3

    total_perguntas_9_b4 = qtd_perguntas_9_b4 * qtd_professores_9_b4
    por_9_b4 = (qtd_respostas_9_b4 * 100) / total_perguntas_9_b4



    total_perguntas_3_b1 = qtd_perguntas_3_b1 * qtd_professores_3_b1
    por_3_b1 = (qtd_respostas_3_b1 * 100) / total_perguntas_3_b1

    total_perguntas_3_b2 = qtd_perguntas_3_b2 * qtd_professores_3_b2
    por_3_b2 = (qtd_respostas_3_b2 * 100) / total_perguntas_3_b2

    total_perguntas_3_b3 = qtd_perguntas_3_b3 * qtd_professores_3_b3
    por_3_b3 = (qtd_respostas_3_b3 * 100) / total_perguntas_3_b3

    total_perguntas_3_b4 = qtd_perguntas_3_b4 * qtd_professores_3_b4
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
    por_int = (total_respostas_int * 100) / total_perguntas_int

    por_juris_cap = (total_respostas_cap * 100) / (total_respostas_cap + total_respostas_int)

    #cumprimento do curriculo por nivel de ensino
    total_perguntas_em = total_perguntas_3_b1 + total_perguntas_3_b2 + total_perguntas_3_b3 + total_perguntas_3_b4
    total_perguntas_ef = total_perguntas_2_b1 + total_perguntas_2_b2 + total_perguntas_2_b3 + total_perguntas_2_b4 + total_perguntas_5_b1 + total_perguntas_5_b2 + total_perguntas_5_b3 + total_perguntas_5_b4 + total_perguntas_9_b1 + total_perguntas_9_b2 + total_perguntas_9_b3 + total_perguntas_9_b4
    total_respostas_em = qtd_respostas_3_b1 + qtd_respostas_3_b2 + qtd_respostas_3_b3 + qtd_respostas_3_b4
    total_respostas_ef = qtd_respostas_2_b1 + qtd_respostas_2_b2 + qtd_respostas_2_b3 + qtd_respostas_2_b4 + qtd_respostas_5_b1 + qtd_respostas_5_b2 + qtd_respostas_5_b3 + qtd_respostas_5_b4 + qtd_respostas_9_b1 + qtd_respostas_9_b2 + qtd_respostas_9_b3 + qtd_respostas_9_b4
    por_cumprimento_em = (total_respostas_em * 100) / total_perguntas_em
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

    por_mt = (total_respostas_mt * 100) / total_perguntas_mt
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
    }


    return JsonResponse(data_json)


# Jurisdição cumprimento


