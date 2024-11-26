from django.urls import path
from . import views

urlpatterns = [
    # Lista de Cliente
    path('', views.clientes, name="clientes"),
    # Anotações dos Clientes
    path('cliente/<int:id>/', views.anotacoes, name="anotacoes"),
    # Adicionar Cliente
    path('adicionar_cliente', views.adicionar_cliente, name="adicionar_cliente"),
    # Deletar Cliente
    path('deletar_cliente/<int:cliente_id>/', views.deletar_cliente, name="deletar_cliente"),
    # Adicionar Item
    path('adicionar_itens_cliente/', views.adicionar_itens_cliente, name='adicionar_itens_cliente'),
    # Deletar Item
    path('deletar-item/', views.deletar_item, name='deletar_item'),

    # historico
    path('historico', views.historico, name="historico"),

    # Perfil
    path('perfil', views.perfil, name="perfil"),
]


