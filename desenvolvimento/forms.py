from django import forms
from .models import Amostra


class AmostraForm(forms.ModelForm):
    class Meta:
        model = Amostra
        fields = [
            "codigo_peça",
            "descrição",
            "cliente_nome",
            "peso_amostra",
            "liga_produto",
            "foto_amostra",
            "requer_analise_metalografica",
            "requer_analise_dureza",
        ]
        widgets = {
            "codigo_peça": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ex: 1234567"}
            ),
            "descrição": forms.TextInput(attrs={"class": "form-control"}),
            "cliente_nome": forms.TextInput(attrs={"class": "form-control"}),
            "peso_amostra": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.001"}
            ),
            "liga_produto": forms.Select(attrs={"class": "form-select"}),
            "foto_amostra": forms.FileInput(attrs={"class": "form-control"}),
            "requer_analise_metalografica": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "requer_analise_dureza": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }
