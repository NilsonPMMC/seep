from django.contrib import admin
from .models import Secretaria, Plantonista, Periodo, ContatoEmergencial, Escala

@admin.register(Secretaria)
class SecretariaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'escala_ativa')
    list_filter = ('escala_ativa',)
    search_fields = ('nome',)

@admin.register(Plantonista)
class PlantonistaAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'secretaria', 'telefones')
    list_filter = ('secretaria',)
    search_fields = ('nome_completo', 'secretaria__nome')
    autocomplete_fields = ('usuario',) # Melhora a seleção de usuário

class EscalaInline(admin.TabularInline):
    """
    Permite adicionar e editar a escala (vincular plantonistas)
    diretamente na tela de cadastro do Período. É muito mais prático.
    """
    model = Escala
    extra = 1  # Quantidade de linhas extras para adicionar novos plantonistas
    autocomplete_fields = ('plantonista',) # Facilita encontrar plantonistas

@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'data_inicio', 'data_fim')
    list_filter = ('data_inicio',)
    search_fields = ('descricao',)
    inlines = [EscalaInline] # Adiciona o Inline que criamos acima

@admin.register(ContatoEmergencial)
class ContatoEmergencialAdmin(admin.ModelAdmin):
    list_display = ('orgao', 'telefones')
    search_fields = ('orgao',)