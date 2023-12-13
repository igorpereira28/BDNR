import uuid
def create_produto(session):
    print('\nInsira as informações do produto')

    vendedores = session.execute("SELECT vend_id from ecommerce.vendedor")
    vendedores = list(vendedores)

    nome = input('Nome: ')
    descricao = input('Descrição: ')

    validacaoValor = 0
    while(validacaoValor != 1):
        valor = input('Valor: ')
        try:
            valor = float(valor)
            validacaoValor = 1
        except ValueError:
            print('Insira um valor válido')
    
    validacaoQuantidade = 0
    while(validacaoQuantidade != 1):
        quantidade = input('Quantidade disponível: ')
        if(quantidade.isnumeric()):
            quantidade = int(quantidade)
            validacaoQuantidade = 1
        else:
            print('Insira um valor válido')
    
    verificacaoVendedor = 0
    while(verificacaoVendedor != 1):
        cpfOuCnpj = input('\nDigite o cpf ou cnpj do vendedor: ')
        
        if any(cpfOuCnpj == row.vend_id for row in vendedores):
            verificacaoVendedor = 1
        else:
            print('Não foram encontrados vendedores com essas informações')

    session.execute("INSERT INTO ecommerce.produto(vend_id, prod_id, prod_nome, prod_descricao, prod_valor, prod_quantidade) VALUES (%s, %s, %s, %s, %s, %s)",
                    (cpfOuCnpj, uuid.uuid4(), nome, descricao, valor, quantidade))
    print(f'\nProduto cadastrado!')

    return

def delete_produto(session):
    cpfOuCnpj = input('\nDigite o CPF ou CNPJ do vendedor do produto que deseja excluir: ')
    idProduto = input('Digite o código do produto que deseja excluir: ')
    try:
        idProduto = uuid.UUID(idProduto)
    except ValueError:
        print('Formato inválido de código de produto')

    session.execute("DELETE FROM ecommerce.produto WHERE vend_id = %s AND prod_id = %s", (cpfOuCnpj, idProduto))

    print(f'Deletando o produto de id ${idProduto}')
    return

def read_produto(session):
    idProduto = input('\nDigite o código do produto que deseja encontrar: ')
    try:
        idProduto = uuid.UUID(idProduto)
    except ValueError:
        print('Formato inválido de código de produto')

    produtos = session.execute("SELECT * FROM ecommerce.produto WHERE prod_id = %s ALLOW FILTERING", (idProduto,))
    

    if not produtos:
        print('Não foram encontrados produtos com esse código.')
    else:
        produto = produtos.one()._asdict()

        print("\nInformações do produto:")
        print(f'Código: {produto["prod_id"]}')
        print(f'Nome: {produto["prod_nome"]}')
        print(f'Descrição: {produto["prod_descricao"]}')
        print(f'Valor: {produto["prod_valor"]}')
        print(f'Quantidade disponível: {produto["prod_quantidade"]}')
    
    return

def update_produto(session):
    idProduto = input('\nDigite o código do produto que deseja atualizar: ')
    try:
        idProduto = uuid.UUID(idProduto)
    except ValueError:
        print('Formato inválido de código de produto')

    produtos = session.execute("SELECT * FROM ecommerce.produto WHERE prod_id = %s ALLOW FILTERING", (idProduto,))
    

    if not produtos:
        print('Não foram encontrados produtos com esse código')
    else:
        produto = produtos.one()._asdict()

        print(f'Editando informações do produto {produto["prod_nome"]}. Aperte ENTER para pular um campo')
        nome = input('Nome: ')
        if len(nome):
            produto["prod_nome"] = nome
        
        descricao = input('Descrição: ')
        if len(descricao):
            produto["prod_descricao"] = descricao
        
        valor = input('Valor: ')
        if len(valor):
            validacaoValor = 0
            while(validacaoValor != 1):
                try:
                    produto["prod_valor"] = float(valor)
                    validacaoValor = 1
                except ValueError:
                    valor = input('Insira um valor válido: ')

        quantidade = input('Quantidade: ')
        if len(quantidade):
            validacaoQuantidade = 0
            while(validacaoQuantidade != 1):
                if(quantidade.isnumeric()):
                    produto["prod_quantidade"] = int(quantidade)
                    validacaoQuantidade = 1
                else:
                    quantidade = input('Insira uma quantidade válida: ')

        try:
            session.execute("UPDATE ecommerce.produto SET prod_nome = %s, prod_descricao = %s, prod_valor = %s, prod_quantidade = %s WHERE vend_id = %s AND prod_id = %s",
                            (produto["prod_nome"], produto["prod_descricao"], produto["prod_valor"], produto["prod_quantidade"], produto["vend_id"], idProduto))
            print('\nInformações atualizadas com sucesso!')
        except:
            print('Ocorreu algum erro...')
        
    return