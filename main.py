from defs.usuarios import menu_autenticacao, menu_gerenciar_usuario, obter_status_usuario
from defs.postos import listar_postos, fazer_checkin_posto, fazer_checkout_posto, menu_posto
from defs.calculos import rota_postos
from defs.arquivos import ler_postos
from defs.utils import ler_float, ler_inteiro, limpar_tela, pausar


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
        return
    dist_rota, postos_no_caminho = rota_postos(lat_ori, lon_ori, lat_des, lon_des, postos, raio)
    print(f"\nDistância aproximada da rota: {dist_rota:.2f} metros")
    print(f"Total de postos no caminho: {len(postos_no_caminho)}")
    if not postos_no_caminho:
        print("Nenhum posto encontrado dentro do buffer informado.")
        return
    print("\n== Postos no caminho ==")
    for posto in postos_no_caminho:
        print(f"{posto[0]} - {posto[1]} | Status: {posto[4]} | Distância até a rota: {posto[5]} m")
    pausar()


def menu_usuario_logado(usuario_email, nome_usuario, usuario_tipo):
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
            break
    return False


def main():
    while True:
        usuario_email, nome_usuario, usuario_tipo, _ = menu_autenticacao()
        if usuario_email is None:
            break
        usuario_deletado = menu_usuario_logado(usuario_email, nome_usuario, usuario_tipo)
        if usuario_deletado:
            continue


if __name__ == "__main__":
    main()
