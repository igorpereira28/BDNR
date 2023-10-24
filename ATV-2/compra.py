def realizarCompra(db):
    #create compra
    banco = db.compra
    bancoUsuario = db.usuario
    bancoVendedor = db.vendedor
    bancoProduto = db.produto
    print("\nRealizando uma nova compra")
    print("\nUsuários disponíveis")
    for usuario in bancoUsuario.find({}):
        print(usuario["nome"])
    usuario = None
    while not usuario:
        nomeUsuario = input("Qual usuário está realizando a compra? ")
        usuario = bancoUsuario.find_one({"nome": nomeUsuario})
        if not usuario:
            print("Usuário não encontrado")
            continue
    print("\nEscolha um vendedor")
    for vendedor in bancoVendedor.find({}):
        print(vendedor["nome"])
    vendedor = None
    while not vendedor:
        nomeVendedor = input("Qual vendedor está realizando a operação? ")
        vendedor = bancoVendedor.find_one({"nome": nomeVendedor})
        if not vendedor:
            print("Vendedor não encontrado")
            continue
    print("\nEscolha um produto")
    for produto in bancoProduto.find({}):
        print(produto["nome"])
    produto = None
    while not produto:
        nomeProduto = input("Qual produto está sendo comprado? ")
        produto = bancoProduto.find_one({"nome": nomeProduto})
        if not produto:
            print("Produto não encontrado")
            continue
    valor = produto["valor"]
    quantidade = int(input("Quantos itens? "))
    total = valor * quantidade
    salvar = {"usuario": usuario, "vendedor": vendedor, "produto": produto, "valor": valor, "quantidade": quantidade, "total gasto": total}
    x = db.compra.insert_one(salvar)
    print("Compra realizada com sucesso!")
    print("Documento inserido com ID ", x.inserted_id)

def visualizarCompra(db):
    #read compra
    banco = db.compra
    bancoUsuario = db.usuario
    bancoVendedor = db.vendedor
    bancoProduto = db.produto
    print("\nVisualizando as compras")
    nomeUsuario = input("Deseja filtrar por algum usuário especifico? ")
    nomeVendedor = input("Deseja filtrar por algum vendedor especifico? ")
    nomeProduto = input("Deseja filtrar por algum produto especifico? ")
    filtro = {}
    if nomeUsuario:
        filtro["usuario.nome"] = nomeUsuario
    if nomeVendedor:
        filtro["vendedor.nome"] = nomeVendedor
    if nomeProduto:
        filtro["produto.nome"] = nomeProduto

    for compra in banco.find(filtro):
        print(
            "Cliente:", compra["usuario"]["nome"],
            "\nVendedor:", compra["vendedor"]["nome"],
            "\nProduto comprado:", compra["produto"]["nome"],
            "\nValor do produto:", compra["valor"],
            "\nQuantidade comprada:", compra["quantidade"],
            "\nTotal gasto:", compra["total gasto"],
            "\n--------------------------------"
            )