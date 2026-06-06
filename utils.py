def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print("Entrada inválida. Por favor, informe um texto não vazio.")


def ler_senha(mensagem):
    while True:
        senha = input(mensagem).strip()
        if senha:
            return senha
        print("Entrada inválida. Por favor, informe uma senha não vazia.")


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
