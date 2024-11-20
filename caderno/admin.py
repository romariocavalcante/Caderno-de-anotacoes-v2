from django.contrib import admin
from .models import *

# Para o modelo Endereco
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('rua', 'numero', 'bairro', 'cidade', 'estado')
    search_fields = ('rua', 'bairro', 'cidade')
    list_filter = ('rua', 'bairro', 'cidade')

# Para o modelo Cliente
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'contato', 'endereco')
    search_fields = ('nome', 'contato')
    list_filter = ('endereco__cidade', 'endereco__estado')

# Para o modelo Item
class ItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco')
    search_fields = ('nome',)
    
# Para o modelo ClienteItem
class ClienteItemAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'item', 'quantidade')
    search_fields = ('cliente__nome', 'item__item__nome')
    list_filter = ('cliente', 'item')

# Para o modelo HistoricoCliente
class HistoricoClienteAdmin(admin.ModelAdmin):
    list_display = ('cliente',)
    search_fields = ('cliente__nome',)
    list_filter = ('cliente',)

# Para o modelo Observacoes
class ObservacoesAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'observacoes')
    search_fields = ('cliente__nome',)
    list_filter = ('cliente',)


# Registrando os modelos com seus respectivos admins
admin.site.register(Endereco, EnderecoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ClienteItem, ClienteItemAdmin)
admin.site.register(HistoricoCliente, HistoricoClienteAdmin)
admin.site.register(Observacoes, ObservacoesAdmin)
