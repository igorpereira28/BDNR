from pymongo import MongoClient
import redis

def importar_produto(uri, redis_host, redis_port, redis_password):
    # Conectar ao MongoDB
    cliente_mongo = MongoClient(uri)
    banco_de_dados_mongo = cliente_mongo.get_database("mercadolivre")
    colecao_produto_mongo = banco_de_dados_mongo.get_collection("produto")

    # Conectar ao Redis
    cliente_redis = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    # Obter todos os documentos da coleção no MongoDB
    documentos_mongo = colecao_produto_mongo.find()

    # Iterar sobre os documentos e armazenar no Redis usando o nome do produto como chave
    for documento in documentos_mongo:
        nome = documento['nome']
        id_produto = str(documento['_id'])
        descricao_produto = documento['descricao']
        # data_cadastro_produto = documento['data_cadastro']

        # Armazenar no Redis usando o nome do produto como chave
        chave_redis = f"Produto:{nome}"
        cliente_redis.hmset(chave_redis, {'_id': id_produto, 'nome': nome, 'descricao': descricao_produto})

    # Fechar as conexões
    cliente_mongo.close()
    cliente_redis.close()
    print("Importação concluída com sucesso")

def read_produto(redis_host, redis_port, redis_password):
    # Conectar ao Redis
    cliente_redis = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    # Obter todas as chaves no Redis (cada chave representa um produto)
    chaves_produtos = cliente_redis.keys("Produto:*")

    # Verificar se há produtos cadastrados
    if not chaves_produtos:
        print("Nenhum produto cadastrado.")
    else:
        # Imprimir os nomes dos produtos e obter a seleção do usuário
        print("Selecione um produto:")
        for i, chave_produto in enumerate(chaves_produtos, start=1):
            nome = cliente_redis.hget(chave_produto, 'nome')
            print(f"{i}. {nome}")

        # Pedir ao usuário para selecionar um produto pelo ID
        try:
            indice_selecionado = int(input("Digite o número correspondente ao produto que deseja visualizar: "))
        except ValueError:
            print("Entrada inválida. Digite um número válido.")
            return

        # Verificar se o índice está dentro dos limites
        if 1 <= indice_selecionado <= len(chaves_produtos):
            # Obter a chave correspondente ao ID selecionado
            chave_produto_selecionado = chaves_produtos[indice_selecionado - 1]
            dados_produto = cliente_redis.hgetall(chave_produto_selecionado)

            # Mostrar os dados do produto selecionado
            print(f"\nNome do produto: {dados_produto['nome']}")
            print(f"Descrição: {dados_produto['descricao']}")
            print("")
        else:
            print("Índice inválido. Selecione um número válido.")

    # Fechar a conexão
    cliente_redis.close()
    

def delete_produto(uri, redis_host, redis_port, redis_password):
    cliente_mongo = MongoClient(uri)
    banco_de_dados_mongo = cliente_mongo.get_database("mercadolivre")
    colecao_produto_mongo = banco_de_dados_mongo.get_collection("produto")
    # Conectar ao Redis
    cliente_redis = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    # Obter todas as chaves no Redis (cada chave representa um produto)
    chaves_produtos = cliente_redis.keys("Produto:*")

    if len (chaves_produtos) == 0:
        print("Nenhum produto cadastrado")
    else:
        # Mostrar os nomes dos produtos e obter a seleção do usuário
        print("Selecione um produto para excluir:")
        for i, chave_produto in enumerate(chaves_produtos, start=1):
            nome = cliente_redis.hget(chave_produto, 'nome')
            print(f"{i}. {nome}")

        # Pedir ao usuário para selecionar um produto pelo índice
        try:
            indice_selecionado = int(input("Digite o número correspondente ao produto que deseja excluir: "))
        except ValueError:
            print("Entrada inválida. Digite um número válido.")
            return
        
        # Verificar se o índice está dentro dos limites
        if 1 <= indice_selecionado <= len(chaves_produtos):
            # Obter a chave correspondente ao índice selecionado
            chave_produto_selecionado = chaves_produtos[indice_selecionado - 1]
            nome_produto_selecionado = cliente_redis.hget(chave_produto_selecionado, 'nome')

            # Deletar o produto selecionado
            cliente_redis.delete(chave_produto_selecionado)

            print(f"Produto '{nome_produto_selecionado}' excluído com sucesso.")
        else:
            print("Índice inválido. Selecione um número válido.")

        # Fechar as conexões
        cliente_mongo.close()
        cliente_redis.close()

def update_produto(uri, redis_host, redis_port, redis_password):
    # Conectar ao MongoDB
    cliente_mongo = MongoClient(uri)
    banco_de_dados_mongo = cliente_mongo.get_database("mercadolivre")
    colecao_produto_mongo = banco_de_dados_mongo.get_collection("produto")

    # Conectar ao Redis
    cliente_redis = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    # Obter todas as chaves no Redis (cada chave representa um produto)
    chaves_produtos = cliente_redis.keys("Produto:*")

    if len (chaves_produtos) == 0:
        print("Nenhum produto cadastrado")
    else:

        # Mostrar os nomes dos produtos e obter a seleção do usuário
        print("Selecione um produto para atualizar:")
        for i, chave_produto in enumerate(chaves_produtos, start=1):
            nome = cliente_redis.hget(chave_produto, 'nome')
            print(f"{i}. {nome}")

        # Pedir ao usuário para selecionar um produto pelo índice
        try:
            indice_selecionado = int(input("Digite o número correspondente ao produto que deseja atualizar: "))
        except ValueError:
            print("Entrada inválida. Digite um número válido.")
            return

        # Verificar se o índice está dentro dos limites
        if 1 <= indice_selecionado <= len(chaves_produtos):
            # Obter a chave correspondente ao índice selecionado
            chave_produto_selecionado = chaves_produtos[indice_selecionado - 1]
            nome_produto_atual = cliente_redis.hget(chave_produto_selecionado, 'nome')

            # Pedir ao usuário para fornecer o novo nome e descrição (ou pressionar Enter para manter)
            novo_nome_produto = input(f"Digite o novo nome para o produto '{nome_produto_atual}' (ou pressione Enter para manter): ")
            nova_descricao_produto = input(f"Digite a nova descrição para o produto '{nome_produto_atual}' (ou pressione Enter para manter): ")

            # Verificar se o usuário deseja manter os valores existentes
            if not novo_nome_produto:
                novo_nome_produto = nome_produto_atual
            if not nova_descricao_produto:
                nova_descricao_produto = cliente_redis.hget(chave_produto_selecionado, 'descricao')

            # Atualizar no MongoDB
            filtro = {'nome': nome_produto_atual}
            atualizacao = {'$set': {'nome': novo_nome_produto, 'descricao': nova_descricao_produto}}
            colecao_produto_mongo.update_one(filtro, atualizacao)
           
            # Atualizar no Redis (renomear a chave e atualizar os dados)
            nova_chave_redis = f"Produto:{novo_nome_produto}"
            cliente_redis.rename(chave_produto_selecionado, nova_chave_redis)

            # Atualizar os dados na nova chave
            cliente_redis.hmset(nova_chave_redis, {'nome': novo_nome_produto, 'descricao': nova_descricao_produto})

            print(f"Produto '{nome_produto_atual}' atualizado com sucesso para '{novo_nome_produto}'.")
        else:
            print("Índice inválido. Selecione um número válido.")

        # Fechar as conexões
        cliente_mongo.close()
        cliente_redis.close()