from pymongo import UpdateOne
def delete_usuario(db, nome, sobrenome):
    # Delete
    mycol = db.usuario
    myquery = {"nome": nome, "sobrenome": sobrenome}
    mydoc = mycol.delete_one(myquery)
    print("Deletado o usuário ", mydoc)

def create_usuario(db):
    # Insert
    mycol = db.usuario
    print("\nInserindo um novo usuário")
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    cpf = input("CPF: ")
    key = 1
    end = []
    while (key != 'N'):
        rua = input("Rua: ")
        num = input("Num: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        estado = input("Estado: ")
        cep = input("CEP: ")
        endereco = {
            "rua": rua,
            "num": num,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep
        }
        end.append(endereco)
        key = input("Deseja cadastrar um novo endereço (S/N)? ")
    mydoc = {"nome": nome, "sobrenome": sobrenome, "cpf": cpf, "end": end}
    x = mycol.insert_one(mydoc)
    print("Documento inserido com ID ", x.inserted_id)

def read_usuario(db, nome):
    # Read
    mycol = db.usuario
    print("Usuários existentes: ")
    if not len(nome):
        mydoc = mycol.find().sort("nome")
        for x in mydoc:
            print(x["nome"], x["cpf"])
    else:
        myquery = {"nome": nome}
        mydoc = mycol.find(myquery)
        for x in mydoc:
            print(x)

def update_usuario(db, nome):
    # Update
    mycol = db.usuario
    myquery = {"nome": nome}
    mydoc = mycol.find_one(myquery)
    print("Dados do usuário: ", mydoc)
    nome = input("Mudar Nome:")
    if len(nome):
        mydoc["nome"] = nome

    sobrenome = input("Mudar Sobrenome:")
    if len(sobrenome):
        mydoc["sobrenome"] = sobrenome

    cpf = input("Mudar CPF:")
    if len(cpf):
        mydoc["cpf"] = cpf

    newvalues = {"$set": mydoc}
    mycol.update_one(myquery, newvalues)

def adicionarFavoritos(db):
    #create favorito
    mycol = db.usuario
    bancoProduto = db.produto
    print("\nInserindo um novo favorito")
    print("Primeiramente, selecione um cliente")
    for usuario in mycol.find({}):
        print(usuario["nome"])
    usuario = None
    while not usuario:
        nomeUsuario = input("Qual cliente está favoritando? ")
        usuario = mycol.find_one({"nome": nomeUsuario})
        if not usuario:
            print("Cliente não encontrado")
            continue
    for produto in bancoProduto.find({}):
        print(produto["nome"])
    produto = None
    while not produto:
        nomeProduto = input("Qual produto está sendo favoritado? ")
        produto = bancoProduto.find_one({"nome": nomeProduto})
        if not produto:
            print("Produto não encontrado")
            continue
    # Update the document
    document = mycol.update_one({"nome": usuario["nome"]}, {"$push": {"favorito": [produto["nome"]]}})
    print("Documento atualizado com ID ", document.modified_count)

def visualizarFavoritos(db):
    print("Visualizar Favoritos")
    mycol = db.usuario
    print("Deseja selecionar algum cliente em específico?")
    for usuario in mycol.find({}):
        print(usuario["nome"])
    nome = input("Digite o nome: ")
    if not len(nome):
        mydoc = mycol.find().sort("nome")
        for x in mydoc:
            print(x["nome"], x["favorito"])
            print("-----------------------------------------------")
    else:
        myquery = {"nome": nome}
        mydoc = mycol.find(myquery)
        for x in mydoc:
            print(x["nome"], x["favorito"])
            print("-----------------------------------------------")

def excluirFavorito(db):
    # Delete favorito
    print("Excluir Favoritos")
    mycol = db.usuario
    for usuario in mycol.find({}):
        print(usuario["nome"])
    nome = input("Digite o nome do cliente: ")
    nomeProduto = input("Digite o nome do produto a ser excluído dos favoritos: ")

    # Construa a consulta para encontrar o documento certo
    myquery = {"nome": nome}

    # Recupere o documento
    user_doc = mycol.find_one(myquery)

    if user_doc:
        # Obtenha o campo "favorito"
        favorito = user_doc.get("favorito", [])

        produto_encontrado = False

        if favorito:
            new_favorito = []

            # Percorra todas as matrizes dentro do campo "favorito"
            for arr in favorito:
                if arr != [nomeProduto]:
                    new_favorito.append(arr)

            # Atualize o documento com o novo "favorito"
            mycol.update_one(myquery, {"$set": {"favorito": new_favorito}})
            print("Array dentro de 'favorito' excluído com sucesso!")
        else:
            print("Nenhum favorito encontrado.")
    else:
        print("Cliente não encontrado.")