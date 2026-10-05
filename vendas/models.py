from django.db import models


class Produto(models.Model):
    """Um item vendido no mini mercado (biscoito, chocolate, etc.)."""

    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    imagem = models.ImageField(upload_to="produtos/", blank=True, null=True)
    ativo = models.BooleanField(
        default=True,
        help_text="Desmarque para parar de exibir este produto na tela de compra, sem apaga-lo do historico.",
    )

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Comprador(models.Model):
    """Pessoa que realizou uma ou mais compras."""

    nome = models.CharField(max_length=150)

    def __str__(self):
        return self.nome


class Venda(models.Model):
    """Uma compra registrada: um comprador, um conjunto de itens e uma forma de pagamento."""

    PAGAR_NA_HORA = "na_hora"
    PAGAR_FIM_DO_MES = "fim_do_mes"
    FORMAS_PAGAMENTO = [
        (PAGAR_NA_HORA, "Pagarei agora"),
        (PAGAR_FIM_DO_MES, "Pagar no fim do mes"),
    ]

    STATUS_PENDENTE = "pendente"
    STATUS_PAGO = "pago"
    STATUS_CHOICES = [
        (STATUS_PENDENTE, "Pendente"),
        (STATUS_PAGO, "Pago"),
    ]

    comprador = models.ForeignKey(Comprador, on_delete=models.PROTECT, related_name="vendas")
    data_hora = models.DateTimeField(auto_now_add=True)
    forma_pagamento = models.CharField(max_length=20, choices=FORMAS_PAGAMENTO)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDENTE)
    valor_total = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        ordering = ["-data_hora"]

    def __str__(self):
        return f"Venda #{self.pk} - {self.comprador.nome}"

    def recalcular_total(self):
        """Soma os itens da venda e atualiza valor_total. Chamado apos criar os itens."""
        total = sum((item.subtotal() for item in self.itens.all()), 0)
        self.valor_total = total
        self.save(update_fields=["valor_total"])
        return total


class ItemVenda(models.Model):
    """Uma linha da venda: um produto, uma quantidade, e o preco no momento da compra."""

    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Preco do produto no momento da compra (nao muda se o preco do produto mudar depois).",
    )

    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"
