from datetime import datetime
import uuid

def criar_vendedor(connection):
    try:
        connection.connect()

        nome_vendedor = input("Digite o nome do vendedor: ")

        id_vendedor = str(uuid.uuid4())

        data_cadastro = datetime.now().strftime("%Y-%m-%d")

        query = (
            f"CREATE (:Vendedor {{id: '{id_vendedor}', nomeVendedor: '{nome_vendedor}', data_cadastro: '{data_cadastro}'}})"
        )

        connection.query(query)

        print("Vendedor criado com sucesso!")
    finally:
        connection.close()

def listar_vendedores(connection):
    try:
        connection.connect()

        # Consulta para listar vendedores e produtos atrelados
        query_listar_vendedores = (
            "MATCH (v:Vendedor)-[:Vende]->(p:Produto) "
            "RETURN v.id AS id_vendedor, v.nomeVendedor AS nome_vendedor, "
            "p.id AS id_produto, p.nomeProduto AS nome_produto, p.descricao AS descricao_produto, "
            "p.preco AS preco_produto, p.data_cadastro AS data_cadastro_produto"
        )

        vendedores_produtos = connection.query(query_listar_vendedores)

        print("Lista de Vendedores:")
        vendedores = set()
        for vendedor_produto in vendedores_produtos:
            vendedores.add((vendedor_produto['id_vendedor'], vendedor_produto['nome_vendedor']))

        for i, (id_vendedor, nome_vendedor) in enumerate(vendedores, start=1):
            print(f"{i}. Nome: {nome_vendedor}")

        try:
            index_vendedor = int(input("Digite o número do vendedor desejado (0 para sair): "))
            if index_vendedor == 0:
                return

            vendedor_selecionado = next(
                (v for v in vendedores if v[0] == vendedores_produtos[index_vendedor - 1]['id_vendedor']),
                None
            )

            if vendedor_selecionado:
                print("\nDetalhes do Vendedor:")
                print(f"ID: {vendedor_selecionado[0]}")
                print(f"Nome: {vendedor_selecionado[1]}")

                print("\nProdutos Atrelados:")
                for produto in vendedores_produtos:
                    if produto['id_vendedor'] == vendedor_selecionado[0]:
                        print(f"  - ID Produto: {produto['id_produto']}")
                        print(f"    Nome Produto: {produto['nome_produto']}")
                        print(f"    Descrição Produto: {produto['descricao_produto']}")
                        print(f"    Preço Produto: {produto['preco_produto']}")
                        print(f"    Data Cadastro Produto: {produto['data_cadastro_produto']}")
            else:
                print("Vendedor não encontrado.")
        except (ValueError, IndexError):
            print("Seleção inválida.")
    finally:
        connection.close()