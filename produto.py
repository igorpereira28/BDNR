def delete_produto(db, nome, valor):
    # Delete
    mycol = db.produto
    myquery = {"nome": nome}
    myquery = {"valor": valor}
    mydoc = mycol.delete_one(myquery)
    print("Deletado o produto ", mydoc)

def create_produto(db):
    # Insert
    mycol = db.vendedor
    print("\nInserindo um novo produto")
    nome = input("Nome: ")
    valor = input("Valor: ")
    mydoc = {"nome": nome, "valor": valor}
    x = mycol.insert_one(mydoc)
    print("Documento inserido com ID ", x.inserted_id)

def read_produto(db, nome):
    # Read
    mycol = db.produto
    print("Produtos existentes: ")
    if not len(nome):
        mydoc = mycol.find().sort("nome")
        for x in mydoc:
            print(x["nome"], x["valor"])
    else:
        myquery = {"nome": nome}
        mydoc = mycol.find(myquery)
        for x in mydoc:
            print(x)

def update_produto(db, nome):
    # Update
    mycol = db.produto
    myquery = {"nome": nome}
    mydoc = mycol.find_one(myquery)
    print("Dados do produto: ", mydoc)
    nome = input("Mudar Nome:")
    if len(nome):
        mydoc["nome"] = nome

    valor = input("Mudar Valor:")
    if len(valor):
        mydoc["valor"] = valor

    newvalues = {"$set": mydoc}
    mycol.update_one(myquery, newvalues)