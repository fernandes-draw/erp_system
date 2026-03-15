from django.db import models
from django.conf import settings
import datetime


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

    codigo_peca = models.CharField(
        max_length=50, verbose_name="Código da Peça (Cliente)"
    )
    descricao = models.CharField(max_length=255)
    cliente_nome = models.CharField(max_length=100)
    peso_amostra = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True
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
    peso_teorico = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,  # peso modelo 3D com sobre-metal calculado pelo software CAD
    )
    sobremetal = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Sobremetal (mm)",
    )
    quantidade_figuras = models.PositiveIntegerField(
        default=1, verbose_name="Figuras no Molde"
    )
    observacoes = models.TextField(blank=True, null=True)

    # Imagem do CAD
    imagem_cad = models.ImageField(upload_to="projetos/cad/", null=True, blank=True)

    # Estrutura ColdBox
    caixa_alta = models.BooleanField(default=False)
    caixa_baixa = models.BooleanField(default=False)
    qtd_caixas_macho = models.PositiveIntegerField(default=0)

    data_inicio = models.DateTimeField(auto_now_add=True)
    ultima_atualização = models.DateTimeField(auto_now_add=True)
    responsavel_atual = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    # Campo para definir quem assume a próxima etapa
    responsavel_proxima_fase = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projetos_a_assumir",
    )

    @property
    def imagem_exibicao(self):
        # Se houver imagem do CAD, usa ela. Se não, usa a da amostra.
        if self.imagem_cad:
            return self.imagem_cad.url
        elif self.amostra.foto:
            return self.amostra.foto.url
        return None

    def save(self, *args, **kwargs):
        if not self.codigo_projeto:
            # Busca o último projeto cadastrado
            ultimo_projeto = Projeto.objects.order_by("id").last()

            if not ultimo_projeto:
                # Se for o primeiro projeto do sistema
                novo_numero = 1
            else:
                # Pega o código do último (ex: P-000123) remove o "P-",
                # convert em int e soma 1
                ultimo_codigo = ultimo_projeto.codigo_projeto  # string "P-000123"
                numero_limpo = int(ultimo_codigo.replace("P-", ""))
                novo_numero = numero_limpo + 1

            # Formata com prefixo e 6 dígitos (zfill preenche com zeros à esquerda)
            self.codigo_projeto = f"P-{str(novo_numero).zfill(6)}"
        super(Projeto, self).save(*args, **kwargs)

    def __str__(self):
        return self.codigo_projeto
