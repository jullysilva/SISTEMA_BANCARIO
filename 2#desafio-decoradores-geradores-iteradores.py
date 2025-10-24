from datetime import datetime

# =================
# SISTEMA BANCÁRIO
# =================

def menu():
    return """
[0] Novo cliente
[1] Nova conta
[2] Listar contas
[3] Acessar conta
[d] Depositar
[s] Sacar
[e] Extrato
[r] Relatório
[q] Sair
=> """


# ---------------------
# DECORADOR DE LOG
# ---------------------
def log_transacao(func):
    def wrapper(*args, **kwargs):
        tipo = func.__name__.capitalize()
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"\n[LOG] {data_hora} → Transação: {tipo}")
        resultado = func(*args, **kwargs)
        print(f"[LOG] {tipo} concluído.\n")
        return resultado
    return wrapper


# ---------------------
# GERADOR DE RELATÓRIOS
# ---------------------
def gerar_relatorio(transacoes, tipo=None):
    """Gerador que retorna transações uma a uma, opcionalmente filtradas por tipo"""
    for linha in transacoes.split("\n"):
        if not linha.strip():
            continue
        if tipo is None or tipo.lower() in linha.lower():
            yield linha


# ---------------------
# ITERADOR PERSONALIZADO
# ---------------------
class ContaIterador:
    """Iterador que percorre todas as contas"""
    def __init__(self, contas):
        self.contas = contas
        self.indice = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.indice < len(self.contas):
            conta = self.contas[self.indice]
            self.indice += 1
            return {
                "agencia": conta["agencia"],
                "numero_conta": conta["numero_conta"],
                "titular": conta["usuario"]["nome"],
                "saldo": conta["saldo"]
            }
        raise StopIteration


# ---------------------
# FUNÇÕES BANCÁRIAS
# ---------------------
@log_transacao
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato


@log_transacao
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

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
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato, numero_saques


@log_transacao
def exibir_extrato(saldo, /, *, extrato):
    print("\n========== EXTRATO ==========")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"Saldo atual: R$ {saldo:.2f}")
    print("=============================\n")


@log_transacao
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    if any(usuario["cpf"] == cpf for usuario in usuarios):
        print("Já existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    print("Usuário criado com sucesso!")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


@log_transacao
def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        conta = {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario,
            "saldo": 0,
            "extrato": "",
            "numero_saques": 0
        }
        contas.append(conta)
        print(f"Conta criada com sucesso! Agência: {agencia} | Conta: {numero_conta}")
    else:
        print("Usuário não encontrado. Cadastre o usuário primeiro.")


def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return

    print("\n=== LISTA DE CONTAS ===")
    for conta in ContaIterador(contas):  # uso do iterador personalizado
        print(f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {conta['titular']} | Saldo: R$ {conta['saldo']:.2f}")


def acessar_conta(contas):
    cpf = input("Informe o CPF: ")
    numero_conta = int(input("Informe o número da conta: "))

    for conta in contas:
        if conta["usuario"]["cpf"] == cpf and conta["numero_conta"] == numero_conta:
            print(f"Bem-vindo(a), {conta['usuario']['nome']}!")
            return conta

    print("Conta não encontrada ou dados incorretos.")
    return None


# ---------------------
# PROGRAMA PRINCIPAL
# ---------------------
def main():
    LIMITE_SAQUES = 3
    LIMITE_VALOR = 500
    AGENCIA = "0001"

    usuarios = []
    contas = []
    conta_logada = None

    while True:
        opcao = input(menu())

        if opcao == "0":
            criar_usuario(usuarios)

        elif opcao == "1":
            numero_conta = len(contas) + 1
            criar_conta(AGENCIA, numero_conta, usuarios, contas)

        elif opcao == "2":
            listar_contas(contas)

        elif opcao == "3":
            conta_logada = acessar_conta(contas)

        elif opcao == "d":
            if conta_logada:
                valor = float(input("Informe o valor do depósito: "))
                conta_logada["saldo"], conta_logada["extrato"] = depositar(
                    conta_logada["saldo"], valor, conta_logada["extrato"]
                )
            else:
                print("Você precisa acessar uma conta primeiro!")

        elif opcao == "s":
            if conta_logada:
                valor = float(input("Informe o valor do saque: "))
                conta_logada["saldo"], conta_logada["extrato"], conta_logada["numero_saques"] = sacar(
                    saldo=conta_logada["saldo"],
                    valor=valor,
                    extrato=conta_logada["extrato"],
                    limite=LIMITE_VALOR,
                    numero_saques=conta_logada["numero_saques"],
                    limite_saques=LIMITE_SAQUES
                )
            else:
                print("Você precisa acessar uma conta primeiro!")

        elif opcao == "e":
            if conta_logada:
                exibir_extrato(conta_logada["saldo"], extrato=conta_logada["extrato"])
            else:
                print("Você precisa acessar uma conta primeiro!")

        elif opcao == "r":
            if conta_logada:
                tipo = input("Filtrar por tipo (Deposito/Saque ou Enter para todos): ")
                print("\n===== RELATÓRIO DE TRANSAÇÕES =====")
                for transacao in gerar_relatorio(conta_logada["extrato"], tipo):
                    print(transacao)
                print("===================================")
            else:
                print("Você precisa acessar uma conta primeiro!")

        elif opcao == "q":
            print("Saindo do sistema... Até logo!")
            break

        else:
            print("Operação inválida! Tente novamente.")


if __name__ == "__main__":
    main()
