from django import forms
from .models import Venda


class IdentificacaoForm(forms.Form):
    """Tela 1: so pede o nome e sobrenome do comprador."""

    nome = forms.CharField(
        label="Nome e sobrenome",
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Ex.: Joanderson Barbosa", "autofocus": True}),
    )

    def clean_nome(self):
        nome = self.cleaned_data["nome"].strip()
        if len(nome.split()) < 2:
            raise forms.ValidationError("Digite nome e sobrenome.")
        return " ".join(palavra.capitalize() for palavra in nome.split())


class PagamentoForm(forms.Form):
    """Parte da Tela 2: so o campo de forma de pagamento (os produtos sao tratados a parte)."""

    forma_pagamento = forms.ChoiceField(
        label="Forma de pagamento",
        choices=Venda.FORMAS_PAGAMENTO,
        widget=forms.RadioSelect,
        initial=Venda.PAGAR_NA_HORA,
    )
