import os

VALID_DOMINIOS = [
    "gmail.com",
    "hotmail.com",
    "outlook.com",
    "yahoo.com.br",
    "uol.com",
    "ig.com.br",
    "terra.com.br",
    "bor.com.br",
    "icloud.com",
    "cesar.school",
]


def limpar_tela():
    os.system("cls")


def validar_email(email):
    email = email.strip().lower()
    if email.count("@") != 1:
        return False
    local, dominio = email.split("@", 1)
    if not local or not dominio or not dominio in VALID_DOMINIOS:
        return False
    return True


def ler_inteiro(mensagem, minimo=None, maximo=None):
    while True:
        valor = input(mensagem).strip()
        try:
            inteiro = int(valor)
            if minimo is not None and inteiro < minimo:
                print(f"Valor deve ser maior ou igual a {minimo}.")
                continue
            if maximo is not None and inteiro > maximo:
                print(f"Valor deve ser menor ou igual a {maximo}.")
                continue
            return inteiro
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")


def ler_float(mensagem, minimo=None, maximo=None):
    while True:
        valor = input(mensagem).strip()
        try:
            flutuante = float(valor)
            if minimo is not None and flutuante < minimo:
                print(f"Valor deve ser maior ou igual a {minimo}.")
                continue
            if maximo is not None and flutuante > maximo:
                print(f"Valor deve ser menor ou igual a {maximo}.")
                continue
            return flutuante
        except ValueError:
            print("Entrada inválida. Por favor, digite um número decimal válido.")


def pausar():
    try:
        input("Digite ENTER para continuar...")
    except Exception:
        # em ambientes não interativos, ignore
        return
