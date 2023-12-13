from cassandra.query import BatchStatement
import uuid

def create_vendedor(session):
    print('\nInsira as informações do vendedor')
    nome = input('Nome do vendedor ou da loja: ')
    cpfOuCnpj = input('Seu documento (CPF ou CNPJ): ')

    enderecos = []
    keyEnderecos = 0
    while(keyEnderecos != 'N'):
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
    while(keyTelefones != 'N'):
        telefone = input('DDD + Telefone: ')
        telefones.add(telefone)
        keyTelefones = input('\nDeseja cadastrar mais um telefone? S/N ').upper()

    email = input('Email: ')
    senha = input('Senha: ')

    batch = BatchStatement()
    vendedor_statement = session.prepare("INSERT INTO ecommerce.vendedor(vend_id, vend_nome, vend_telefone, vend_email, vend_senha) VALUES (?, ?, ?, ?, ?)")
    batch.add(vendedor_statement, (cpfOuCnpj, nome, telefones, email, senha))

    endereco_statement = session.prepare("INSERT INTO ecommerce.endereco(usuario_id, end_id, end_cep, end_rua, end_numero, end_bairro, end_cidade, end_estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
    for endereco in enderecos:
        batch.add(endereco_statement, (cpfOuCnpj, endereco["id"], endereco["cep"], endereco["rua"], endereco["numero"], endereco["bairro"], endereco["cidade"], endereco["estado"]))
    
    session.execute(batch)
    print(f'\nVendedor cadastrado!')

    return

def delete_vendedor(session):
    cpfOuCnpj = input('Digite o cpf ou cnpj do vendedor que deseja excluir: ')

    batch = BatchStatement()

    vendedor_statement = session.prepare("DELETE FROM ecommerce.vendedor WHERE vend_id = ?")
    batch.add(vendedor_statement, (cpfOuCnpj,))
    endereco_statement = session.prepare("DELETE FROM ecommerce.endereco WHERE usuario_id = ?")
    batch.add(endereco_statement, (cpfOuCnpj,))
    produtos_statement = session.prepare("DELETE FROM ecommerce.produto WHERE vend_id = ?")
    batch.add(produtos_statement, (cpfOuCnpj,))
    
    session.execute(batch)
    
    print(f'Vendedor deletado!')
    return

def read_vendedor(session):
    cpfOuCnpj = input('Digite o cpf ou cnpj do vendedor que deseja encontrar: ')

    vendedores = session.execute("SELECT * FROM ecommerce.vendedor WHERE vend_id = %s", (cpfOuCnpj,))
    

    enderecos = session.execute("SELECT * FROM ecommerce.endereco WHERE usuario_id = %s", (cpfOuCnpj,))
    produtos = session.execute("SELECT prod_id, prod_nome FROM ecommerce.produto WHERE vend_id = %s", (cpfOuCnpj,))

    if not vendedores:
        print('Não foram encontrados vendedores com essas informações')
    else:
        vendedor = vendedores.one()._asdict()

        print("\nInformações do vendedor:")
        print(f"Documento: {vendedor['vend_id']}")
        print(f"Nome: {vendedor['vend_nome']}")

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
        print(f"Email: {vendedor['vend_email']}")
        print("Telefones:")
        for telefone in vendedor['vend_telefone']:
            print(telefone)


        if produtos:
            print('\nProdutos deste vendedor: ')
            for produto in produtos:
                produto = produto._asdict()
                print(f'Código: {produto["prod_id"]}')
                print(f'Nome: {produto["prod_nome"]}')     
        else:
            print('\nNão há produtos cadastrados nesse vendedor')
    return

def update_vendedor(session):
    cpfOuCnpj = input('Digite o cpf ou cnpj do vendedor que deseja excluir: ')

    vendedores = session.execute("SELECT vend_nome, vend_email, vend_senha, vend_telefone FROM ecommerce.vendedor WHERE vend_id = %s", (cpfOuCnpj,))
    

    if not vendedores:
        print('Não foram encontrados vendedores com esse número de documento')
    else:
        vendedor = vendedores.one()._asdict()
        print(f'Editando informações de {vendedor["vend_nome"]}. Aperte ENTER para pular um campo')
        nomeCompleto = input('Novo nome: ')
        if len(nomeCompleto):
            vendedor["vend_nome"] = nomeCompleto

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
                                        (cpfOuCnpj, endereco["id"], endereco["cep"], endereco["rua"], endereco['numero'], endereco['bairro'], endereco['cidade'], endereco['estado']))
                        print('Endereço adicionado!\n')
                    case '2':
                        enderecos = session.execute("SELECT * FROM ecommerce.endereco WHERE usuario_id = %s", (cpfOuCnpj,))
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
                                session.execute("DELETE FROM ecommerce.endereco WHERE usuario_id = %s AND end_id = %s", [cpfOuCnpj, end_id])
                                print('Endereço removido!\n')
                        else:
                            print('Endereço inválido\n')

        keyUpdateTelefones = input('\nDeseja atualizar os telefones? S/N ').upper()
        if(keyUpdateTelefones == 'S'):
            telefones_atuais = list(vendedor["vend_telefone"])
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
           vendedor["vend_email"] = email

        senha = input('Nova senha: ')
        if len(senha):
            vendedor["vend_senha"] = senha
        
        session.execute("UPDATE ecommerce.vendedor SET vend_nome = %s, vend_email = %s, vend_senha = %s, vend_telefone = %s WHERE vend_id = %s", (vendedor["vend_nome"], vendedor["vend_email"], vendedor["vend_senha"], set(telefones_atuais), cpfOuCnpj))
        print('\nInformações atualizadas com sucesso!')
    
    return