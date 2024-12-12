from datetime import datetime

def login():
    cpf_requerido = input("Digite seu CPF: ")
    senha_requerida = input("Digite sua senha: ")
    encontrou = False

    for nome, dados in usuarios.items():
        if cpf_requerido in dados['cpf']:
            encontrou = True
            if dados['senha'] == senha_requerida:
                print(f"Bem-vindo(a) {nome}, login com sucesso!")
                return True  # Retorna que o login foi bem-sucedido
            else:
                print(f"Senha incorreta para o usuário {nome}.")
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


def menu_conta():
    while True:
        print("!!!!Bem vindo ao NOOB BANK!!!!")
        print("MENU")
        print("1 - Acessar conta")
        print("2 - Trocar de usuário")
        print("3 - Logout e voltar ao menu inicial")
        print("0 - Sair")
        menu_escolha = int(input())

        if menu_escolha == 1:
            print("Opções da conta não implementadas.")
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
        print(f"Usuário logado: {usuario_logado}")
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
                    acao = menu_conta()
                    if acao == "trocar":
                        usuario_logado = False
                        break  # Sai para trocar de usuário
                    elif acao == "logout":
                        usuario_logado = False
                        break  # Sai para o menu inicial
                    elif acao == "sair":
                        return  # Encerra o programa
        elif escolha_menu == 2:
            nome = input("Digite seu nome completo: ")
            cpf = input("Digite seu CPF: ")
            # Valida o CPF digitado
            if valida_cpf(cpf):
                print(f"O CPF {cpf} é válido.")
            else:
                print(f"O CPF {cpf} é inválido.")

            senha = input("Digite sua senha: ")
    
            data_nascimento=input("Digite sua data de nascimento: ")
            valido, mensagem = valida_data_nascimento(data_nascimento)
            print(valido,mensagem)
           
            
            usuarios[nome] = {
                "cpf": cpf,
                "senha": senha,
                "data_nascimento": data_nascimento,
                
            }
            print("Cadastro realizado com sucesso!")
        elif escolha_menu == 3:
            print("Por favor, faça login para trocar de usuário.")
        elif escolha_menu == 0:
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida! Tente novamente.")


usuarios = {}
menu()


