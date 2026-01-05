import textwrap
from abc import ABC, abstractmethod

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome,cpf, data_nascimento):
        super().__init__(endereco=None)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

def deposito(saldo, valor, extrato, /):
    """Realiza um depósito na conta bancária.
    Parâmetros apenas por posição: (saldo, valor, extrato)"""

    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        
    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato
    

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """Realiza um saque na conta bancária.
    Parâmetros apenas por nome: (saldo, valor, extrato, limite, numero_saques, limite_saques)"""

    if valor > limite + saldo:
        print("Operação falhou! Você não tem saldo suficiente e o valor do saque excede o limite.")

    elif numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
        
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\tR$ {valor:.2f}\n"
        numero_saques += 1
    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    """Exibe o extrato da conta bancária.
    Parâmetros por posição ou por nome: (saldo, extrato)"""

    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\tR$ {saldo:.2f}")
    print("==========================================")

def filtrar_usuario(cpf, usuarios):
    """Filtra um usuário pelo CPF."""
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_usuario(usuarios):
    """Cria um novo usuário no sistema bancário."""
    cpf = input("CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe usuário com esse CPF!")
        return
    
    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, número - bairro - cidade/UF): ")
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("\nUsuário criado com sucesso!")

def criar_conta(AGENCIA, numero_conta, usuarios, contas):
    """Cria uma nova conta bancária para um usuário existente."""
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        contas.append({"agencia": AGENCIA, "numero_conta": numero_conta, "usuario": usuario})
        numero_conta += 1
        print("\nConta criada com sucesso!")
        return numero_conta
    
    print("\nUsuário não encontrado, fluxo de criação de conta encerrado!")
    return numero_conta

def listar_contas(contas):
    """Lista todas as contas bancárias criadas no sistema."""
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def listar_usuarios(usuarios):
    """Lista todos os usuários cadastrados no sistema."""
    for usuario in usuarios:
        linha = f"""\
            Nome:\t{usuario['nome']}
            CPF:\t{usuario['cpf']}
            Data de Nascimento:\t{usuario['data_nascimento']}
            Endereço:\t{usuario['endereco']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def menu():
    """Exibe o menu de opções do sistema bancário."""
    menu = """
    
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nu]\tNovo Usuário
    [lu]\tListar Usuários
    [nc]\tNova Conta
    [lc]\tListar Contas
    [q]\tSair
    
    => """
    return input(textwrap.dedent(menu))


def main():
    """Função principal do sistema bancário."""
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    numero_conta = 1
    
    
    while True:
    
        opcao = menu()
    
        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
    
            saldo, extrato = deposito(saldo, valor, extrato)
    
        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
    
            saldo, extrato, numero_saques = saque(saldo=saldo, valor=valor, extrato=extrato, limite=limite,
                                                numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)
    
        elif opcao == "e":
            exibir_extrato(saldo, extrato = extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = criar_conta(AGENCIA, numero_conta, usuarios, contas)

        elif opcao == "lc":
            listar_contas(contas)
        
        elif opcao == "lu":
            listar_usuarios(usuarios)
    
        elif opcao == "q":
            break
        
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()