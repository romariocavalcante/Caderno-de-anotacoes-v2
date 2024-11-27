from django.urls import path
from . import views
from . import consumers


urlpatterns = [
    # Lista de Clientes
    path('', views.clientes, name="clientes"),


    # Anotações dos Clientes (inclui salvar observações)
    path('cliente/<int:id>/', views.anotacoes, name="anotacoes"),

    # path('cliente/<int:id>/', consumers.AnotacoesConsumer.as_asgi(), name='anotacoes'),


    # Adicionar Cliente
    path('adicionar_cliente', views.adicionar_cliente, name="adicionar_cliente"),
    # Deletar Cliente
    path('deletar_cliente/<int:cliente_id>/', views.deletar_cliente, name="deletar_cliente"),
    # Adicionar Item
    path('adicionar_itens_cliente/', views.adicionar_itens_cliente, name='adicionar_itens_cliente'),
    # Deletar Item
    path('deletar-item/', views.deletar_item, name='deletar_item'),
    # Histórico
    path('historico', views.historico, name="historico"),
    # Perfil
    path('perfil', views.perfil, name="perfil"),
]


websocket_urlpatterns = [
    path('cliente/<int:id>/', consumers.AnotacoesConsumer.as_asgi(), name='anotacoes'),
]
