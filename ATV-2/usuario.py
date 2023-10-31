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

#ESTA FUNCIONAL, PORÉM, FALTA FAZER A PESQUISA POR CPF
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

def excluirFavotito(db, filtro={}, nome=None, nomeFavorito=None, indice=None):
    #delete favorito
    print("Excluir Favorito")
    mycol = db.usuario

    nome = input("Digite o nome: ")
    nomeFavorito = input("Qual produto? ")
    indice = None

    if nome is not None:
        filtro["usuario.nome"] = nome
    if nomeFavorito is not None:
        filtro["usuario.favorito"] = nomeFavorito
    if indice is not None:
        filtro["favorito.$index"] = indice

    usuarios = mycol.find(filtro)

    if mycol.count_documents(filtro) > 0:
        for usuario in usuarios:
            # Verifique se o usuário é um documento MongoDB
            if isinstance(usuario, dict):
                # Obtenha o valor do campo "favorito" como uma lista
                favorito = usuario.get("favorito", [])

                # Verifique se o produto existe no favorito do usuário
                for item in favorito:
                    if item == nomeFavorito:
                        favorito.remove(item)
                        mydoc = mycol.update_one({"nome": usuario["nome"]}, {"$set": {"favorito": favorito}})
                        print("Produto excluido do favorito!")
                        print(mydoc)
                        break

                else:
                    print("O produto que você deseja excluir não está no favorito do usuário.")
    else:
        print("Nenhum usuário encontrado.")