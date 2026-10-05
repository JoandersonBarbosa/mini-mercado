from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import IdentificacaoForm, PagamentoForm
from .models import Produto, Comprador, Venda, ItemVenda


def identificacao(request):
    """Tela 1: pede nome e sobrenome, guarda na sessao e segue para a Tela 2."""
    if request.method == "POST":
        form = IdentificacaoForm(request.POST)
        if form.is_valid():
            request.session["nome_comprador"] = form.cleaned_data["nome"]
            return redirect("vendas:produtos")
    else:
        form = IdentificacaoForm()

    return render(request, "vendas/identificacao.html", {"form": form})


def produtos(request):
    """Tela 2: selecao de produtos + forma de pagamento, tudo na mesma tela."""
    nome_comprador = request.session.get("nome_comprador")
    if not nome_comprador:
        # Ninguem pula a Tela 1: sem nome na sessao, volta para o inicio.
        return redirect("vendas:identificacao")

    produtos_disponiveis = Produto.objects.filter(ativo=True)

    if request.method == "POST":
        pagamento_form = PagamentoForm(request.POST)

        # Monta a lista de itens escolhidos a partir dos campos qtd_<id> do formulario.
        itens_escolhidos = []
        for produto in produtos_disponiveis:
            qtd_bruta = request.POST.get(f"qtd_{produto.id}", "0")
            try:
                quantidade = int(qtd_bruta)
            except ValueError:
                quantidade = 0
            if quantidade > 0:
                itens_escolhidos.append((produto, quantidade))

        if not itens_escolhidos:
            messages.error(request, "Selecione ao menos um produto antes de confirmar.")
        elif pagamento_form.is_valid():
            comprador = Comprador.objects.create(nome=nome_comprador)
            venda = Venda.objects.create(
                comprador=comprador,
                forma_pagamento=pagamento_form.cleaned_data["forma_pagamento"],
            )
            for produto, quantidade in itens_escolhidos:
                ItemVenda.objects.create(
                    venda=venda,
                    produto=produto,
                    quantidade=quantidade,
                    preco_unitario=produto.preco,
                )
            venda.recalcular_total()

            # Limpa a sessao para a proxima pessoa comecar do zero.
            del request.session["nome_comprador"]

            return redirect("vendas:confirmacao", venda_id=venda.id)
    else:
        pagamento_form = PagamentoForm()

    total_estimado = Decimal("0")
    contexto = {
        "produtos": produtos_disponiveis,
        "pagamento_form": pagamento_form,
        "nome_comprador": nome_comprador,
    }
    return render(request, "vendas/produtos.html", contexto)


def confirmacao(request, venda_id):
    """Tela 3: resumo da compra ja registrada."""
    venda = get_object_or_404(Venda, id=venda_id)
    return render(request, "vendas/confirmacao.html", {"venda": venda})
