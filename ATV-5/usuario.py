import uuid
from datetime import datetime

def criar_usuario(connection):
    try:
        connection.connect()

        nome_usuario = input("Digite o nome do usuário: ")
        cpf = input("Digite o CPF: ")
        rua = input("Digite a rua: ")
        num = input("Digite o número: ")
        bairro = input("Digite o bairro: ")
        cidade = input("Digite a cidade: ")
        estado = input("Digite o estado: ")
        cep = input("Digite o CEP: ")

        usuario_id = str(uuid.uuid4())

        data_cadastro = datetime.now().strftime("%Y-%m-%d")

        query = (
            f"CREATE (:Usuario {{id: '{usuario_id}', nome_usuario: '{nome_usuario}', cpf: '{cpf}', "
            f"rua: '{rua}', num: '{num}', bairro: '{bairro}', cidade: '{cidade}', estado: '{estado}', cep: '{cep}', "
            f"data_cadastro: '{data_cadastro}'}})"
        )

        connection.query(query)

        print("Usuário criado com sucesso!")
    finally:
        connection.close()

def listar_usuarios(connection):
    try:
        connection.connect()

        query_listar_usuarios = (
            "MATCH (u:Usuario) RETURN u.id AS id, u.nome_usuario AS nome, u.cpf AS cpf, "
            "u.rua AS rua, u.num AS num, u.bairro AS bairro, u.cidade AS cidade, u.estado AS estado, u.cep AS cep"
        )

        usuarios = connection.query(query_listar_usuarios)

        print("Lista de Usuários:")
        for i, usuario in enumerate(usuarios, start=1):
            print(f"{i}. Nome: {usuario['nome']}")

        try:
            index_usuario = int(input("Digite o número do usuário desejado (0 para sair): "))
            if index_usuario == 0:
                return
            usuario_selecionado = usuarios[index_usuario - 1]

            print("\nDetalhes do Usuário:")
            print(f"ID: {usuario_selecionado['id']}")
            print(f"Nome: {usuario_selecionado['nome']}")
            print(f"CPF: {usuario_selecionado['cpf']}")
            print("Endereço:")
            print(f"Rua: {usuario_selecionado['rua']}")
            print(f"Número: {usuario_selecionado['num']}")
            print(f"Bairro: {usuario_selecionado['bairro']}")
            print(f"Cidade: {usuario_selecionado['cidade']}")
            print(f"Estado: {usuario_selecionado['estado']}")
            print(f"CEP: {usuario_selecionado['cep']}")

        except (ValueError, IndexError):
            print("Seleção inválida.")
    finally:
        connection.close()