from django.urls import path
from . import views

urlpatterns = [
    path('', views.anotacoes, name="anotacoes"),

    # Cliente
    path('cliente/<int:id>/', views.anotacoes, name="cliente_id"),
    path('adicionar_cliente', views.adicionar_cliente, name="adicionar_cliente"),
    path('deletar_cliente/<int:cliente_id>/', views.deletar_cliente, name="deletar_cliente"),
    path('adicionar_itens_cliente/', views.adicionar_itens_cliente, name='adicionar_itens_cliente'),
    path('cliente/<int:cliente_id>/deletar_item/<int:item_id>/', views.deletar_item_cliente, name="deletar_item_cliente"),

    # historico
    path('historico', views.historico, name="historico"),
]


