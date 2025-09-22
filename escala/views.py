from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, DetailView
from .models import Periodo, ContatoEmergencial, Plantonista, Secretaria

def escala_hoje(request):
    """
    Esta é a view principal (página inicial) do sistema.
    Ela busca o período de plantão que está ATIVO no momento.
    Se não houver nenhum ativo, ela busca o PRÓXIMO período a acontecer.
    """
    agora = timezone.now()
    contexto = {}

    # 1. Tenta encontrar um período de plantão ativo
    periodo_ativo = Periodo.objects.filter(data_inicio__lte=agora, data_fim__gte=agora).first()

    if periodo_ativo:
        contexto['periodo'] = periodo_ativo
        contexto['status'] = 'ativo'
    else:
        # 2. Se não houver, encontra o próximo período a começar
        proximo_periodo = Periodo.objects.filter(data_inicio__gt=agora).order_by('data_inicio').first()
        contexto['periodo'] = proximo_periodo
        contexto['status'] = 'proximo'

    # Adiciona também os contatos emergenciais na página principal para acesso rápido
    contexto['contatos_emergenciais'] = ContatoEmergencial.objects.all()

    return render(request, 'escala/escala_hoje.html', contexto)

class PeriodoListView(ListView):
    """
    Lista todos os períodos de plantão, do mais recente para o mais antigo.
    Ideal para ver o histórico ou as escalas futuras.
    """
    model = Periodo
    template_name = 'escala/periodo_list.html'  # Template que vamos criar
    context_object_name = 'periodos'  # Nome da variável no template
    ordering = ['-data_inicio']  # O '-' indica ordem decrescente
    paginate_by = 10  # Mostra 10 períodos por página

class PeriodoDetailView(DetailView):
    """
    Mostra os detalhes de um único período de plantão, incluindo
    todos os plantonistas escalados para ele.
    """
    model = Periodo
    template_name = 'escala/periodo_detail.html' # Template que vamos criar
    context_object_name = 'periodo'

class PlantonistaListView(ListView):
    """
    Lista todos os plantonistas cadastrados.
    """
    model = Plantonista
    template_name = 'escala/plantonista_list.html'
    context_object_name = 'plantonistas'
    paginate_by = 15

class SecretariaListView(ListView):
    """
    Lista todas as secretarias.
    """
    model = Secretaria
    template_name = 'escala/secretaria_list.html'
    context_object_name = 'secretarias'

class ContatoEmergencialListView(ListView):
    """
    Página dedicada para listar todos os contatos emergenciais.
    """
    model = ContatoEmergencial
    template_name = 'escala/contato_list.html'
    context_object_name = 'contatos'