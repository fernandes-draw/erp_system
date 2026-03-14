from django.urls import path
from .views import AmostraCreateView, AmostraListView

urlpatterns = [
    path('amostras/', AmostraListView.as_view(), name='amostra_list'),
    path('amostras/nova/', AmostraCreateView.as_view(), name='amostra_create'),
]