from django.db import models
from django.conf import settings


class Amostra(models.Model):
    LIGAS_CHOICE = [
        ("FC-20", "FC-20"),
        ("FC-25", "FC-25"),
        ("GGG-40", "GGG-40"),
        ("GGG-50", "GGG-50"),
        ("GGG-60", "GGG-60"),
        ("GGG-70", "GGG-70"),
        ("GJV", "GJV"),
        ("SiMo", "SiMo"),
    ]

    codigo_peça = models.CharField(
        max_length=50, verbose_name="Código da Peça (Cliente)"
    )
    descrição = models.CharField(max_length=255)
    cliente_nome = models.CharField(max_length=100)
    peso_amostra = models.DecimalField(
        max_length=10, decimal_places=3, null=True, blank=True
    )
    liga_produto = models.CharField(max_length=50, choices=LIGAS_CHOICE)
    foto_amostra = models.ImageField(upload_to="amostras/", null=True, blank=True)

    # Requisitos técnicos
    requer_analise_metalografica = models.BooleanField(default=True)
    requer_analise_dureza = models.BooleanField(default=True)

    data_recebimento = models.DateTimeField(auto_now_add=True)
    cadastrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT
    )

    def __str__(self):
        return f"{self.codigo_peça} - {self.cliente_nome}"


class Projeto(models.Model):
    STATUS_PROJETO = [
        ("0_aguardando", "Aguardando Início"),
        ("1_escaneamento", "Em Escaneamento"),
        ("2_modelagem_cad", "Em Modelagem CAD"),
        ("3_conf_dimensional", "Conferência Dimensional"),
        ("4_analise_compra", "Análise para Compra de Blocos"),
        ("5_finalizacao", "Finalização / Pasta Usinagem"),
        ("6_enviado_ferramentaria", "Enviado para Ferramentaria"),
    ]

    amostra = models.OneToOneField(
        Amostra, on_delete=models.CASCADE, related_name="projeto"
    )
    codigo_projeto = models.CharField(
        max_length=8, unique=True, help_text="Formato: P-000000"
    )
    status = models.CharField(
        max_length=30, choices=STATUS_PROJETO, default="0_aguardando"
    )

    # Detalhes de Análise
    resultado_metalografia = models.TextField(null=True, blank=True)
    resultado_dureza = models.CharField(max_length=100, null=True, blank=True)
    peso_real = models.DecimalField(
        max_length=10, decimal_places=3, null=True, blank=True
    )

    # Estrutura CldBox
    caixa_alta = models.BooleanField(default=False)
    caixa_baixa = models.BooleanField(default=False)
    qtd_caixas_macho = models.PositiveIntegerField(default=0)

    data_inicio = models.DateTimeField(auto_now_add=True)
    ultima_atualização = models.DateTimeField(auto_now_add=True)
    responsavel_atual = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.codigo_projeto
