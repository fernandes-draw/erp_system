from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from accounts.models import CustomUser
from .models import Amostra, Projeto, ProjetoObservacao
from .forms import AmostraForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json


class AmostraCreateView(LoginRequiredMixin, CreateView):
    model = Amostra
    form_class = AmostraForm
    template_name = "desenvolvimento/amostra_form.html"
    success_url = reverse_lazy("amostra_list")

    def form_valid(self, form):
        form.instance.cadastrado_por = self.request.user
        return super().form_valid(form)


class AmostraListView(LoginRequiredMixin, ListView):
    model = Amostra
    template_name = "desenvolvimento/amostra_list.html"
    context_object_name = "amostras"
    ordering = ["-data_recebimento"]


class ProjetoKanbanView(LoginRequiredMixin, ListView):
    model = Projeto
    template_name = "desenvolvimento/projeto_kanban.html"
    context_object_name = "projetos"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Passamos as fases para o template criar as colunas
        context["fases"] = Projeto.STATUS_PROJETO
        return context


def iniciar_projeto(request, amostra_id):
    amostra = get_object_or_404(Amostra, id=amostra_id)

    # Verifica se já existe um projeto para essa amostra
    if hasattr(amostra, "projeto"):
        messages.warning(
            request, "Esta amostra já possui um projeto vinculado.")
    else:
        # Cria o projeto. O método save() que editamos acima
        # vai gerar o código P-00000X automaticamente.
        projeto = Projeto.objects.create(
            amostra=amostra, responsavel_atual=request.user, status="0_aguardando"
        )
        messages.success(
            request, f"Projeto {projeto.codigo_projeto} iniciado com sucesso!"
        )

    return redirect("amostra_list")


@login_required
@require_POST
def atualizar_status_projeto(request):
    try:
        data = json.loads(request.body)
        projeto = get_object_or_404(Projeto, id=data.get("projeto_id"))

        # Atualiza o status e define quem moveu como o responsável atual
        projeto.status = data.get("novo_status")
        projeto.responsavel_atual = request.user
        projeto.save()

        return JsonResponse(
            {
                "status": "success",
                # Forçamos a conversão para string para garantir o #hexadecimal
                "nova_cor": str(request.user.cor_identificadora),
                "nome_usuario": request.user.get_full_name() or request.user.username,
            }
        )
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


@login_required
def detalhes_projeto_json(request, projeto_id):
    # O get_object_or_404 previne erros se o ID não existir
    projeto = get_object_or_404(Projeto, id=projeto_id)

    try:
        # Busca a lista de usuários para o select do modal
        usuarios = [
            {"id": u.id, "nome": u.get_full_name() or u.username}
            for u in CustomUser.objects.all()
        ]

        # Monta os dados principais do projeto
        data = {
            "id": projeto.id,
            "codigo": projeto.codigo_projeto,
            "peca": projeto.amostra.codigo_peca,
            "cliente": projeto.amostra.cliente_nome,
            "status_nome": projeto.get_status_display(),
            "peso_teorico": str(projeto.peso_teorico) if projeto.peso_teorico else "",
            "sobremetal": str(projeto.sobremetal) if projeto.sobremetal else "",
            "quantidade_figuras": projeto.quantidade_figuras,
            "observacoes": projeto.observacoes or "",  # Se ainda usar o campo fixo
            "usuarios": usuarios,
            "responsavel_atual_id": (
                projeto.responsavel_atual.id if projeto.responsavel_atual else None
            ),
            # Usando imagem_cad.url para evitar o erro de 'imagem_exibicao'
            "imagem_url": projeto.imagem_cad.url if projeto.imagem_cad else None,
        }

        # Adiciona a lista de observações do histórico
        data["observacoes_historico"] = [
            {
                "usuario": obs.usuario.get_full_name() or obs.usuario.username,
                "texto": obs.texto,
                "data": obs.data_registro.strftime("%d/%m/%y %H:%M"),
                "cor": getattr(obs.usuario, "cor_identificadora", "#17a2b8"),
            }
            for obs in projeto.historico_observacoes.all()
        ]

        return JsonResponse(data)

    except Exception as e:
        # Isso aparecerá no terminal do VS Code se algo der errado
        print(f"ERRO NA VIEW: {e}")
        return JsonResponse({"error": str(e)}, status=500)


@require_POST
def salvar_edicao_projeto(request):
    projeto_id = request.POST.get("projeto_id")
    projeto = get_object_or_404(Projeto, id=projeto_id)

    try:
        # Tratando strings vazias para campos numéricos
        peso = request.POST.get("peso_teorico")
        projeto.peso_teorico = float(peso.replace(
            ',', '.')) if peso and peso.strip() else 0

        sobremetal = request.POST.get("sobremetal")
        projeto.sobremetal = float(sobremetal.replace(
            ',', '.')) if sobremetal and sobremetal.strip() else 0

        qtd_figuras = request.POST.get("quantidade_figuras")
        projeto.quantidade_figuras = int(
            qtd_figuras) if qtd_figuras and qtd_figuras.strip() else 1

        projeto.observacoes = request.POST.get("observacoes")

        # Ajuste do Responsável
        novo_resp_id = request.POST.get("proximo_responsavel")
        if novo_resp_id and novo_resp_id.strip():
            projeto.responsavel_atual_id = int(novo_resp_id)
            # Verifique se o nome correto no model é fase ou etapa:
            projeto.responsavel_proxima_fase_id = int(novo_resp_id)

        if "imagem_cad" in request.FILES:
            projeto.imagem_cad = request.FILES["imagem_cad"]

        projeto.save()
        return JsonResponse({"status": "success", "message": "Atualizado!"})

    except Exception as e:
        # Isso ajuda a ver o erro real no terminal
        print(f"Erro ao salvar projeto: {e}")
        return JsonResponse({"status": "error", "message": str(e)})
    projeto_id = request.POST.get("projeto_id")
    projeto = Projeto.objects.get(id=projeto_id)

    try:
        # Atualizando campos numéricos e texto
        projeto.peso_teorico = request.POST.get("peso_teorico") or 0
        projeto.sobremetal = request.POST.get("sobremetal") or 0
        projeto.quantidade_figuras = request.POST.get(
            "quantidade_figuras") or 1
        projeto.observacoes = request.POST.get("observacoes")

        # AJUSTE AQUI:
        novo_resp_id = request.POST.get("proximo_responsavel")
        if novo_resp_id:
            # Atualizamos o responsável_atual para que o Kanban reflita a mudança na hora
            projeto.responsavel_atual_id = novo_resp_id
            # Se você usa o campo de 'próxima etapa' para histórico, pode atualizar também:
            projeto.responsavel_proxima_etapa_id = novo_resp_id

        if "imagem_cad" in request.FILES:
            projeto.imagem_cad = request.FILES["imagem_cad"]

        projeto.save()

        return JsonResponse({"status": "success", "message": "Atualizado!"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_POST
def adicionar_observacao(request):
    projeto_id = request.POST.get("projeto_id")
    texto = request.POST.get("texto")

    if texto:
        obs = ProjetoObservacao.objects.create(
            projeto_id=projeto_id, usuario=request.user, texto=texto
        )
        return JsonResponse(
            {
                "status": "success",
                "usuario": obs.usuario.get_full_name() or obs.usuario.username,
                "data": obs.data_registro.strftime("%d/%m/%y %H:%M"),
                "texto": obs.texto,
                # PEGA A COR REAL DO USUÁRIO
                'cor': getattr(obs.usuario, 'cor_identificadora', '#17a2b8')
            }
        )
    return JsonResponse({"status": "error", "message": "Texto vazio"})
