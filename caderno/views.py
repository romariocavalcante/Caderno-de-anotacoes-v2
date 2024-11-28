from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum, F
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt

# Lista de Clientes
def clientes(request):
    if not Cliente.objects.exists():
        return redirect('adicionar_cliente')
    clientes = Cliente.objects.all()
    context = {'clientes': clientes}
    return render(request, 'clientes.html', context)

# Adicionar Cliente
def adicionar_cliente(request):
    estados = [
        {"sigla": "AC", "nome": "Acre"}, {"sigla": "AL", "nome": "Alagoas"}, 
        {"sigla": "AP", "nome": "Amapá"}, {"sigla": "AM", "nome": "Amazonas"},
        {"sigla": "BA", "nome": "Bahia"}, {"sigla": "CE", "nome": "Ceará"},
        {"sigla": "DF", "nome": "Distrito Federal"}, {"sigla": "ES", "nome": "Espírito Santo"},
        {"sigla": "GO", "nome": "Goiás"}, {"sigla": "MA", "nome": "Maranhão"},
        {"sigla": "MT", "nome": "Mato Grosso"}, {"sigla": "MS", "nome": "Mato Grosso do Sul"},
        {"sigla": "MG", "nome": "Minas Gerais"}, {"sigla": "PA", "nome": "Pará"},
        {"sigla": "PB", "nome": "Paraíba"}, {"sigla": "PR", "nome": "Paraná"},
        {"sigla": "PE", "nome": "Pernambuco"}, {"sigla": "PI", "nome": "Piauí"},
        {"sigla": "RJ", "nome": "Rio de Janeiro"}, {"sigla": "RN", "nome": "Rio Grande do Norte"},
        {"sigla": "RS", "nome": "Rio Grande do Sul"}, {"sigla": "RO", "nome": "Rondônia"},
        {"sigla": "RR", "nome": "Roraima"}, {"sigla": "SC", "nome": "Santa Catarina"},
        {"sigla": "SP", "nome": "São Paulo"}, {"sigla": "SE", "nome": "Sergipe"},
        {"sigla": "TO", "nome": "Tocantins"}
    ]
    estado_padrao, cidade_padrao = "PA", "Canaã dos Carajás"

    if request.method == 'POST':
        nome = request.POST.get('nome')
        contato = request.POST.get('contato')
        rua = request.POST.get('rua')
        numero = request.POST.get('numero')
        complemento = request.POST.get('complemento', '')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')

        if Cliente.objects.filter(nome=nome).exists():
            return render(request, 'adicionar_cliente.html', {
                'estados': estados,
                'estado_padrao': estado_padrao,
                'cidade_padrao': cidade_padrao,
                'erro': f"Um cliente com o nome '{nome}' já existe."
            })

        endereco = Endereco.objects.create(
            rua=rua, numero=numero, complemento=complemento,
            bairro=bairro, cidade=cidade, estado=estado
        )
        Cliente.objects.create(nome=nome, contato=contato, endereco=endereco)
        return redirect('clientes')

    return render(request, 'adicionar_cliente.html', {
        'estados': estados,
        'estado_padrao': estado_padrao,
        'cidade_padrao': cidade_padrao
    })

# Deletar Cliente
def deletar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('clientes')

# Adicionar itens ao Cliente
def adicionar_itens_cliente(request):
    if request.method == "POST":
        cliente_id = request.POST.get("cliente")
        itens_selecionados = request.POST.getlist("itens")
        if cliente_id and itens_selecionados:
            cliente = get_object_or_404(Cliente, id=cliente_id)
            for item_id in itens_selecionados:
                quantidade = int(request.POST.get(f"quantidade_{item_id}", 1))
                item = get_object_or_404(Item, id=item_id)
                ClienteItem.objects.create(cliente=cliente, item=item, quantidade=quantidade)
            return redirect('anotacoes', id=cliente.id)
    return redirect('anotacoes')

@csrf_exempt
def deletar_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_ids = data.get('items', [])
        
        if item_ids:
            # Filtra e deleta apenas os itens selecionados
            itens_deletados = Item.objects.filter(id__in=item_ids).delete()
            return JsonResponse({'success': True, 'message': f'{itens_deletados[0]} itens deletados com sucesso.'})
        else:
            return JsonResponse({'success': False, 'message': 'Nenhum item foi selecionado.'})
    return JsonResponse({'success': False, 'message': 'Método inválido.'})

# Anotações dos Clientes
def anotacoes(request, id=None):
    if request.method == 'POST':
        # Salvar Observação no modelo Cliente
        try:
            # Lê os dados do corpo da requisição
            data = json.loads(request.body)  # Lê o JSON enviado
            observacao = data.get('observacao', '')  # Obtém o campo 'observacao'

            cliente = get_object_or_404(Cliente, id=id)  # Obtém o cliente com o id fornecido
            cliente.observacao = observacao  # Atualiza a observação do cliente
            cliente.save()  # Salva a alteração no banco de dados

            return JsonResponse({'status': 'success', 'message': 'Observação salva com sucesso!'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Erro ao decodificar o JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    # Requisição GET: Renderizar Página
    itens = Item.objects.all()
    cliente, cliente_itens, cliente_selecionado = None, [], False

    if id:
        cliente = get_object_or_404(Cliente, id=id)  # Obtém o cliente
        cliente_itens = ClienteItem.objects.filter(cliente=cliente).select_related('item')  # Obtém os itens do cliente
        cliente_selecionado = True

    total = sum(item.item.preco * item.quantidade for item in cliente_itens)  # Calcula o total
    context = {
        'clientes': Cliente.objects.all(),
        'itens': itens,
        'cliente_itens': cliente_itens,
        'total': total,
        'cliente': cliente,
        'cliente_selecionado': cliente_selecionado,
        'observacao': cliente.observacao if cliente else '',
    }
    return render(request, 'anotacoes.html', context)

# Histórico
# def historico(request):
#     cliente_id = request.GET.get('cliente_id')
#     historico = HistoricoCliente.objects.filter(cliente__id=cliente_id) if cliente_id else HistoricoCliente.objects.all()
#     total = historico.aggregate(total=Sum(F('item__preco') * F('cliente__clienteitem__quantidade')))['total'] or 0
#     context = {
#         'historico': historico,
#         'clientes_unicos': Cliente.objects.all(),
#         'total': total
#     }
#     return render(request, 'historico.html', context)

def historico(request):
    cliente_id = request.GET.get('cliente_id')
    historico = HistoricoCliente.objects.filter(cliente__id=cliente_id) if cliente_id else HistoricoCliente.objects.all()
    total = historico.aggregate(total=Sum(F('item__preco') * F('cliente__clienteitem__quantidade')))['total'] or 0
    context = {
        'historico': historico,
        'clientes_unicos': Cliente.objects.all(),
        'total': total
    }
    return render(request, 'historico.html', context)

# Perfil
def perfil(request):
    return render(request, 'perfil.html')