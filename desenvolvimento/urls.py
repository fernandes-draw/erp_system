from django.urls import path
from .views import AmostraCreateView, AmostraListView, ProjetoKanbanView, atualizar_status_projeto, iniciar_projeto

urlpatterns = [
    path('amostras/', AmostraListView.as_view(), name='amostra_list'),
    path('amostras/nova/', AmostraCreateView.as_view(), name='amostra_create'),
    path('amostras/iniciar-projeto/<int:amostra_id>/', iniciar_projeto, name='iniciar_projeto'),
    path('kanban/', ProjetoKanbanView.as_view(), name='projeto_kanban'),
    path('kanban/update/', atualizar_status_projeto, name='atualizar_status_projeto'),
]