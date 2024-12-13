from datetime import datetime
import random
def login():
    cpf_requerido = input("Digite seu CPF: ")
    senha_requerida = input("Digite sua senha: ")
    encontrou = False

    for cpf, dados in usuarios.items():
        if cpf_requerido in cpf:
            encontrou = True
            if dados['senha'] == senha_requerida:
                print(f"Bem-vindo(a) {dados['nome']}, login com sucesso!")
                return cpf,True  # Retorna que o login foi bem-sucedido
            else:
                print(f"Senha incorreta para o usuário {cpf}.")
                return False  # Retorna que a senha está incorreta
    if not encontrou:
        print("Usuário não encontrado.")
    return False  # Retorna que o usuário não foi encontrado



def valida_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = ''.join([c for c in cpf if c.isdigit()])

    # Verifica se o CPF tem exatamente 11 dígitos
    if len(cpf) != 11:
        return False

    # Verifica se o CPF é uma sequência repetida de números (ex: 111.111.111-11)
    if cpf == cpf[0] * 11:
        return False

    # Calcula os dois dígitos verificadores
    def calcular_digitos(cpf):
        # Calcula o primeiro dígito verificador
        soma = sum([int(cpf[i]) * (10 - i) for i in range(9)])
        digito1 = 11 - (soma % 11)
        if digito1 >= 10:
            digito1 = 0

        # Calcula o segundo dígito verificador
        soma = sum([int(cpf[i]) * (11 - i) for i in range(10)])
        digito2 = 11 - (soma % 11)
        if digito2 >= 10:
            digito2 = 0

        return f"{digito1}{digito2}"

    # Obtém os dois dígitos verificadores calculados
    digitos_calculados = calcular_digitos(cpf)

    # Compara os dois dígitos calculados com os dois últimos dígitos do CPF
    if cpf[-2:] == digitos_calculados:
        return True
    else:
        return False
    



def valida_data_nascimento(data, idade_minima=18, idade_maxima=120):
    try:
        # Tenta converter a string da data para o formato de data
        data_nascimento = datetime.strptime(data, "%d/%m/%Y")
        
        # Verifica se a data está no futuro
        if data_nascimento > datetime.now():
            return False, "A data de nascimento não pode ser no futuro."
        
        # Calcula a idade com base na data de nascimento
        hoje = datetime.now()
        idade = hoje.year - data_nascimento.year
        if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
            idade -= 1  # Ajusta a idade caso a data de aniversário ainda não tenha ocorrido no ano

        # Verifica se a idade está dentro dos limites estabelecidos
        if idade < idade_minima:
            return False, f"A idade mínima permitida é {idade_minima} anos."
        if idade > idade_maxima:
            return False, f"A idade máxima permitida é {idade_maxima} anos."
        
        return True, f"A data de nascimento {data} é válida. Idade: {idade} anos."
    
    except ValueError:
        # Se a data não puder ser convertida, será uma data inválida
        return False, "Formato de data inválido. Use o formato dd/mm/yyyy."

def menu_interno(nome_cliente):
    
    while True:
        print('---Menu interno---')
        print('1- Consultar saldo')
        print('2- Depositar')
        print('3- Transferir')
        print('4- Sacar')
        print('0-Sair')
        
        menu_escolha = int(input())
        
        if menu_escolha == 1:
            print("Saldo:")
            print(usuarios[nome_cliente]['saldo'])
        elif menu_escolha == 2:
            valor_deposito = float(input("Informe a quantidade do deposito: "))         
            usuarios[nome_cliente]['saldo'] += valor_deposito
            usuarios[nome_cliente]['operacao_deposito'].append(valor_deposito)
            #arrumar para ficar mais legivel
            usuarios[nome_cliente]['data_deposito'].append(datetime.now().date())
            #apenas dias
            print((usuarios[nome_cliente]['data_deposito'][0] - datetime(2024, 11, 1).date()).days)         
            print("Desposito realizado com sucesso")
            #print(usuarios[nome_cliente])
        elif menu_escolha == 3:
            encontrou = False
            agencia_transferencia = input("Informe a agência de destino")
            conta_transferencia = input("Informe a conta de destino")
            if usuarios[nome_cliente]['conta'] != conta_transferencia: 
                valor_transferencia = float(input("Informe o valor da transferência: "))
                if usuarios[nome_cliente]['saldo'] > valor_transferencia:
                    for nome, dados in usuarios.items():
                        if agencia_transferencia in dados['agencia']:
                            if conta_transferencia in dados['conta']:
                                encontrou = True
                                usuarios[nome_cliente]['saldo'] += -valor_transferencia 
                                usuarios[nome_cliente]['operacao_transferencia'].append(-valor_transferencia)
                                usuarios[nome_cliente]['data_transferencia'].append(datetime.now().date())
                                #ele volta ao menu e não ao menu interno
                                print(f'encontru {nome}')
                    if not encontrou:
                        print("Usuário não encontrado. Verifique a agência e conta!")
                    return False  # Retorna que o usuário não foi encontrado
                else:
                    print("Valor insuficiente para transferência!")
            else:
                print("Operação inválida")

            
        elif menu_escolha == 4:
            valor_saque=float(input("Digite o valor para sacar:  "))
            if valor_saque <= usuarios[nome_cliente]['saldo']:
                usuarios[nome_cliente]['saldo'] += -valor_saque
                usuarios[nome_cliente]['operacao_saque'].append(-valor_saque)
                usuarios[nome_cliente]['data_saque'].append(datetime.now().date())
                print("Saque efetuado com sucesso!")
            else:
                print("Valor não disponivel.")

        elif menu_escolha == 0:
            #arrumar aqui
            return "sair"

