import datetime
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
    date = input('Insira a data da compra no formato br com / ex: 22/01/2022: ').split('/')
    day, month, year = [int(item) for item in date]
    data = datetime.datetime(year, month, day)
    total = valor * quantidade
    salvar = {"usuario": usuario, "vendedor": vendedor, "produto": produto, "valor": valor, "quantidade": quantidade, "data": data, "total gasto": total}
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
            "\nData da compra:", compra["data"].strftime("%d/%m/%Y"),
            "\nTotal gasto:", compra["total gasto"],
            "\n--------------------------------"
        )

def atualizarCompra(db):
    #update compra
    banco = db.compra
    bancoUsuario = db.usuario
    bancoVendedor = db.vendedor
    bancoProduto = db.produto
    print("\nAtualizando as compras")
    print("\nPara atualizarmos, precisamos saber o nome do cliente, do vendedor, do produto e o dia")
    nomeUsuario = input("Nome do cliente: ")
    nomeVendedor = input("Nome do vendedor: ")
    nomeProduto = input("Nome do produto: ")
    date = input('Insira a data da compra no formato br com / ex: 22/01/2022: ').split('/')
    day, month, year = [int(item) for item in date]
    dataCompra = datetime.datetime(year, month, day)
    filtro = {}
    if nomeUsuario:
        filtro["usuario.nome"] = nomeUsuario
    if nomeVendedor:
        filtro["vendedor.nome"] = nomeVendedor
    if nomeProduto:
        filtro["produto.nome"] = nomeProduto
    if dataCompra:
        filtro["data"] = dataCompra
    for compra in banco.find(filtro):
        print(
            "\nCliente:", compra["usuario"]["nome"],
            "\nVendedor:", compra["vendedor"]["nome"],
            "\nProduto comprado:", compra["produto"]["nome"],
            "\nValor do produto:", compra["valor"],
            "\nQuantidade comprada:", compra["quantidade"],
            "\nData da compra:", compra["data"].strftime("%d/%m/%Y"),
            "\nTotal gasto:", compra["total gasto"],
            "\n"
        )
        confirmacao = input("É este? S / N ")
        if (confirmacao == "S"):
            key = 0
            while (key != 'S'):
                print("1-Atualizar cliente")
                print("2-Atualizar Vendedor")
                print("3-Atualizar Produto")
                print("4-Atualizar data")

                key = input("Digite a opção desejada? (V para voltar) ")

                if (key == '1'):
                    print("Alterar cliente")
                    usuario = None
                    while not usuario:
                        nomeUsuario = input("Qual usuário está realizando a compra? ")
                        usuario = bancoUsuario.find_one({"nome": nomeUsuario})
                        if not usuario:
                            print("Usuário não encontrado")
                            continue
                    salvar = {"usuario": usuario}
                    salvar = salvar.update({"$set": {"usuario": usuario}})

                elif (key == '2'):
                    print("Alterar vendedor")
                    vendedor = None
                    while not vendedor:
                        nomeVendedor = input("Qual vendedor está realizando a operação? ")
                        vendedor = bancoVendedor.find_one({"nome": nomeVendedor})
                        if not vendedor:
                            print("Vendedor não encontrado")
                            continue
                    salvar = {"$set": vendedor}
                    banco.update_one(filtro, salvar)
                    # salvar = {"vendedor": vendedor}
                    # salvar = salvar.update_one({"$set": {"vendedor": vendedor}})
                
                elif (key == '3'):
                    print("Alterar produto")
                    produto = None
                    while not produto:
                        nomeProduto = input("Qual produto está sendo comprado? ")
                        produto = bancoProduto.find_one({"nome": nomeProduto})
                        if not produto:
                            print("Produto não encontrado")
                            continue
                    salvar = {"produto": produto}
                    salvar = salvar.update_one({"$set": {"produto": produto}})
                
                elif (key == '4'):
                    print("Alterar data")
                    data = input('Insira a data da compra no formato br com / ex: 22/01/2022: ').split('/')
                    day, month, year = [int(item) for item in date]
                    dataCompra = datetime.datetime(year, month, day)
                    salvar = dataCompra
                    salvar = {"$set": {"data": salvar}}
                    banco.update_one(filtro, salvar)

def cancelarCompra(db):
    #delete compra
    print("\nCancele alguma compra")
    print("\nPara conseguirmos cancelar a compra, precisamos do nome do produto, nome do vendedor, do usuário e a data da compra")
    banco = db.compra
    bancoUsuario = db.usuario
    bancoVendedor = db.vendedor
    bancoProduto = db.produto
    nomeUsuario = input("Digite o nome do cliente: ")
    nomeVendedor = input("Digite o nome do vendedor que realizou a venda: ")
    nomeProduto = input("Digite o nome do produto que foi vendido: ")
    date = input('Insira a data da compra no formato br com / ex: 22/01/2022: ').split('/')
    day, month, year = [int(item) for item in date]
    dataCompra = datetime.datetime(year, month, day)
    filtro = {}
    if nomeUsuario:
        filtro["usuario.nome"] = nomeUsuario
    if nomeVendedor:
        filtro["vendedor.nome"] = nomeVendedor
    if nomeProduto:
        filtro["produto.nome"] = nomeProduto
    if dataCompra:
        filtro["data"] = dataCompra
    for compra in banco.find(filtro):
        print(
            "\nCliente:", compra["usuario"]["nome"],
            "\nVendedor:", compra["vendedor"]["nome"],
            "\nProduto comprado:", compra["produto"]["nome"],
            "\nValor do produto:", compra["valor"],
            "\nQuantidade comprada:", compra["quantidade"],
            "\nData da compra:", compra["data"].strftime("%d/%m/%Y"),
            "\nTotal gasto:", compra["total gasto"],
            "\n"
        )
    confirmacao = input("É ESTA COMPRA QUE VOCÊ DESEJA CANCELAR?: S / N   ")
    if (confirmacao == "S" or confirmacao == "s"):
        mydoc = banco.delete_one(filtro)
        print("Compra Cancelada!")

