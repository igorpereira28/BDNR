from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import datetime
from usuario import create_usuario, read_usuario, update_usuario, delete_usuario, adicionarFavoritos, visualizarFavoritos, excluirFavorito
from vendedor import create_vendedor, read_vendedor, update_vendedor, delete_vendedor
from produto import create_produto, read_produto, update_produto, delete_produto
from compra import realizarCompra, visualizarCompra, cancelarCompra
from uri import uri

uri = uri

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercadolivre

key = 0
sub = 0
while (key != 'S'):
    print("1-CRUD Usuário")
    print("2-CRUD Vendedor")
    print("3-CRUD Produto")
    print("4-CRUD Compra")
    key = input("Digite a opção desejada? (S para sair) ")

    if (key == '1'):
        print("Menu do Usuário")
        print("1-Create Usuário")
        print("2-Read Usuário")
        print("3-Update Usuário")
        print("4-Delete Usuário")
        print("---------FAVORITOS-----------")
        print("5-Adicionar Favoritos")
        print("6-Visualizar Favoritos")
        print("7-Excluir Favoritos")
        sub = input("Digite a opção desejada? (V para voltar) ")
        if (sub == '1'):
            print("Create usuario")
            create_usuario(db)
            
        elif (sub == '2'):
            nome = input("Read usuário, deseja algum nome especifico? ")
            read_usuario(db, nome)
        
        elif (sub == '3'):
            nome = input("Update usuário, deseja algum nome especifico? ")
            update_usuario(db, nome)

        elif (sub == '4'):
            print("delete usuario")
            nome = input("Nome a ser deletado: ")
            sobrenome = input("Sobrenome a ser deletado: ")
            delete_usuario(db, nome, sobrenome)

        elif (sub == '5'):
            adicionarFavoritos(db)

        elif (sub == '6'):
            visualizarFavoritos(db)

        elif (sub == '7'):
            excluirFavorito(db)
            
    elif (key == '2'):
        print("Menu do Vendedor")    
        print("1-Create Vendedor")
        print("2-Read Vendedor")
        print("3-Update Vendedor")
        print("4-Delete Vendedor")
        sub = input("Digite a opção desejada? (V para voltar) ")
        if (sub == '1'):
            print("Create Vendedor")
            create_vendedor(db)
            
        elif (sub == '2'):
            nome = input("Read vendedor, deseja algum nome especifico? ")
            read_vendedor(db, nome)
        
        elif (sub == '3'):
            nome = input("Update vendedor, deseja algum nome especifico? ")
            update_vendedor(db, nome)

        elif (sub == '4'):
            print("delete vendedor")
            nome = input("Nome a ser deletado: ")
            sobrenome = input("Sobrenome a ser deletado: ")
            delete_vendedor(db, nome, sobrenome)
            
    elif (key == '3'):
        print("Menu do Produto")
        print("1-Create Produto")
        print("2-Read Produto")
        print("3-Update Produto")
        print("4-Delete Produto")
        sub = input("Digite a opção desejada? (V para voltar) ")
        if (sub == '1'):
            print("Create Produto")
            create_produto(db)
            
        elif (sub == '2'):
            nome = input("Read produto, deseja algum nome especifico? ")
            read_produto(db, nome)
        
        elif (sub == '3'):
            nome = input("Update produto, deseja algum nome especifico? ")
            update_produto(db, nome)

        elif (sub == '4'):
            print("delete produto")
            nome = input("Nome a ser deletado: ")
            valor = input("Valor a ser deletado: ")
            delete_produto(db, nome, valor)

    elif (key == '4'):
        print("Menu da Compra")
        print("1-Realizar Compra")
        print("2-Visualizar Compra")
        print("3-Cancelar Compra")
        sub = input("Digite a opção desejada? (V para voltar) ")

        if (sub == '1'):
            realizarCompra(db)
        
        elif (sub == '2'):
            visualizarCompra(db)

        # elif (sub == '3'):
        #     atualizarCompra(db)

        elif (sub == '3'):
            cancelarCompra(db)