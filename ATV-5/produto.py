from datetime import datetime
import uuid  

def criar_produto(connection):
    try:
        # Conectar ao Neo4j
        connection.connect()

        nome_produto = input("Digite o nome do produto: ")
        descricao = input("Digite a descrição do produto: ")
        preco = input("Digite o preço do produto: ")

        produto_id = str(uuid.uuid4())

        data_cadastro = datetime.now().strftime("%Y-%m-%d")

        query = (
            f"CREATE (:Produto {{id: '{produto_id}', nomeProduto: '{nome_produto}', descricao: '{descricao}', data_cadastro: '{data_cadastro}', preco: '{preco}'}})"
        )

        connection.query(query)

        print("Produto criado com sucesso!")
    finally:
        connection.close()


def listar_produtos(connection):
    try:
        connection.connect()

        query = "MATCH (p:Produto) RETURN p.id AS id, p.nomeProduto AS nome, p.descricao AS descricao, p.data_cadastro AS data_cadastro, p.preco AS preco"

        produtos = connection.query(query)

        if not produtos:
            print("Nenhum produto encontrado.")
            return

        print("Lista de Produtos:")
        for i, produto in enumerate(produtos, start=1):
            print(f"{i}. Nome: {produto['nome']}")

        selected_index = int(input("Digite o número do produto para obter mais informações (0 para sair): "))

        if selected_index == 0:
            return

        produto_selecionado = produtos[selected_index - 1]
        print("\nDetalhes do Produto:")
        print(f"ID: {produto_selecionado['id']}")
        print(f"Nome: {produto_selecionado['nome']}")
        print(f"Descrição: {produto_selecionado['descricao']}")
        print(f"Data de Cadastro: {produto_selecionado['data_cadastro']}")
        print(f"Preço: R${produto_selecionado['preco']}")
    finally:
        connection.close()
