from django.contrib import admin
from .models import Produto, Comprador, Venda, ItemVenda


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "preco", "ativo")
    list_filter = ("ativo",)
    search_fields = ("nome",)


@admin.register(Comprador)
class CompradorAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


class ItemVendaInline(admin.TabularInline):
    """Mostra os itens de uma venda direto na tela da venda, sem precisar abrir outra pagina."""

    model = ItemVenda
    extra = 0
    readonly_fields = ("produto", "quantidade", "preco_unitario")
    can_delete = False


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ("id", "comprador", "data_hora", "forma_pagamento", "status", "valor_total")
    list_filter = ("status", "forma_pagamento", "data_hora")
    search_fields = ("comprador__nome",)
    readonly_fields = ("comprador", "data_hora", "forma_pagamento", "valor_total")
    inlines = [ItemVendaInline]
    actions = ["marcar_como_pago"]

    @admin.action(description="Marcar vendas selecionadas como pagas")
    def marcar_como_pago(self, request, queryset):
        atualizadas = queryset.update(status=Venda.STATUS_PAGO)
        self.message_user(request, f"{atualizadas} venda(s) marcada(s) como paga(s).")
