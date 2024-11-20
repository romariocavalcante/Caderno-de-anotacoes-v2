from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F
from .models import *

# View Anotações -------------------------------------------/
def anotacoes(request, id=None):
    # Verifica se há clientes cadastrados
    if not Cliente.objects.exists():
        return redirect('adicionar_cliente')
    
    itens = Item.objects.all()
    clientes = Cliente.objects.all()

    if id:
        cliente = get_object_or_404(Cliente, id=id)
        cliente_itens = ClienteItem.objects.filter(cliente=cliente).select_related('item')
    else:
        cliente = None
        cliente_itens = ClienteItem.objects.all().select_related('cliente', 'item')

    # Calcular o total dos itens (preço * quantidade)
    total = sum(cliente_item.item.preco * cliente_item.quantidade for cliente_item in cliente_itens)

    # Passar os dados para o template
    context = {
        'clientes': clientes,
        'itens': itens,
        'cliente_itens': cliente_itens,
        'total': total,
        'cliente': cliente,
    }
    return render(request, 'anotacoes.html', context)



# View Adicionar Cliente -------------------------------------------/
def adicionar_cliente(request):
    estados = [
        {"sigla": "AC", "nome": "Acre"},
        {"sigla": "AL", "nome": "Alagoas"},
        {"sigla": "AP", "nome": "Amapá"},
        {"sigla": "AM", "nome": "Amazonas"},
        {"sigla": "BA", "nome": "Bahia"},
        {"sigla": "CE", "nome": "Ceará"},
        {"sigla": "DF", "nome": "Distrito Federal"},
        {"sigla": "ES", "nome": "Espírito Santo"},
        {"sigla": "GO", "nome": "Goiás"},
        {"sigla": "MA", "nome": "Maranhão"},
        {"sigla": "MT", "nome": "Mato Grosso"},
        {"sigla": "MS", "nome": "Mato Grosso do Sul"},
        {"sigla": "MG", "nome": "Minas Gerais"},
        {"sigla": "PA", "nome": "Pará"},
        {"sigla": "PB", "nome": "Paraíba"},
        {"sigla": "PR", "nome": "Paraná"},
        {"sigla": "PE", "nome": "Pernambuco"},
        {"sigla": "PI", "nome": "Piauí"},
        {"sigla": "RJ", "nome": "Rio de Janeiro"},
        {"sigla": "RN", "nome": "Rio Grande do Norte"},
        {"sigla": "RS", "nome": "Rio Grande do Sul"},
        {"sigla": "RO", "nome": "Rondônia"},
        {"sigla": "RR", "nome": "Roraima"},
        {"sigla": "SC", "nome": "Santa Catarina"},
        {"sigla": "SP", "nome": "São Paulo"},
        {"sigla": "SE", "nome": "Sergipe"},
        {"sigla": "TO", "nome": "Tocantins"}
    ]
    estado_padrao = "PA"
    cidade_padrao = "Canaã dos Carajás"

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

        endereco = Endereco(
            rua=rua,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
        )
        endereco.save()

        cliente = Cliente(
            nome=nome,
            contato=contato,
            endereco=endereco
        )
        cliente.save()
        
        return redirect('anotacoes')
    return render(request, 'adicionar_cliente.html', {
        'estados': estados,
        'estado_padrao': estado_padrao,
        'cidade_padrao': cidade_padrao
    })


# View Deletar Cliente -------------------------------------------------------------/
def deletar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('anotacoes')


# View Histórico -------------------------------------------------------------------/
def historico(request):
    cliente_id = request.GET.get('cliente_id')

    if cliente_id:
        historico = HistoricoCliente.objects.filter(cliente__cliente__id=cliente_id)
    else:
        historico = HistoricoCliente.objects.all()

    total = historico.aggregate(
        total=Sum(F('cliente__quantidade') * F('cliente__item__preco'))
    )['total'] or 0

    clientes_unicos = Cliente.objects.all()

    context = {
        'historico': historico,
        'clientes_unicos': clientes_unicos,
        'total': total,
    }

    return render(request, 'historico.html', context)


