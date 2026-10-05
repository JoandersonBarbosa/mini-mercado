from decimal import Decimal

nome = input("Digite o seu nome e sobrenome: ")

produto1qtd = (int(input("Digite a quantidade: ")))
if produto1qtd < 1:
     print("A quantidade do produto 1 deve ser maior que zero.")
else:
    produto1preco = (Decimal(input("Digite o preço: ")))

produto2qtd = (int(input("Digite a quantidade: ")))
if produto2qtd < 1:
    print("A quantidade do produto 2 deve ser maior que zero.")
else:
    produto2preco = (Decimal(input("Digite o preço: ")))

print(f"Produto 1: {produto1qtd} unidades, preço unitário: R$ {produto1preco:.2f}, total: R$ {produto1qtd * produto1preco:.2f}")

print(f"Produto 2: {produto2qtd} unidades, preço unitário: R$ {produto2preco:.2f}, total: R$ {produto2qtd * produto2preco:.2f}")

print(f"Total da compra: R$ {(produto1qtd * produto1preco) + (produto2qtd * produto2preco):.2f}")

pagamento = int(input("Escolha a forma de pagamento: \n 1 - Pagarei agora \n 2 - Pagarei no fim do mês \n"))