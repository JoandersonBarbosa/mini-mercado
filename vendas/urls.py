from django.urls import path
from . import views

app_name = "vendas"

urlpatterns = [
    path("", views.identificacao, name="identificacao"),
    path("produtos/", views.produtos, name="produtos"),
    path("confirmacao/<int:venda_id>/", views.confirmacao, name="confirmacao"),
]
