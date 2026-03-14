from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Amostra
from .forms import AmostraForm

class AmostraCreateView(LoginRequiredMixin, CreateView):
    model = Amostra
    form_class = AmostraForm
    template_name = 'desenvolvimento/amostra_form.html'
    success_url = reverse_lazy('amostra_list')

    def form_valid(self, form):
        form.instance.cadastrado_por = self.request.user
        return super().form_valid(form)

class AmostraListView(LoginRequiredMixin, ListView):
    model = Amostra
    template_name = 'desenvolvimento/amostra_list.html'
    context_object_name = 'amostras'
    ordering = ['-data_recebimento']