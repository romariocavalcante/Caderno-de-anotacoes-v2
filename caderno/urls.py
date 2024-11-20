from django.urls import path
from . import views

urlpatterns = [
    path('', views.anotacoes, name="anotacoes"),
    path('cliente/<int:id>', views.anotacoes, name="cliente_id"),
    path('adicionar_itens_cliente/', views.anotacoes, name='adicionar_itens_cliente'),
    path('adicionar_cliente', views.adicionar_cliente, name="adicionar_cliente"),
    path('historico', views.historico, name="historico"),
    path('deletar_cliente/<int:cliente_id>/', views.deletar_cliente, name="deletar_cliente"),
]
