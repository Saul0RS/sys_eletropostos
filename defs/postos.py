from defs.arquivos import ler_postos, salvar_postos, gerar_id
from defs.usuarios import atualizar_status_usuario, obter_posto_usuario, obter_status_usuario
from defs.utils import ler_float, ler_inteiro, pausar


def cadastrar_posto(email_dono):
    print("== Cadastro de novo posto ==")

    nome = input("Nome do posto: ").strip()
    
    if not nome:
        print("Nome do posto não pode ficar vazio.")
        pausar()
        return
    
    lat = ler_float("Latitude do posto (-90 a 90): ", minimo=-90.0, maximo=90.0)
    lon = ler_float("Longitude do posto (-180 a 180): ", minimo=-180.0, maximo=180.0)
    status = "livre"
    postos = ler_postos()
    novo_id = gerar_id(postos)
    postos.append([novo_id, nome, lat, lon, status, email_dono])
    
    salvar_postos(postos)
    print(f"Posto cadastrado com ID {novo_id} e nome {nome}.")
    pausar()


def listar_postos():
    postos = ler_postos()
    print("== Lista de postos ==")

    if not postos:
        print("Nenhum posto cadastrado ainda.")
        pausar()
        return
    
    for posto in postos:
        print(f"{posto[0]} - {posto[1]} | Lat: {posto[2]:.6f} | Lon: {posto[3]:.6f} | Status: {posto[4]} | Dono: {posto[5]}")
    pausar()


def listar_postos_do_dono(email_dono):
    todos_postos = ler_postos()
    postos = []
    for posto in todos_postos:
        if posto[5].lower() == email_dono.lower():
            postos.append(posto)

    print("== Meus postos ==")

    if not postos:
        print("Nenhum posto vinculado ao seu e-mail.")
        pausar()
        return
    
    for posto in postos:
        print(f"{posto[0]} - {posto[1]} | Lat: {posto[2]:.6f} | Lon: {posto[3]:.6f} | Status: {posto[4]}")
    pausar()

def _buscar_posto_por_id(postos, posto_id):
    for posto in postos:
        if posto[0] == posto_id:
            return posto
        
    return None


def fazer_checkin_posto(usuario_email):
    todos_postos = ler_postos()
    postos_livres = []

    for posto in todos_postos:
        if posto[4].lower() == "livre":
            postos_livres.append(posto)

    if not postos_livres:
        print("Nenhum posto livre disponível para check-in.")
        pausar()
        return
    
    print("== Postos livres para check-in ==")
    for posto in postos_livres:
        print(f"{posto[0]} - {posto[1]} | Lat: {posto[2]:.6f} | Lon: {posto[3]:.6f} | Dono: {posto[5]}")

    posto_id = ler_inteiro("Digite o ID do posto para fazer check-in: ", minimo=1, maximo=len(todos_postos))
    selecionado = _buscar_posto_por_id(postos_livres, posto_id)
    
    if selecionado is None:
        print("ID de posto não encontrado entre os postos livres.")
        pausar()
        return
    
    posto_completo = _buscar_posto_por_id(todos_postos, posto_id)
    posto_completo[4] = "ocupado"
    salvar_postos(todos_postos)
    atualizar_status_usuario(usuario_email, "in", posto_id)
    print(f"Check-in realizado no posto {posto_completo[1]}.")
    pausar()


def fazer_checkout_posto(usuario_email):
    status = obter_status_usuario(usuario_email)

    if status != "in":
        print("Você não está em nenhum posto (nenhum check-in ativo).")
        pausar()
        return
    
    posto_id_str = obter_posto_usuario(usuario_email)
    if not posto_id_str:
        print("Nenhum posto vinculado ao seu check-in. Contate o administrador.")
        pausar()
        return
    
    try:
        posto_id = int(posto_id_str)
    except ValueError:
        print("ID de posto inválido armazenado no usuário.")
        pausar()
        return
    
    todos_postos = ler_postos()
    posto_completo = _buscar_posto_por_id(todos_postos, posto_id)
    
    if posto_completo is None:
        print("O posto associado ao seu check-in não foi encontrado.")
        atualizar_status_usuario(usuario_email, "out", "")
        pausar()
        return
    
    print(f"Realizando check-out no posto {posto_completo[0]} - {posto_completo[1]} | Lat: {posto_completo[2]:.6f} | Lon: {posto_completo[3]:.6f} | Dono: {posto_completo[5]}")
    posto_completo[4] = "livre"
    salvar_postos(todos_postos)
    atualizar_status_usuario(usuario_email, "out", "")
    print(f"Check-out realizado no posto {posto_completo[1]}.")
    pausar()


def modificar_posto(email_dono):
    postos = ler_postos()
    meus_postos = []

    for posto in postos:
        if posto[5].lower() == email_dono.lower():
            meus_postos.append(posto)

    if not meus_postos:
        print("Nenhum posto vinculado ao seu e-mail.")
        pausar()
        return
    
    listar_postos_do_dono(email_dono)
    posto_id = ler_inteiro("Digite o ID do posto que deseja alterar: ", minimo=1, maximo=len(postos))
    selecionado = _buscar_posto_por_id(meus_postos, posto_id)

    if selecionado is None:
        print("ID de posto não encontrado entre seus postos.")
        pausar()
        return
    
    novo_nome = input(f"Novo nome do posto (ENTER para manter '{selecionado[1]}'): ").strip()

    if not novo_nome:
        print("Nome do posto não pode ficar vazio.")
        return
    
    nova_lat = ler_float("Nova latitude do posto (-90 a 90): ", minimo=-90.0, maximo=90.0)
    nova_lon = ler_float("Nova longitude do posto (-180 a 180): ", minimo=-180.0, maximo=180.0)
    novo_status = input("Novo status do posto (livre/ocupado): ").strip().lower()
    
    if novo_status not in ["livre", "ocupado"]:
        print("Status inválido. Use 'livre' ou 'ocupado'.")
        return
    
    selecionado[1] = novo_nome
    selecionado[2] = nova_lat
    selecionado[3] = nova_lon
    selecionado[4] = novo_status
    salvar_postos(postos)
    print("Posto alterado com sucesso.")
    pausar()


def deletar_posto(email_dono):
    postos = ler_postos()
    meus_postos = []

    for posto in postos:
        if posto[5].lower() == email_dono.lower():
            meus_postos.append(posto)

    if not meus_postos:
        print("Nenhum posto vinculado ao seu e-mail.")
        pausar()
        return
    
    listar_postos_do_dono(email_dono)
    posto_id = ler_inteiro("Digite o ID do posto que deseja deletar: ", minimo=1, maximo=len(postos))
    selecionado = _buscar_posto_por_id(meus_postos, posto_id)

    if selecionado is None:
        print("ID de posto não encontrado entre seus postos.")
        return
    
    postos.remove(selecionado)
    salvar_postos(postos)
    print(f"Posto {selecionado[1]} deletado com sucesso.")
    pausar()