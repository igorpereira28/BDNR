import uuid
def create_compra(session):
    cpf = input('Digite o cpf do usuário realizando a compra: ')
    
    usuarios = session.execute("SELECT us_nome FROM ecommerce.usuario WHERE us_id = %s", (cpf,))
    

    if not usuarios:
        print('Usuário não encontrado')
    else:
        usuario = usuarios.one()._asdict()
        produtos = session.execute("SELECT vend_id, prod_id, prod_nome, prod_descricao, prod_valor, prod_quantidade FROM ecommerce.produto")

        for produto in produtos:
            produto = produto._asdict()
            print('\nProdutos encontrados:')
            print(f'\nCódigo: {produto["prod_id"]}')
            print(f'Nome: {produto["prod_nome"]}')
            print(f'Valor: {produto["prod_valor"]}')
            print(f'Quantidade: {produto["prod_quantidade"]}')
            

            verificacaoCodigoProduto = 0
            produtoEscolhido = {}
            while(verificacaoCodigoProduto != 1):
                idProdutoEscolhido = input('Digite o código do produto que deseja comprar: ')
                try:
                    idProdutoEscolhido = uuid.UUID(idProdutoEscolhido)
                    produtoEscolhido = next((produto for produto in produtos if produto._asdict()["prod_id"] == idProdutoEscolhido), None)
                    if(produtoEscolhido):
                        produtoEscolhido = produtoEscolhido._asdict()
                        verificacaoCodigoProduto = 1
                    else:
                        print('Código inválido')
                except:
                    print("Código inválido")


            verificacaoQuantidadeProduto = 0
            quantidadeDisponivel = produtoEscolhido["prod_quantidade"]
            while(verificacaoQuantidadeProduto != 1):
                print(f'\nQuantidade disponível: {quantidadeDisponivel}')
                quantidadeEscolhida = input('Quantas unidades deseja comprar? ')

                if(quantidadeEscolhida.isnumeric()):
                    quantidadeEscolhida = int(quantidadeEscolhida)
                    if(quantidadeEscolhida > quantidadeDisponivel):
                        print('Quantidade indisponível')
                    else:
                        verificacaoQuantidadeProduto = 1
                else:
                    print('Digite uma quantidade válida.')

            valorCompra = produtoEscolhido["prod_valor"] * quantidadeEscolhida
            print(f'\nCompra no nome de {usuario["us_nome"]}')
            print(f'Produto: {produtoEscolhido["prod_nome"]}')
            print(f'Quantidade: {quantidadeEscolhida}')
            print(f'Valor: {valorCompra}')

            confirmarCompra = input('\nConfirmar compra? S/N ').upper()
            if(confirmarCompra == 'S'):
                dataAtual = datetime.now()
                
                session.execute("""INSERT INTO ecommerce.compras(us_id, comp_id, comp_data, comp_prod_nome, comp_prod_descricao, comp_valor, comp_prod_quantidade, prod_id)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",  
                                (cpf, uuid.uuid4(), dataAtual, produtoEscolhido["prod_nome"], produtoEscolhido["prod_descricao"], valorCompra, quantidadeEscolhida, produtoEscolhido["prod_id"]))

                quantidadeAtual = quantidadeDisponivel - quantidadeEscolhida
                session.execute("UPDATE ecommerce.produto SET prod_quantidade = %s WHERE vend_id = %s AND prod_id = %s",
                                (quantidadeAtual, produtoEscolhido["vend_id"], produtoEscolhido["prod_id"]))

                print('Compra realizada com sucesso! ')

            elif(confirmarCompra == 'N'):
                print('Compra cancelada.')

    return

def delete_compra(session):
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