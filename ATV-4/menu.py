from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json

from usuario import *
from vendedor import *
from produto import *


cloud_config= {
  'secure_connect_bundle': 'secure-connect-mercadolivre.zip'
}

with open("mercadolivre-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect('mercadolivre')

opcao = 0
while(opcao != 'S'):
    print("\n1 - CRUD de Usuários")
    print("2 - CRUD de Vendedores")
    print("3 - CRUD de Produtos")
    print("4 - CRUD de Compras")
    opcao = input("Selecione uma opção. (S para sair) ").upper()

    acao = 0
    match opcao:
        case '1':
            while(acao != 'V'):
                print("1 - Cadastrar um novo usuário")
                print("2 - Excluir um usuário")
                print("3 - Listar informações de um usuário")
                print("4 - Atualizar informações de um usuário")
                acao = input("Selecione uma ação. (V para voltar) ").upper()
                match acao:
                    case '1':
                        create_usuario(session)
                    case '2':
                        delete_usuario(session)
                    case '3':
                        read_usuario(session)
                    case '4':
                        update_usuario(session)
                    case '5':
                        compra_usuario(session)
        case '2':
             while(acao != 'V'):
                print("1 - Cadastrar um novo vendedor")
                print("2 - Excluir um vendedor")
                print("3 - Listar informações de um vendedor")
                print("4 - Atualizar informações de um vendedor")
                acao = input("Selecione uma ação. (V para voltar) ").upper()
                match acao:
                    case '1':
                        create_vendedor(session)
                    case '2':
                        delete_vendedor(session)
                    case '3':
                        read_vendedor(session)
                    case '4':
                        update_vendedor(session)
        case '3':
             while(acao != 'V'):
                print("1 - Cadastrar um novo produto")
                print("2 - Excluir um produto")
                print("3 - Listar informações de um produto")
                print("4 - Atualizar informações de um produto")
                acao = input("Selecione uma ação. (V para voltar) ").upper()
                match acao:
                    case '1':
                        create_produto(session)
                    case '2':
                        delete_produto(session)
                    case '3':
                        read_produto(session)
                    case '4':
                        update_produto(session)

        case '4':
             while(acao != 'V'):
                print("1 - Cadastrar uma nova compra")
                print("2 - Excluir uma compra")
                print("3 - Listar todas as compras")
                acao = input("Selecione uma ação. (V para voltar) ").upper()
                match acao:
                    case '1':
                        create_compra(session)
                    case '2':
                        delete_compra(session)
                    case '3':
                        read_compra(session)