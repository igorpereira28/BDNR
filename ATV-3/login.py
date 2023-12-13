from pymongo import MongoClient
import redis
import time

def importar_usuarios(uri, redis_host, redis_port, redis_password):
    # Conectar ao MongoDB
    cliente_mongo = MongoClient(uri)
    banco_de_dados_mongo = cliente_mongo.get_database("mercadolivre")
    colecao_usuario_mongo = banco_de_dados_mongo.get_collection("usuario")

    # Conectar ao Redis
    cliente_redis = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    # Obter todos os documentos da coleção no MongoDB
    documentos_mongo = colecao_usuario_mongo.find()

    # Iterar sobre os documentos e armazenar no Redis usando o CPF do usuário como chave
    for documento in documentos_mongo:
        id_usuario = str(documento['_id'])
        nome_usuario = documento['nome']
        sobrenome_usuario = documento['sobrenome']
        cpf_usuario = documento['cpf']

        # Armazenar no Redis usando o CPF do usuário como chave
        chave_redis = f"Usuario:CPF:{cpf_usuario}"
        cliente_redis.hmset(chave_redis, {'_id': id_usuario, 'nome': nome_usuario, 'sobrenome': sobrenome_usuario, 'cpf': cpf_usuario})

    # Fechar as conexões
    cliente_mongo.close()
    cliente_redis.close()
    print("Exportação de usuários concluída com sucesso")

def criar_conta_login(uri, redis_host, redis_port, redis_password, chave_usuario_existente, login, senha):
    # Conectar ao Redis
    cliente_redis = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    # Criar conta de login para o usuário existente
    cliente_redis.hmset(chave_usuario_existente, {'login': login, 'senha': senha})

    # Fechar a conexão
    cliente_redis.close()
    print("Conta de login criada com sucesso.")

def listar_e_autenticar_usuarios(redis_host, redis_port, redis_password):
    # Conectar ao Redis
    cliente_redis = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    # Obter todas as chaves no Redis (cada chave representa um usuário)
    chaves_usuarios = cliente_redis.keys("Usuario:CPF:*")

    # Verificar se há usuários cadastrados
    if not chaves_usuarios:
        print("Nenhum usuário cadastrado.")
    else:
        # Imprimir os nomes dos usuários e obter a seleção do usuário
        print("Selecione um usuário:")
        for i, chave_usuario in enumerate(chaves_usuarios, start=1):
            dados_usuario = cliente_redis.hgetall(chave_usuario)
            print(f"{i}. Nome: {dados_usuario['nome']} {dados_usuario['sobrenome']}, CPF: {dados_usuario['cpf']}")

        # Pedir ao usuário para selecionar um usuário pelo ID
        try:
            indice_selecionado = int(input("Digite o número correspondente ao usuário que deseja autenticar: "))
        except ValueError:
            print("Entrada inválida. Digite um número válido.")
            return

        # Verificar se o índice está dentro dos limites
        if 1 <= indice_selecionado <= len(chaves_usuarios):
            # Obter a chave correspondente ao ID selecionado
            chave_usuario_selecionado = chaves_usuarios[indice_selecionado - 1]
            dados_usuario = cliente_redis.hgetall(chave_usuario_selecionado)

            # Mostrar os dados do usuário selecionado
            print(f"\nNome do usuário: {dados_usuario['nome']} {dados_usuario['sobrenome']}")
            print(f"CPF: {dados_usuario['cpf']}")
            
            # Pedir ao usuário para digitar o login e a senha
            login_digitado = input("Digite o login: ")
            senha_digitada = input("Digite a senha: ")

            # Verificar se o login e a senha estão corretos
            if login_digitado == dados_usuario['login'] and senha_digitada == dados_usuario['senha']:
                print("Login e senha corretos. Autenticando...")

                # Simular autenticação com um expire de 10 segundos
                cliente_redis.expire(chave_usuario_selecionado, 60)
                print("Autenticação bem-sucedida. Você está autenticado.")
                
                
                # Quando a chave não existir mais, a sessão expirou
                for i in range(10, 0, -1):
                    print(f"A sessão será encerrada em {i} segundos.", end='\r')
                    time.sleep(1)  # Aguardar 1 segundo antes de imprimir o próximo segundo

                # Quando a chave não existir mais, a sessão expirou
                print("Sessão expirada. Você foi desconectado.")
            else:
                print("Login ou senha inválidos.")
        else:
            print("Índice inválido. Selecione um número válido.")

    # Fechar a conexão
    cliente_redis.close()

def visualizar_usuarios_disponiveis(redis_host, redis_port, redis_password):
    # Conectar ao Redis
    cliente_redis = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    # Obter todas as chaves no Redis (cada chave representa um usuário)
    chaves_usuarios = cliente_redis.keys("Usuario:CPF:*")

    # Verificar se há usuários cadastrados
    if not chaves_usuarios:
        print("Nenhum usuário cadastrado.")
    else:
        # Criar uma lista para armazenar as informações dos usuários
        usuarios = []

        # Iterar sobre as chaves dos usuários
        for chave_usuario in chaves_usuarios:
            dados_usuario = cliente_redis.hgetall(chave_usuario)
            usuarios.append({
                'chave': chave_usuario,
                'dados': dados_usuario
            })

        # Imprimir os nomes dos usuários
        print("Usuários disponíveis:")
        for i, usuario in enumerate(usuarios, start=1):
            dados_usuario = usuario['dados']
            print(f"{i}. Nome: {dados_usuario['nome']} {dados_usuario['sobrenome']}, CPF: {dados_usuario['cpf']}")

    # Fechar a conexão
    cliente_redis.close()

    # Retornar a lista de usuários
    return usuarios


def criar_conta_login_para_usuario_existente(uri, redis_host, redis_port, redis_password, chave_usuario_existente, login, senha):
    # Conectar ao Redis
    cliente_redis = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    # Criar conta de login para o usuário existente
    cliente_redis.hmset(chave_usuario_existente, {'login': login, 'senha': senha})

    # Fechar a conexão
    cliente_redis.close()
    print("Conta de login criada com sucesso.")