from django.urls import path
from .views import AmostraCreateView, AmostraListView, iniciar_projeto

urlpatterns = [
    path('amostras/', AmostraListView.as_view(), name='amostra_list'),
    path('amostras/nova/', AmostraCreateView.as_view(), name='amostra_create'),
    path('amostras/iniciar-projeto/<int:amostra_id>/', iniciar_projeto, name='iniciar_projeto'),
]