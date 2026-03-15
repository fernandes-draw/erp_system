from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from accounts.models import CustomUser
from .models import Amostra, Projeto
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
        messages.warning(request, "Esta amostra já possui um projeto vinculado.")
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
    projeto = get_object_or_404(Projeto, id=projeto_id)
    usuarios = [
        {"id": u.id, "nome": u.get_full_name() or u.username}
        for u in CustomUser.objects.all()
    ]

    data = {
        "id": projeto.id,
        "codigo": projeto.codigo_projeto,
        "peca": projeto.amostra.codigo_peca,
        "cliente": projeto.amostra.cliente_nome,
        "status_nome": projeto.get_status_display(),
        "peso_teorico": str(projeto.peso_teorico) if projeto.peso_teorico else "",
        "sobremetal": str(projeto.sobremetal) if projeto.sobremetal else "",
        "quantidade_figuras": projeto.quantidade_figuras,
        "observacoes": projeto.observacoes or "",
        "resultado_metalografia": projeto.amostra.requer_analise_metalografica,  # Apenas pra saber se requer
        "usuarios": usuarios,
        "responsavel_proxima_id": (
            projeto.responsavel_proxima_fase.id
            if projeto.responsavel_proxima_fase
            else None
        ),
        'imagem_url': projeto.imagem_exibicao if projeto.imagem_exibicao else None,
    }
    return JsonResponse(data)
