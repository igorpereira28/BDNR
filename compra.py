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
    for compra in banco.find({}):
        print(compra["usuario"]["nome"], compra["vendedor"]["nome"], compra["produto"]["nome"], compra["valor"], compra["quantidade"], compra["total gasto"])