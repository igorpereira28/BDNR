from cassandra.query import BatchStatement
from datetime import datetime
import uuid

def create_usuario(session):
    print('\nInsira as informações do usuário')
    cpf = input('CPF: ')
    nomeCompleto = input('Nome completo: ')

    enderecos = []
    keyEnderecos = 0
    while keyEnderecos != 'N':
        print('\nDigite seu endereço: ')
        cep = input('CEP: ')
        rua = input('Rua: ')
        numero = input('Número: ')
        bairro = input('Bairro: ')
        cidade = input('Cidade: ')
        estado = input('Estado: ')

        endereco = {
            "id": uuid.uuid4(),
            "cep": cep,
            "rua": rua,
            "numero": numero,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado
        }

        enderecos.append(endereco)
        keyEnderecos = input('\nDeseja inserir mais um endereço? S/N ').upper()

    telefones = set()
    keyTelefones = 0
    while keyTelefones != 'N':
        telefone = input('DDD + Telefone: ')
        telefones.add(telefone)
        keyTelefones = input('\nDeseja cadastrar mais um telefone? S/N ').upper()

    email = input('Email: ')
    senha = input('Senha: ')

    batch = BatchStatement()
    usuario_statement = session.prepare("INSERT INTO ecommerce.usuario(us_id, us_email, us_nome, us_senha, us_telefone) VALUES (?, ?, ?, ?, ?)")
    batch.add(usuario_statement, (cpf, email, nomeCompleto, senha, telefones))
    
    endereco_statement = session.prepare("INSERT INTO ecommerce.endereco(usuario_id, end_id, end_cep, end_rua, end_numero, end_bairro, end_cidade, end_estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
    for endereco in enderecos:
        batch.add(endereco_statement, (cpf, endereco["id"], endereco["cep"], endereco["rua"], endereco["numero"], endereco["bairro"], endereco["cidade"], endereco["estado"]))

    session.execute(batch)                 

    print(f'\nUsuário cadastrado!')
    return

def delete_usuario(session):
    cpf = input('\nDigite o cpf do usuário que deseja excluir: ')

    batch = BatchStatement()

    usuario_statement = session.prepare("DELETE FROM ecommerce.usuario WHERE us_id = ?")
    batch.add(usuario_statement, (cpf,))
    endereco_statement = session.prepare("DELETE FROM ecommerce.endereco WHERE usuario_id = ?")
    batch.add(endereco_statement, (cpf,))
    favoritos_statement = session.prepare("DELETE FROM ecommerce.favoritos WHERE us_id = ?")
    batch.add(favoritos_statement, (cpf,))
    
    session.execute(batch)
    print(f'Usuário deletado!')
    return

def read_usuario(session):
    cpf = input('\nDigite o cpf do usuário que deseja encontrar: ')

    usuarios = session.execute("SELECT * FROM ecommerce.usuario WHERE us_id = %s", (cpf,))
    enderecos = session.execute("SELECT * FROM ecommerce.endereco WHERE usuario_id = %s", (cpf,))
    favoritos = session.execute("SELECT * FROM ecommerce.favoritos WHERE us_id = %s", (cpf,))
    compras = session.execute("SELECT * FROM ecommerce.compras WHERE us_id = %s", (cpf,))
    

    if not usuarios:
        print('Não foram encontrados usuários com esse CPF')
    else:
        usuario = usuarios.one()._asdict()
        
        print("\nInformações do usuário:")
        print(f"CPF: {usuario['us_id']}")
        print(f"Nome: {usuario['us_nome']}")

        print("Endereços:")
        for endereco in enderecos:
            endereco = endereco._asdict()
            print(f"\nCEP: {endereco['end_cep']}")
            print(f"Rua: {endereco['end_rua']}")
            print(f"Número: {endereco['end_numero']}")
            print(f"Bairro: {endereco['end_bairro']}")
            print(f"Cidade: {endereco['end_cidade']}")
            print(f"Estado: {endereco['end_estado']}")

        print("\nContatos:")
        print(f"Email: {usuario['us_email']}")
        print("Telefones:")
        for telefone in usuario["us_telefone"]:
            print(telefone)
    
    return

def update_usuario(session):
    cpf = input('\nDigite o cpf do usuário que deseja atualizar: ')

    usuarios = session.execute("SELECT us_nome, us_email, us_senha, us_telefone FROM ecommerce.usuario WHERE us_id = %s", (cpf,))
    

    if not usuarios:
        print('Não foram encontrados usuários com esse CPF')
    else:
        usuario = usuarios.one()._asdict()

        print(f'Editando informações de {usuario["us_nome"]}. Aperte ENTER para pular um campo')
        nomeCompleto = input('Novo nome: ')
        if len(nomeCompleto):
            usuario["us_nome"] = nomeCompleto

        keyUpdateEnderecos = input('\nDeseja atualizar os endereços? S/N ').upper()
        if(keyUpdateEnderecos == 'S'):
            
            keyOpcaoEnderecos = 0
            while(keyOpcaoEnderecos != 'C'):
                print('1 - Adicionar um endereço')
                print('2 - Remover um endereço existente')
                keyOpcaoEnderecos = input('Escolha uma opção: (C para cancelar) ').upper()

                match keyOpcaoEnderecos:
                    case '1':
                        endereco = {
                            "id": uuid.uuid4(),
                            "cep": input('CEP: '),
                            "rua": input('Rua: '),
                            "numero": input('Numero: '),
                            "bairro": input('Bairro: '),
                            "cidade": input('Cidade: '),
                            "estado": input('Estado: ')
                        }
                        
                        session.execute("INSERT INTO ecommerce.endereco(usuario_id, end_id, end_cep, end_rua, end_numero, end_bairro, end_cidade, end_estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                        (cpf, endereco["id"], endereco["cep"], endereco["rua"], endereco['numero'], endereco['bairro'], endereco['cidade'], endereco['estado']))
                        
                        print('Endereço adicionado!\n')
                    case '2':
                        enderecos = session.execute("SELECT * FROM ecommerce.endereco WHERE usuario_id = %s", (cpf,))
                        enderecos = list(enderecos)

                        contadorEndereco = 1
                        for endereco in enderecos:
                            endereco = endereco._asdict()
                            print(f'\nEndereço {contadorEndereco}')
                            print(f"CEP: {endereco['end_cep']}")
                            print(f"Rua: {endereco['end_rua']}")
                            print(f"Número: {endereco['end_numero']}")
                            print(f"Bairro: {endereco['end_bairro']}")
                            print(f"Cidade: {endereco['end_cidade']}")
                            print(f"Estado: {endereco['end_estado']}")

                            contadorEndereco+=1
                        
                        enderecoEscolhido = input('Escolha o endereço que você deseja remover: ')
                        if enderecoEscolhido.isdigit():
                            indiceEnderecoEscolhido = int(enderecoEscolhido)
                            if indiceEnderecoEscolhido > contadorEndereco:
                                print('Endereço inválido\n')
                            else:
                                enderecoEscolhido = enderecos[indiceEnderecoEscolhido - 1]._asdict()
                                end_id = enderecoEscolhido["end_id"]
                                session.execute("DELETE FROM ecommerce.endereco WHERE usuario_id = %s AND end_id = %s", [cpf, end_id])
                                print('Endereço removido!\n')
                        else:
                            print('Endereço inválido\n')

        telefones_atuais = list(usuario["us_telefone"])
        keyUpdateTelefones = input('\nDeseja atualizar os telefones? S/N ').upper()
        if(keyUpdateTelefones == 'S'):
            keyOpcaoTelefones = 0
            while(keyOpcaoTelefones != 'C'):
                print('1 - Adicionar um telefone')
                print('2 - Remover um telefone existente')
                keyOpcaoTelefones = input('Escolha uma opção: (C para cancelar) ').upper()

                match keyOpcaoTelefones:
                    case '1':
                        novoTelefone = input('Digite o novo telefone (DDD + Número): ')
                        if len(novoTelefone):
                            telefones_atuais.append(novoTelefone)
                        print('Telefone adicionado!')
                    case '2':
                        contadorTelefones = 1
                        for telefone in telefones_atuais:
                            print(f'Telefone {contadorTelefones}')
                            print(telefone)

                            contadorTelefones+=1

                        telefoneEscolhido = input('Escolha o telefone que você deseja remover: ')
                        if telefoneEscolhido.isdigit():
                            telefoneEscolhido = int(telefoneEscolhido)
                            if telefoneEscolhido > contadorTelefones:
                                print('Telefone inválido\n')
                            else:
                                telefones_atuais.pop(telefoneEscolhido - 1)
                                print('Telefone removido!\n')
                        else:
                            print('Telefone inválido\n')

        email = input('Novo email: ')
        if len(email):
            usuario["us_email"] = email

        senha = input('Nova senha: ')
        if len(senha):
            usuario["us_senha"] = senha

        keyUpdateFavoritos = input('\nDeseja atualizar os favoritos? S/N ').upper()
        if(keyUpdateFavoritos == 'S'):
            keyOpcaoFavoritos = 0
            while(keyOpcaoFavoritos != 'C'):
                print('1 - Adicionar um favorito')
                print('2 - Remover um item favorito')
                keyOpcaoFavoritos = input('Escolha uma opção: (C para cancelar) ').upper()
                match keyOpcaoFavoritos:
                    case '1':
                        produtos = session.execute('SELECT prod_id, prod_nome, prod_descricao, prod_valor FROM ecommerce.produto')
                        produtos = list(produtos)
                        if not produtos:
                            print('Ainda não há produtos cadastrados')
                        else:
                            for produto in produtos:
                                produto = produto._asdict()
                                print(f'\nCódigo: {produto["prod_id"]}')
                                print(f'Nome: {produto["prod_nome"]}')
                                

                            idProdutoEscolhido = input('Digite o código do produto escolhido: ')
                            try:
                                idProdutoEscolhido = uuid.UUID(idProdutoEscolhido)
                                produtoEscolhido = next((produto for produto in produtos if produto._asdict()["prod_id"] == idProdutoEscolhido), None)
                                produtoEscolhido = produtoEscolhido._asdict()

                                session.execute("INSERT INTO ecommerce.favoritos(us_id, fav_id, prod_id, fav_nome, fav_descricao, fav_valor) VALUES (%s, %s, %s, %s, %s, %s)",
                                                (cpf, uuid.uuid4(), produtoEscolhido["prod_id"], produtoEscolhido["prod_nome"], produtoEscolhido["prod_descricao"], produtoEscolhido["prod_valor"]))
                                print('Favorito adicionado!')
                            except:
                                print("Código inválido")
  
                    case '2':
                        favoritos = session.execute("SELECT * FROM ecommerce.favoritos WHERE us_id = %s", (cpf,))
                        favoritos = list(favoritos)

                        if not favoritos:
                            print('Não há itens nos favoritos para remover')
                        else:
                            for favorito in favoritos:
                                favorito = favorito._asdict()
                                print(f'\nCódigo: {favorito["fav_id"]}')
                                print(f'Nome: {favorito["fav_nome"]}')
                                print(f'Descrição: {favorito["fav_descricao"]}')
                                print(f'Valor: {favorito["fav_valor"]}')
                            
                            idFavoritoEscolhido = input('\nDigite o código do favorito que deseja remover: ')
                            try:
                                idFavoritoEscolhido = uuid.UUID(idFavoritoEscolhido)
                                favoritoEscolhido = next((favorito for favorito in favoritos if favorito._asdict()["fav_id"] == idFavoritoEscolhido), None)
                                favoritoEscolhido = favoritoEscolhido._asdict()

                                session.execute("DELETE FROM ecommerce.favoritos WHERE us_id = %s AND fav_id = %s", (cpf, favoritoEscolhido["fav_id"]))
                                print('Favorito removido!')
                            except:
                                print('Código inválido')
                            

        session.execute("UPDATE ecommerce.usuario SET us_nome = %s, us_email = %s, us_senha = %s, us_telefone = %s WHERE us_id = %s", (usuario["us_nome"], usuario["us_email"], usuario["us_senha"], set(telefones_atuais), cpf))
        print('\nInformações atualizadas com sucesso!')

    return