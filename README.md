# Desafio: Otimizar Sistema Bancário
Desafio de otimização de sistema bancário do Bootcamp DIO Luizalabs Back-end com Python

## Índice
[Descrição](#descrição)\
[Objetivo Geral](#objetivo-geral)\
[Código pré-existente](#código-pré-existente)\
[Desafio](#desafio)\
[Funções](#funções)

### Descrição
Otimizar o Sistema Bancário previamente desenvolvido com o uso de funções Python. O objetivo é aprimorar a estrutura e a eficiência do sistema, implementando as operações de depósito, saque e extrato em funções específicas. Você terá a chance de refatorar o código existente, dividindo-o em funções reutilizáveis, facilitando a manutenção e o entendimento do sistema como um todo.

### Objetivo Geral
Separar as funções existentes de saque, depósito e extrato em funções. Criar duas novas funções: cadastrar usuário (cliente) e cadastrar conta bancária.

#### Código pré-existente
```
menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
```

### Desafio
Precisamos deixar nosso código mais modularizado, para isso vamos criar funções para as operações existentes: sacar, depositar e visualizar extrato. Além disso, para a versão 2 do nosso sistema precisamos criar duas novas funções: criar usuário (cliente  do banco) e criar conta corrente (vincular com usuário).

### Funções

#### Saque
A função saque deve receber os argumentos apenas por nome (keyword only). 
Sugestão de argumentos: saldo, valor, extrato, limite, numero_saques, limite_saques
Sugestão de retorno: saldo e extrato

#### Depósito
A função depósito deve receber os argumentos apenas por posição (positional only).
Sugestão de argumentos: saldo, valor, extrato
Sugestão de retorno: saldo e extrato

#### Extrato
A função extrato deve receber os argumentos por posição e nome (positional only e keyword only).
Argumentos posicionais: saldo
Argumentos nomeados: extrato

#### Criar usuário (cliente)
O programa deve armazenar os usuários em uma lista, um usuário é composto po: nome, data de nascimento, cpf e endereço. O endereço é uma string com o formato: logradouro, nr0 - bairro - cidade/UF. Deve ser armazenado somente os números do CPF. Não podemos cadastrar 2 usuários com o mesmo CPF.

#### Criar conta corrente
O programa deve armazenar contas em uma lista, uma conta é composta por: agência, número da conta e usuário. O número da conta é sequencial, iniciando em 1. O número da agência é fixo: "0001". O usuário pode ter mais de uma conta, mas uma conta pertence a somente um usuário.

##### Dica
Para vincular um usuário a uma conta, filtre a lista de usuários buscando o número do CPF informado para cada usuário da lista
