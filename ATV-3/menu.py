from pymongo import MongoClient
from pymongo.server_api import ServerApi
import redis
from vendedor import importar_vendedor, read_vendedor, update_vendedor, delete_vendedor
from produto import importar_produto, read_produto, update_produto, delete_produto
from login import importar_usuarios, listar_e_autenticar_usuarios, criar_conta_login, visualizar_usuarios_disponiveis
from uri import uri, r

uri = uri

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercadolivre
MONGO_CLIENTE = uri
REDIS_HOST = "redis-17717.c308.sa-east-1-1.ec2.cloud.redislabs.com"
REDIS_PORT = 17717
REDIS_PASSWORD = "aa7naO2FUNVdTv92WfPIJs9ZvbtFZv9b"


key = 0
sub = 0
while (key != 'S'):
    print("1-Login")
    print("2-CRUD Vendedor")
    print("3-CRUD Produto")
    key = input("Digite a opção desejada? (S para sair) ")

    if (key == '1'):
        print("1-Importação Usuários do MongoDB para o Redis")
        print("2-Login de Usuário")
        print("3-Criar Conta")
        sub = input("Digite a opção desejada? (V para voltar) ")
        print("")

        if (sub == '1'):
            importar_usuarios(uri, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)
        elif (sub == '2'):
            listar_e_autenticar_usuarios(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)
        elif (sub == '3'):
            print("Usuários existentes:")
            visualizar_usuarios_disponiveis(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)
            
            # Solicitar ao usuário que escolha um usuário existente
            try:
                indice_usuario_existente = int(input("Digite o número correspondente ao usuário existente para criar conta de login: "))
            except ValueError:
                print("Entrada inválida. Digite um número válido.")
                continue

            # Obter as informações do usuário existente usando a função visualizar_usuarios_disponiveis
            usuarios = visualizar_usuarios_disponiveis(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)
            
            if 1 <= indice_usuario_existente <= len(usuarios):
                usuario_selecionado = usuarios[indice_usuario_existente - 1]
                chave_usuario_existente = usuario_selecionado['chave']

                # Solicitar ao usuário que insira o novo login e a nova senha
                login = input("Digite o novo login: ")
                senha = input("Digite a nova senha: ")

                # Criar conta de login para o usuário existente
                criar_conta_login(uri, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, chave_usuario_existente, login, senha)
            else:
                print("Índice inválido. Selecione um número válido.")

    elif (key == '2'):
        print("Menu do Vendedor")
        print("1-Importação Vendedores do MongoDB para o Redis")
        print("2-Read Vendedor")
        print("3-Update Vendedor")
        print("4-Delete Vendedor")
        sub = input("Digite a opção desejada? (V para voltar) ")
        if (sub == '1'):
            importar_vendedor(uri, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)
        elif (sub == '2'):
            read_vendedor(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)
        elif (sub == '3'):
            update_vendedor(uri, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)
        elif (sub == '4'):
            delete_vendedor(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)

    elif (key == '3'):
        print("Menu do Produto")
        print("1-Importação Produtos do MongoDB para o Redis")
        print("2-Read Produto")
        print("3-Update Produto")
        print("4-Delete Produto")
        sub = input("Digite a opção desejada? (V para voltar) ")
        if (sub == '1'):
            importar_produto(uri, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)
        elif (sub == '2'):
            read_produto(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)
        elif (sub == '3'):
            update_produto(uri, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)
        elif (sub == '4'):
            delete_produto(uri, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)