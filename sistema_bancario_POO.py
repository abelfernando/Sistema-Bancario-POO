import textwrap
from datetime import datetime
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
    def __init__(self, nome,cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

    def __str__(self):
        return f"""\
            Nome:\t{self.nome}
            CPF:\t{self.cpf}
            Data de Nascimento:\t{self.data_nascimento}
            Endereço:\t{self.endereco}
        """

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

     
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):  
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        
        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True
        
        else:
            print("Operação falhou! O valor informado é inválido.")

        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso!")
            
        else:
            print("Operação falhou! O valor informado é inválido.")
            return False
        
        return True
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico._transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)

        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
    
class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )
    
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)

        if sucesso:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)

        if sucesso:
            conta.historico.adicionar_transacao(self)

def filtrar_usuario(cpf, usuarios):
    """Filtra um usuário pelo CPF."""
    usuarios_filtrados = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def recuperar_conta_usuario(usuario):
    """Recupera as contas bancárias de um usuário."""
    if len( usuario.contas) == 0:
        print("O usuário não possui contas bancárias.")
        return None
    elif len( usuario.contas) > 1:
        print("=" *100)
        print("O usuário possui mais de uma conta. Selecione a conta desejada:")
        for i, conta in enumerate(usuario.contas):
            print(f"[{i + 1}] - Conta número: {conta.numero}")
        conta_escolhida = int(input("Número da conta desejada: "))
        return usuario.contas[conta_escolhida - 1]
    else:
        return usuario.contas[0]

def deposito(usuarios):
    """Realiza um depósito na conta bancária"""

    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("Usuário não encontrado!")
        return

    conta = recuperar_conta_usuario(usuario)
    if not conta:
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    
    usuario.realizar_transacao(conta, transacao)

def saque(usuarios):
    """Realiza um saque na conta bancária."""

    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("Usuário não encontrado!")
        return

    conta = recuperar_conta_usuario(usuario)
    if not conta:
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    usuario.realizar_transacao(conta, transacao)

def exibir_extrato(usuarios):
    """Exibe o extrato da conta bancária."""

    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("Usuário não encontrado!")
        return
    
    conta = recuperar_conta_usuario(usuario)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico._transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['data']} - {transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
    
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


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

    usuario = PessoaFisica(nome = nome, cpf = cpf, data_nascimento = data_nascimento, endereco = endereco)

    usuarios.append(usuario)

    print("\nUsuário criado com sucesso!")

def criar_conta(numero_conta, usuarios, contas):
    """Cria uma nova conta bancária para um usuário existente."""
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        conta = ContaCorrente.nova_conta(cliente=usuario, numero=numero_conta)
        contas.append(conta)
        usuario.contas.append(conta)
        numero_conta += 1
        print("\nConta criada com sucesso!")
        return numero_conta
    
    print("\nUsuário não encontrado, fluxo de criação de conta encerrado!")
    return numero_conta

def listar_contas(contas):
    """Lista todas as contas bancárias criadas no sistema."""
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def listar_usuarios(usuarios):
    """Lista todos os usuários cadastrados no sistema."""
    for usuario in usuarios:
        print("=" * 100)
        print(textwrap.dedent(str(usuario)))


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
    usuarios = []
    contas = []
    numero_conta = 1
    
    
    while True:
    
        opcao = menu()
    
        if opcao == "d":
            deposito(usuarios)
    
        elif opcao == "s":
            saque(usuarios)
    
        elif opcao == "e":
            exibir_extrato(usuarios)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = criar_conta(numero_conta, usuarios, contas)

        elif opcao == "lc":
            listar_contas(contas)
        
        elif opcao == "lu":
            listar_usuarios(usuarios)
    
        elif opcao == "q":
            break
        
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()