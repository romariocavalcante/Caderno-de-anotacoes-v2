from django.db import models

# Endereço
class Endereco(models.Model):
    rua = models.CharField(max_length=150, blank=True, null=True, verbose_name="Rua")
    numero = models.CharField(max_length=10, blank=True, null=True, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    bairro = models.CharField(max_length=100, blank=True, null=True, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    estado = models.CharField(max_length=2, verbose_name="Estado")
    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.cidade}-{self.estado}"
    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

# Cliente
class Cliente(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    contato = models.CharField(max_length=200, verbose_name="Contato")
    observacao = models.TextField(blank=True, null=True, verbose_name="Observação")
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, verbose_name="Endereço")
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

# Item
class Item(models.Model):
    nome = models.CharField(max_length=200, unique=True, verbose_name="Nome")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Itens"

# Cliente + Item
class ClienteItem(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Item")
    quantidade = models.PositiveIntegerField(default=1, verbose_name="Quantidade")
    data_registro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Registro")
    def __str__(self):
        return f"{self.cliente.nome} - {self.item.nome} - {self.quantidade} ({self.data_registro}x)"
    class Meta:
        verbose_name = "Cliente Item"
        verbose_name_plural = "Cliente Itens"

# Histórico
class HistoricoCliente(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Item")
    quantidade = models.PositiveIntegerField(default=1, verbose_name="Quantidade")
    data_registro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Registro")
    def __str__(self):
        return f"{self.cliente.nome} - {self.item.nome} - {self.quantidade} ({self.data_registro}x)"
    class Meta:
        verbose_name = "Histórico"
        verbose_name_plural = "Histórico"

class Observacoes(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    observacoes = models.TextField(verbose_name="Observações")

    def __str__(self):
        return f"Observação para {self.cliente.nome}"

    class Meta:
        verbose_name = "Observação"
        verbose_name_plural = "Observações"