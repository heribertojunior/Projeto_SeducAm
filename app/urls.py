from django.urls import path
from .views import IndexView, SobreView, ModeloView
from . import views
urlpatterns = [
    path('', IndexView.as_view(), name='inicio'),
    path('sobre/', SobreView.as_view(), name='sobre'),
    path('resposta/', views.salvarResposta, name='resposta'),
    path('login/', views.login, name ='login'),
    #path('criarseries/', views.cadastrarSeries, name ='criarseries'),
    path('cancel/', views.painel, name ='cancel'),
    path('formulario/', views.index, name ='form'),
    path('modelo/', ModeloView.as_view(), name ='modelo'),
    path('coordenadorias', views.getCoordenadorias, name = "coordenadorias"),
    path('escolas', views.getEscolas, name = "escolas"),
    path('turnos', views.getTurnos, name = "turnos"),
    path('series', views.getSeries, name = "series"),
    path('turmas', views.getTurmas, name = "turmas"),
    path('materias', views.getMaterias, name = "materias"),
    path('dashboard', views.dashboard, name = "dashboard"),
    path('cumprimento', views.getCumprimento, name = "cumprimento"),

  #  path('resultado/', views.lista, name='resultado')


]