def menu_conta(nome_cliente):
    while True:
        print("!!!!Bem vindo ao NOOB BANK!!!!")
        print("MENU")
        print("1 - Acessar conta")
        print("2 - Trocar de usuário")
        print("3 - Logout e voltar ao menu inicial")
        print("0 - Sair")
        menu_escolha = int(input())

        if menu_escolha == 1:
            acao = menu_interno(nome_cliente)
            if acao == 'sair':
                print('Saindo do sistema...')
                return 'sair'
                
            
        elif menu_escolha == 2:
            return "trocar"  # Indica que o usuário quer trocar de conta
        elif menu_escolha == 3:
            return "logout"  # Indica que o usuário quer deslogar
        elif menu_escolha == 0:
            print("Saindo do sistema...")
            return "sair"  # Indica que o programa deve encerrar
        else:
            print("Opção inválida! Tente novamente.")


def menu():
    usuario_logado = False
    while True:
        print("----Bem vindo ao NOOB BANK----")
        if usuario_logado == True:
            print(f"Usuário logado: {usuario_logado}")
        else:
            print("MENU")
            print("1 - Login")
            print("2 - Novo cadastro")
            print("3 - Trocar de usuário")
            print("0 - Sair")
        escolha_menu = int(input())

        if escolha_menu == 1:
            usuario_logado = login()
            
            if usuario_logado:
                while True:
                    acao = menu_conta(usuario_logado[0])
                    if acao == "trocar":
                        usuario_logado = False
                        break  # Sai para trocar de usuário
                    elif acao == "logout":
                        usuario_logado = False
                        break  # Sai para o menu inicial
                    elif acao == "sair":
                        return  # Encerra o programa
        elif escolha_menu == 2:
            #ajustar nome completo
            nome = input("Digite seu nome completo: ")
            cpf = input("Digite seu CPF: ")
            # Valida o CPF digitado
            if valida_cpf(cpf):
                print(f"O CPF {cpf} é válido.")
                #melhorar o input, mais claro
                data_nascimento=input("Digite sua data de nascimento: ")
                valido, mensagem = valida_data_nascimento(data_nascimento)
                if valido:
                    print(mensagem)
                    #agencia = input("Informe sua agência: ")
                    agencia_lista= [11111,22222,3333,44444,5555]
                    numero_aleatorio = random.randint(0,4)
                    agencia = str(agencia_lista[numero_aleatorio])
                    print(agencia)
                    #conta = input("Informe sua conta: ")
                    conta = random.sample(range(10),5)
                    conta = "".join(map(str,conta))
                    
                    """
                    for cpf,dados in usuarios.items():
                        while conta == dados['conta']:
                            conta = random.sample(range(10),5)
                            conta = "".join(map(str,conta))
                    """
                    
                        
                    print(conta)
                    senha = input("Digite sua senha: ")
                    usuarios[cpf] = {
                    "nome": nome,
                    "senha": senha,
                    "data_nascimento": data_nascimento,
                    "saldo": 0,
                    "agencia": agencia,
                    "conta": conta,
                    "operacao_deposito": [],
                    "data_deposito": [],
                    "operacao_transferencia": [],
                    "data_transferencia": [],
                    "operacao_saque": [],
                    "data_saque":[],
                
                    }
                    print("Cadastro realizado com sucesso!")

                else:
                    print(mensagem)
                

                
            else:
                print(f"O CPF {cpf} é inválido.")
                

            
        elif escolha_menu == 3:
            print("Por favor, faça login para trocar de usuário.")
        elif escolha_menu == 0:
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida! Tente novamente.")


usuarios = {}



usuarios = {
    "12345678909": {
        "nome": "joão silva",  # CPF válido
        "senha": "senha123",  # Senha válida
        "data_nascimento": "15/08/1990",  # Data de nascimento válida
        "saldo": 500.0,  # Saldo inicial de 500
        "agencia": '1234',
        "conta": '123',
        "operacao_deposito": [],
        "data_deposito": [],
        "operacao_transferir": [],
        "data_transferencia": [],
        "operacao_sacar": [],
        "data_saque":[],
        
    },
    "98765432100": {
        "nome": "Maria Silva da Silva",  # CPF válido
        "senha": "maria2023",  # Senha válida
        "data_nascimento": "20/05/1985",  # Data de nascimento válida
        "saldo": 1200.0,  # Saldo inicial de 1200
        "agencia": '321',
        "conta": '3214',
        "operacao_deposito": [],
        "data_deposito": [],
        "operacao_transferencia": [],
        "data_transferencia": [],
        "operacao_saque": [],
        "data_saque":[],
        
    }
}

menu()

