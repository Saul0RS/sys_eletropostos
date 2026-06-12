import os

from defs.arquivos import ler_postos
from defs.calculos import rota_postos


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
            vinteiro = int(valor)
            if vinteiro >= minimo and vinteiro <= maximo:
                return vinteiro
            else:
                print(f"Valor deve ser entre {minimo} e {maximo}.")
                continue        
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")


def ler_float(mensagem, minimo=None, maximo=None):
    while True:
        valor = input(mensagem).strip()
        try:
            vfloat = float(valor)
            if vfloat >= minimo and vfloat <= maximo:
                return vfloat
            else:
                print(f"Valor deve ser entre {minimo} e {maximo}.")
                continue

        except ValueError:
            print("Entrada inválida. Por favor, digite um número decimal válido.")


def pausar():
    try:
        input("Digite ENTER para continuar...")
    except Exception:
        # em ambientes não interativos, ignore
        return


def menu_rotas():
    
    limpar_tela()
    print("== Traçar rota e buscar postos no caminho ==")
    lat_ori = ler_float("Latitude de origem (-90 a 90): ", minimo=-90.0, maximo=90.0)
    lon_ori = ler_float("Longitude de origem (-180 a 180): ", minimo=-180.0, maximo=180.0)
    lat_des = ler_float("Latitude de destino (-90 a 90): ", minimo=-90.0, maximo=90.0)
    lon_des = ler_float("Longitude de destino (-180 a 180): ", minimo=-180.0, maximo=180.0)
    raio = ler_float("Buffer em metros para buscar postos: ", minimo=0.0)
    postos = ler_postos()
    if not postos:
        print("Nenhum posto cadastrado. Cadastre postos antes de traçar a rota.")
        pausar()
        return
    dist_rota, postos_no_caminho = rota_postos(lat_ori, lon_ori, lat_des, lon_des, postos, raio)
    print(f"\nDistância aproximada da rota: {dist_rota:.2f} metros")
    print(f"Total de postos no caminho: {len(postos_no_caminho)}")
    if not postos_no_caminho:
        print("Nenhum posto encontrado dentro do buffer informado.")
        pausar()
        return
    print("\n== Postos no caminho ==")
    for posto in postos_no_caminho:
        print(f"{posto[0]} - {posto[1]} | Status: {posto[4]} | Distância até a rota: {posto[5]} m")
    pausar()


def menu_usuario_logado(usuario_email, nome_usuario, usuario_tipo):
    from defs.usuarios import obter_status_usuario, menu_gerenciar_usuario
    from defs.postos import listar_postos, fazer_checkin_posto, fazer_checkout_posto

    while True:
        limpar_tela()
        status = obter_status_usuario(usuario_email)
        if status not in ["in", "out"]:
            status = "out"
        print(f"===== Menu de {nome_usuario} =====")
        print("1 - Traçar rota e buscar postos")
        print("2 - Ver lista de postos")
        if status == "out":
            print("3 - Check-in em um posto")
        else:
            print("3 - Check-out em um posto")
        print("5 - Gerenciar usuário")
        if usuario_tipo == "dono_de_posto":
            print("6 - Gerenciar meus postos")
            max_opcao = 6
        else:
            max_opcao = 5
        print("0 - Sair")
        opcao = ler_inteiro("Escolha uma opção: ", minimo=0, maximo=max_opcao)
        if opcao == 1:
            menu_rotas()
        elif opcao == 2:
            limpar_tela()
            listar_postos()
        elif opcao == 3:
            limpar_tela()
            if status == "out":
                fazer_checkin_posto(usuario_email)
            else:
                fazer_checkout_posto(usuario_email)
        elif opcao == 5:
            limpar_tela()
            if menu_gerenciar_usuario(usuario_email):
                return True
        elif opcao == 6 and usuario_tipo == "dono_de_posto":
            limpar_tela()
            menu_posto(usuario_email)
        elif opcao == 0:
            print(f"Deslogando {nome_usuario}. Até mais!")
            pausar()
            break
    return False


def menu_posto(email_dono):
    from defs.postos import listar_postos_do_dono, cadastrar_posto, modificar_posto, deletar_posto

    while True:
        limpar_tela()
        print("\n===== Gerenciamento de postos =====")
        print("1 - Ver meus postos")
        print("2 - Cadastrar posto")
        print("3 - Alterar posto")
        print("4 - Deletar posto")
        print("0 - Voltar")
        opcao = ler_inteiro("Escolha uma opção: ", minimo=0, maximo=4)
        if opcao == 1:
            limpar_tela()
            listar_postos_do_dono(email_dono)
        elif opcao == 2:
            limpar_tela()
            cadastrar_posto(email_dono)
        elif opcao == 3:
            limpar_tela()
            modificar_posto(email_dono)
        elif opcao == 4:
            limpar_tela()
            deletar_posto(email_dono)
        elif opcao == 0:
            break


def main():
    from defs.usuarios import menu_autenticacao

    while True:
        usuario_email, nome_usuario, usuario_tipo, _ = menu_autenticacao()
        if usuario_email is None:
            break
        usuario_deletado = menu_usuario_logado(usuario_email, nome_usuario, usuario_tipo)
        if usuario_deletado:
            continue
