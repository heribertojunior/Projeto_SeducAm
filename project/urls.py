"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='inicio'),
    path('painel/', views.painel, name ='painel'),
    path('sobre/', views.sobre, name='sobre'),
    path('dashboard', views.dashboard, name = "dashboard"),
    path('relatorio', views.getRelatorio, name = "relatorio"),
    path('formulario/', views.formulario, name ='form'),
    path('resposta/', views.salvarResposta, name='resposta'),
    path('coordenadorias', views.getCoordenadorias, name = "coordenadorias"),
    path('escolas', views.getEscolas, name = "escolas"),
    path('turnos', views.getTurnos, name = "turnos"),
    path('series', views.getSeries, name = "series"),
    path('turmas', views.getTurmas, name = "turmas"),
    path('materias', views.getMaterias, name = "materias"),
    path('dashboard', views.dashboard, name = "dashboard"),
    path('cumprimento', views.getCumprimento, name = "cumprimento"),
    path('coordenadoria', views.coordenadoria_cumprimento, name = "coordenadoria"),
    path('relatorio', views.getRelatorio, name = "relatorio"),
    path('grap_escolas', views.grap_escolas, name = "grap_escolas"),
    path('lista_escolas', views.lista_escolas, name = "lista_escolas"),
    path('painel', views.painel, name = "painel"),
    path('lista_escolas_recusadas', views.lista_escolas_recusadas, name = "lista_escolas_recusadas"),
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

