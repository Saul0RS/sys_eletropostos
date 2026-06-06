from arquivos import ler_postos, salvar_postos, gerar_id
from utils import ler_texto, ler_float, ler_inteiro


def cadastrar_posto(email_dono):
    print("\n== Cadastro de novo posto ==")
    nome = ler_texto("Nome do posto: ")
    lat = ler_float("Latitude do posto (-90 a 90): ", minimo=-90.0, maximo=90.0)
    lon = ler_float("Longitude do posto (-180 a 180): ", minimo=-180.0, maximo=180.0)
    status = "livre"
    postos = ler_postos()
    novo_id = gerar_id(postos)
    postos.append([novo_id, nome, lat, lon, status, email_dono])
    salvar_postos(postos)
    print(f"Posto cadastrado com ID {novo_id} e nome {nome}.")


def listar_postos():
    postos = ler_postos()
    print("\n== Lista de postos ==")
    if not postos:
        print("Nenhum posto cadastrado ainda.")
        return
    for posto in postos:
        dono = posto[5] if len(posto) > 5 and posto[5] else "N/A"
        print(f"{posto[0]} - {posto[1]} | Lat: {posto[2]:.6f} | Lon: {posto[3]:.6f} | Status: {posto[4]} | Dono: {dono}")


def listar_postos_do_dono(email_dono):
    postos = [posto for posto in ler_postos() if len(posto) > 5 and posto[5].lower() == email_dono.lower()]
    print("\n== Meus postos ==")
    if not postos:
        print("Nenhum posto vinculado ao seu e-mail.")
        return
    for posto in postos:
        print(f"{posto[0]} - {posto[1]} | Lat: {posto[2]:.6f} | Lon: {posto[3]:.6f} | Status: {posto[4]}")


def _buscar_posto_por_id(postos, posto_id):
    for posto in postos:
        if posto[0] == posto_id:
            return posto
    return None


def fazer_checkin_posto(usuario_email):
    postos = ler_postos()
    if not postos:
        print("Nenhum posto cadastrado.")
        return
    listar_postos()
    posto_id = ler_inteiro("Digite o ID do posto para fazer check-in: ", minimo=1)
    selecionado = _buscar_posto_por_id(postos, posto_id)
    if selecionado is None:
        print("ID de posto não encontrado.")
        return
    selecionado[4] = "ocupado"
    salvar_postos(postos)
    print(f"Check-in realizado no posto {selecionado[1]}.")


def fazer_checkout_posto(usuario_email):
    postos = ler_postos()
    if not postos:
        print("Nenhum posto cadastrado.")
        return
    listar_postos()
    posto_id = ler_inteiro("Digite o ID do posto para fazer check-out: ", minimo=1)
    selecionado = _buscar_posto_por_id(postos, posto_id)
    if selecionado is None:
        print("ID de posto não encontrado.")
        return
    selecionado[4] = "livre"
    salvar_postos(postos)
    print(f"Check-out realizado no posto {selecionado[1]}.")


def modificar_posto(email_dono):
    postos = ler_postos()
    meus_postos = [posto for posto in postos if len(posto) > 5 and posto[5].lower() == email_dono.lower()]
    if not meus_postos:
        print("Nenhum posto vinculado ao seu e-mail.")
        return
    listar_postos_do_dono(email_dono)
    posto_id = ler_inteiro("Digite o ID do posto que deseja alterar: ", minimo=1)
    selecionado = _buscar_posto_por_id(meus_postos, posto_id)
    if selecionado is None:
        print("ID de posto não encontrado entre seus postos.")
        return
    novo_nome = ler_texto("Novo nome do posto: ")
    nova_lat = ler_float("Nova latitude do posto (-90 a 90): ", minimo=-90.0, maximo=90.0)
    nova_lon = ler_float("Nova longitude do posto (-180 a 180): ", minimo=-180.0, maximo=180.0)
    novo_status = ler_texto("Novo status do posto (livre/ocupado): ").lower()
    if novo_status not in ["livre", "ocupado"]:
        print("Status inválido. Use 'livre' ou 'ocupado'.")
        return
    selecionado[1] = novo_nome
    selecionado[2] = nova_lat
    selecionado[3] = nova_lon
    selecionado[4] = novo_status
    salvar_postos(postos)
    print("Posto alterado com sucesso.")


def deletar_posto(email_dono):
    postos = ler_postos()
    meus_postos = [posto for posto in postos if len(posto) > 5 and posto[5].lower() == email_dono.lower()]
    if not meus_postos:
        print("Nenhum posto vinculado ao seu e-mail.")
        return
    listar_postos_do_dono(email_dono)
    posto_id = ler_inteiro("Digite o ID do posto que deseja deletar: ", minimo=1)
    selecionado = _buscar_posto_por_id(meus_postos, posto_id)
    if selecionado is None:
        print("ID de posto não encontrado entre seus postos.")
        return
    postos.remove(selecionado)
    salvar_postos(postos)
    print(f"Posto {selecionado[1]} deletado com sucesso.")


def menu_posto(email_dono):
    while True:
        print("\n===== Gerenciamento de postos =====")
        print("1 - Ver meus postos")
        print("2 - Cadastrar posto")
        print("3 - Alterar posto")
        print("4 - Deletar posto")
        print("0 - Voltar")
        opcao = ler_inteiro("Escolha uma opção: ", minimo=0, maximo=4)
        if opcao == 1:
            listar_postos_do_dono(email_dono)
        elif opcao == 2:
            cadastrar_posto(email_dono)
        elif opcao == 3:
            modificar_posto(email_dono)
        elif opcao == 4:
            deletar_posto(email_dono)
        elif opcao == 0:
            break
