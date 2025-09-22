from django.db import models
from django.contrib.auth.models import User

# Boa prática: Usar um model customizado de usuário no futuro pode ser útil,
# mas para começar, vincular ao User padrão é mais rápido e eficiente.

class Secretaria(models.Model):
    """
    Representa uma secretaria da prefeitura.
    """
    nome = models.CharField(max_length=200, unique=True, verbose_name="Nome da Secretaria")
    escala_ativa = models.BooleanField(default=True, verbose_name="Escala Ativa")

    class Meta:
        verbose_name = "Secretaria"
        verbose_name_plural = "Secretarias"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Plantonista(models.Model):
    """
    Representa um servidor que pode ser escalado para um plantão.
    """
    secretaria = models.ForeignKey(Secretaria, on_delete=models.CASCADE, related_name="plantonistas")
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuário do Sistema")    
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")
    telefones = models.CharField(max_length=100, help_text="Separe os números por vírgula. Ex: (11) 99999-8888, (11) 4798-0000", verbose_name="Telefone(s)")
    
    class Meta:
        verbose_name = "Plantonista"
        verbose_name_plural = "Plantonistas"
        ordering = ['nome_completo']

    def __str__(self):
        return f"{self.nome_completo} ({self.secretaria.nome})"

class Periodo(models.Model):
    """
    Representa um período de plantão (um final de semana, um feriado, etc.).
    """
    descricao = models.CharField(max_length=150, verbose_name="Descrição", help_text="Ex: Final de Semana de Carnaval")
    data_inicio = models.DateTimeField(verbose_name="Data de Início")
    data_fim = models.DateTimeField(verbose_name="Data de Fim")
    plantonistas_escalados = models.ManyToManyField(Plantonista, through='Escala', related_name="periodos_escalados")

    class Meta:
        verbose_name = "Período de Plantão"
        verbose_name_plural = "Períodos de Plantão"
        ordering = ['-data_inicio']

    def __str__(self):
        inicio = self.data_inicio.strftime('%d/%m/%Y %H:%M')
        fim = self.data_fim.strftime('%d/%m/%Y %H:%M')
        return f"{self.descricao} ({inicio} a {fim})"

class Escala(models.Model):
    """
    Modelo intermediário para a escala (relação Muitos-para-Muitos).
    Aqui podemos adicionar informações extras sobre a escala, como a data em que foi criada.
    """
    plantonista = models.ForeignKey(Plantonista, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    
    class Meta:
        unique_together = ('plantonista', 'periodo')
        verbose_name = "Escala"
        verbose_name_plural = "Escalas"

    def __str__(self):
        return f"Escala de {self.plantonista.nome_completo} para o período {self.periodo.descricao}"


class ContatoEmergencial(models.Model):
    """
    Armazena contatos importantes de outros órgãos.
    """
    orgao = models.CharField(max_length=150, unique=True, verbose_name="Órgão")
    telefones = models.CharField(max_length=200, help_text="Separe os números por vírgula.", verbose_name="Telefone(s) de Contato")
    observacao = models.TextField(blank=True, null=True, verbose_name="Observação")

    class Meta:
        verbose_name = "Contato Emergencial"
        verbose_name_plural = "Contatos Emergenciais"
        ordering = ['orgao']

    def __str__(self):
        return self.orgao