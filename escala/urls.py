from django.urls import path
from . import views

app_name = 'escala'

urlpatterns = [
    path('', views.escala_hoje, name='escala-hoje'),
    path('periodos/', views.PeriodoListView.as_view(), name='periodo-list'),
    path('periodo/<int:pk>/', views.PeriodoDetailView.as_view(), name='periodo-detail'),
    path('plantonistas/', views.PlantonistaListView.as_view(), name='plantonista-list'),
    path('secretarias/', views.SecretariaListView.as_view(), name='secretaria-list'),
    path('contatos/', views.ContatoEmergencialListView.as_view(), name='contato-list'),
]