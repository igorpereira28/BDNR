from database_connect import Neo4jConnection
from usuario import criar_usuario, listar_usuarios
from vendedor import criar_vendedor, listar_vendedores
from produto import criar_produto, listar_produtos
from compra import criar_compra, listar_compras

neo4j_uri = "neo4j+s://17077412.databases.neo4j.io"
neo4j_user = "neo4j"
neo4j_password = "6DI1VqYYaKFHlHYdw0H9JbblupB85gjxVQoC0cecDX0"

# Crie uma instância da classe Neo4jConnection
neo4j_connection = Neo4jConnection(neo4j_uri, neo4j_user, neo4j_password)

def menu_principal():
    while True:
        print("1 - Gerenciar Usuários")
        print("2 - Gerenciar Vendedores")
        print("3 - Gerenciar Produtos")
        print("4 - Gerenciar Compras")
        print("S - Sair")

        key = input("Digite a opção desejada: ").upper()
        print("")

        if key == '1':
            menu_usuario()
        elif key == '2':
            menu_vendedor()
        elif key == '3':
            menu_produto()
        elif key == '4':
            menu_compra()
        elif key == 'S':
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_usuario():
    while True:
        print("1 - Criar Usuário")
        print("2 - Listar Usuários")
        print("V - Voltar")

        sub = input("Digite a opção desejada: ").upper()
        print("")

        if sub == '1':
            criar_usuario(neo4j_connection)
        elif sub == '2':
            listar_usuarios(neo4j_connection)
        elif sub == 'V':
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_vendedor():
    while True:
        print("1 - Criar Vendedor")
        print("2 - Listar Vendedores")
        print("V - Voltar")

        sub = input("Digite a opção desejada: ").upper()
        print("")

        if sub == '1':
            criar_vendedor(neo4j_connection)
        elif sub == '2':
            listar_vendedores(neo4j_connection)
        elif sub == 'V':
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_produto():
    while True:
        print("1 - Criar Produto")
        print("2 - Listar Produtos")
        print("V - Voltar")

        sub = input("Digite a opção desejada: ").upper()
        print("")

        if sub == '1':
            criar_produto(neo4j_connection)
        elif sub == '2':
            listar_produtos(neo4j_connection)
        elif sub == 'V':
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_compra():
    while True:
        print("1 - Criar Compra")
        print("2 - Listar Compras")
        print("V - Voltar")

        sub = input("Digite a opção desejada: ").upper()
        print("")

        if sub == '1':
            criar_compra(neo4j_connection)
        elif sub == '2':
            listar_compras(neo4j_connection)
        elif sub == 'V':
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    try:
        menu_principal()
    finally:
        neo4j_connection.close()