import redis
from pymongo import MongoClient
def importar_vendedor(uri, redis_host, redis_port, redis_password):
    # Conectar ao MongoDB
    cliente_mongo = MongoClient(uri)
    banco_de_dados_mongo = cliente_mongo.get_database("mercadolivre")
    colecao_produto_mongo = banco_de_dados_mongo.get_collection("vendedor")

    # Conectar ao Redis
    cliente_redis = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    # Obter todos os documentos da coleção no MongoDB
    documentos_mongo = colecao_produto_mongo.find()

    # Iterar sobre os documentos e armazenar no Redis usando o nome do produto como chave
    for documento in documentos_mongo:
        nome = documento['nome']
        id_vendedor = str(documento['_id'])
        sobrenome = documento['sobrenome']
        cpf = documento['cpf']

        # Armazenar no Redis usando o nome do produto como chave
        chave_redis = f"Vendedor:{nome}"
        cliente_redis.hmset(chave_redis, {'_id': id_vendedor, 'nome': nome, 'sobrenome': sobrenome, 'cpf': cpf})

    # Fechar as conexões
    cliente_mongo.close()
    cliente_redis.close()
    print("Importação concluída com sucesso")

def read_vendedor(redis_host, redis_port, redis_password):
    # Conectar ao Redis
    cliente_redis = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    # Obter todas as chaves no Redis (cada chave representa um vendedor)
    chaves_vendedores = cliente_redis.keys("Vendedor:*")

    # Verificar se há vendedores cadastrados
    if len (chaves_vendedores) == 0:
        print("Nenhum vendedor cadastrado.")
    else:
        # Imprimir os nomes dos vendedores e obter a seleção do usuário
        print("Selecione um vendedor:")
        for i, chave_vendedor in enumerate(chaves_vendedores, start=1):
            nome = cliente_redis.hget(chave_vendedor, 'nome')
            print(f"{i}. {nome}")

        # Pedir ao usuário para selecionar um vendedor pelo ID
        try:
            indice_selecionado = int(input("Digite o número correspondente ao vendedor que deseja visualizar: "))
        except ValueError:
            print("Entrada inválida. Digite um número válido.")
            return

        # Verificar se o índice está dentro dos limites
        if 1 <= indice_selecionado <= len(chaves_vendedores):
            # Obter a chave correspondente ao ID selecionado
            chave_vendedor_selecionado = chaves_vendedores[indice_selecionado - 1]
            dados_vendedor = cliente_redis.hgetall(chave_vendedor_selecionado)

            # Mostrar os dados do vendedor selecionado
            print(f"\nNome do vendedor: {dados_vendedor['nome']}")
            # print(f"Data de cadastro: {dados_vendedor['data_cadastro']}")

    # Fechar a conexão
    cliente_redis.close()

def update_vendedor(uri, redis_host, redis_port, redis_password):
    # Conectar ao Redis
    cliente_redis = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    # Conectar ao MongoDB
    cliente_mongo = MongoClient(uri)
    banco_de_dados_mongo = cliente_mongo.get_database("mercadolivre")
    colecao_vendedor_mongo = banco_de_dados_mongo.get_collection("vendedor")

    # Obter todas as chaves no Redis (cada chave representa um vendedor)
    chaves_vendedores = cliente_redis.keys("Vendedor:*")

    if len (chaves_vendedores) == 0:
        print("Nenhum vendedor cadastrado.")
    else:
        # Mostrar os nomes dos vendedores e obter a seleção do usuário
        print("Selecione um vendedor para editar:")
        for i, chave_vendedor in enumerate(chaves_vendedores, start=1):
            nome = cliente_redis.hget(chave_vendedor, 'nome')
            print(f"{i}. {nome}")

        # Pedir ao usuário para selecionar um vendedor pelo índice
        try:
            indice_selecionado = int(input("Digite o número correspondente ao vendedor que deseja editar: "))
        except ValueError:
            print("Entrada inválida. Digite um número válido.")
            return

        # Verificar se o índice está dentro dos limites
        if 1 <= indice_selecionado <= len(chaves_vendedores):
            # Obter a chave correspondente ao índice selecionado
            chave_vendedor_selecionado = chaves_vendedores[indice_selecionado - 1]
            dados_vendedor = cliente_redis.hgetall(chave_vendedor_selecionado)

            # Mostrar os dados do vendedor selecionado
            print(f"\nNome do vendedor: {dados_vendedor['nome']}")

            # Opção de editar o nome do vendedor
            novo_nome_vendedor = input(f"Digite o novo nome para o vendedor '{dados_vendedor['nome']}' (ou pressione Enter para manter): ")

            # Verificar se o usuário deseja manter o valor existente
            if not novo_nome_vendedor:
                novo_nome_vendedor = dados_vendedor['nome']

            # Atualizar a chave do vendedor no Redis
            nova_chave_redis = f"vendedor:{novo_nome_vendedor}"
            cliente_redis.rename(chave_vendedor_selecionado, nova_chave_redis)

            # Atualizar o nome do vendedor no Redis
            cliente_redis.hset(nova_chave_redis, 'nome', novo_nome_vendedor)

            # Atualizar o nome do vendedor no MongoDB
            filtro = {'nome': dados_vendedor['nome']}
            atualizacao = {'$set': {'nome': novo_nome_vendedor}}
            colecao_vendedor_mongo.update_one(filtro, atualizacao) 

        else:
            print("Índice inválido. Selecione um número válido.")

        # Fechar as conexões
        cliente_redis.close()
        cliente_mongo.close()

def delete_vendedor(redis_host, redis_port, redis_password):
    # Conectar ao Redis
    cliente_redis = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    # Obter todas as chaves no Redis (cada chave representa um vendedor)
    chaves_vendedores = cliente_redis.keys("Vendedor:*")

    if len (chaves_vendedores) == 0:
        print("Nenhum vendedor cadastrado.")
    else:
        # Mostrar os nomes dos vendedores e obter a seleção do usuário
        print("Selecione um vendedor para deletar:")
        for i, chave_vendedor in enumerate(chaves_vendedores, start=1):
            nome = cliente_redis.hget(chave_vendedor, 'nome')
            print(f"{i}. {nome}")

        # Pedir ao usuário para selecionar um vendedor pelo índice
        try:
            indice_selecionado = int(input("Digite o número correspondente ao vendedor que deseja deletar: "))
        except ValueError:
            print("Entrada inválida. Digite um número válido.")
            return

        # Verificar se o índice está dentro dos limites
        if 1 <= indice_selecionado <= len(chaves_vendedores):
            # Obter a chave correspondente ao índice selecionado
            chave_vendedor_selecionado = chaves_vendedores[indice_selecionado - 1]

            # Obter o nome do vendedor
            nome_vendedor_selecionado = cliente_redis.hget(chave_vendedor_selecionado, 'nome')

            # Deletar o vendedor no Redis
            cliente_redis.delete(chave_vendedor_selecionado)

            print(f"Vendedor '{nome_vendedor_selecionado}' deletado com sucesso do Redis.")
        else:
            print("Índice inválido. Selecione um número válido.")

    # Fechar a conexão
    cliente_redis.close()