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
    totalperguntas = Pergunta.objects.all().count()
    resposta = Resposta.objects.filter(foi_possivel = 1)
    totalV = resposta.filter(resposta = 1).count()
    totalP =(totalV/totalperguntas) * 100
    totalF = 100-totalP
    totalpp = "%.2f" % totalP
    totalff = "%.2f" % totalF
    data_json= {'totalV':totalpp,'totalF': totalff}
    return JsonResponse(data_json)
