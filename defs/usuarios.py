from defs.arquivos import ler_list_user, save_user, ler_postos, salvar_postos
from defs.utils import ler_texto, ler_inteiro, ler_senha, validar_email


def cadastrar_usuario():
    print("== Cadastro de novo usuário ==")

    nome = input("Nome do usuário: ")
    email = input("E-mail do usuário: ").lower()

    if not validar_email(email):
        print("E-mail inválido. Utilize um domínio suportado e formato correto.")
        return
    
    usuarios = ler_list_user()
    if any(usuario[0] == email for usuario in usuarios):
        print("E-mail já cadastrado. Utilize outro e-mail.")
        return
    senha = ler_senha("Senha: ")
    senha_confirmacao = ler_senha("Confirme a senha: ")
    if senha != senha_confirmacao:
        print("As senhas não coincidem. Tente novamente.")
        return
    print("Escolha o tipo de usuário:")
    print("1 - Cliente")
    print("2 - Dono de posto")
    opcao_tipo = ler_inteiro("Tipo de usuário: ", minimo=1, maximo=2)
    tipo = "cliente" if opcao_tipo == 1 else "dono_de_posto"
    usuarios.append([email, nome, senha, tipo, "out"])
    save_user(usuarios)
    print(f"Usuário cadastrado com e-mail {email} e nome {nome}.")


def fazer_login():
    print("== Login ==")
    email = ler_texto("E-mail do usuário: ").lower()
    if not validar_email(email):
        print("E-mail inválido. Utilize um domínio suportado e formato correto.")
        return None, None, None, None
    senha = ler_senha("Senha: ")
    usuarios = ler_list_user()
    for usuario in usuarios:
        if usuario[0] == email and usuario[2] == senha:
            print(f"Bem-vindo, {usuario[1]}!")
            status = usuario[4] if len(usuario) > 4 else "out"
            return usuario[0], usuario[1], usuario[3], status
    print("E-mail ou senha incorretos. Tente novamente.")
    return None, None, None, None


def obter_status_usuario(email_usuario):
    usuarios = ler_list_user()
    for usuario in usuarios:
        if usuario[0] == email_usuario:
            return usuario[4] if len(usuario) > 4 else "out"
    return "out"


def obter_posto_usuario(email_usuario):
    usuarios = ler_list_user()
    for usuario in usuarios:
        if usuario[0] == email_usuario:
            return usuario[5] if len(usuario) > 5 and usuario[5] else ""
    return ""


def atualizar_status_usuario(email_usuario, novo_status, posto_id=""):
    usuarios = ler_list_user()
    for usuario in usuarios:
        if usuario[0] == email_usuario:
            usuario[4] = novo_status
            # armazena o id do posto (string) quando estiver 'in'
            usuario_atual = posto_id if posto_id is not None else ""
            if len(usuario) > 5:
                usuario[5] = str(usuario_atual)
            else:
                usuario.append(str(usuario_atual))
            save_user(usuarios)
            return True
    return False


def alterar_nome(email_usuario):
    usuarios = ler_list_user()
    for usuario in usuarios:
        if usuario[0] == email_usuario:
            novo_nome = ler_texto("Novo nome: ")
            usuario[1] = novo_nome
            save_user(usuarios)
            print("Nome atualizado com sucesso.")
            return
    print("Usuário não encontrado.")


def alterar_senha(email_usuario):
    usuarios = ler_list_user()
    for usuario in usuarios:
        if usuario[0] == email_usuario:
            senha_atual = ler_senha("Senha atual: ")
            if senha_atual != usuario[2]:
                print("Senha atual incorreta.")
                return
            nova_senha = ler_senha("Nova senha: ")
            confirmacao = ler_senha("Confirme a nova senha: ")
            if nova_senha != confirmacao:
                print("As senhas não coincidem.")
                return
            usuario[2] = nova_senha
            save_user(usuarios)
            print("Senha atualizada com sucesso.")
            return
    print("Usuário não encontrado.")


def deletar_usuario(email_usuario):
    usuarios = ler_list_user()
    usuarios_ativos = [usuario for usuario in usuarios if usuario[0] != email_usuario]
    if len(usuarios_ativos) == len(usuarios):
        print("Usuário não encontrado.")
        return False
    save_user(usuarios_ativos)
    postos = ler_postos()
    postos_ativos = [posto for posto in postos if len(posto) <= 5 or posto[5].lower() != email_usuario.lower()]
    salvar_postos(postos_ativos)
    print("Usuário deletado com sucesso. Seus postos também foram removidos.")
    return True


def menu_gerenciar_usuario(email_usuario):
    while True:
        print("== Gerenciar meu usuário ==")
        print("1 - Alterar nome")
        print("2 - Alterar senha")
        print("3 - Deletar usuário")
        print("0 - Voltar")
        opcao = ler_inteiro("Escolha uma opção: ", minimo=0, maximo=3)
        if opcao == 1:
            alterar_nome(email_usuario)
        elif opcao == 2:
            alterar_senha(email_usuario)
        elif opcao == 3:
            if deletar_usuario(email_usuario):
                return True
        elif opcao == 0:
            break
    return False


def menu_autenticacao():
    while True:
        print("===== Sistema de eletropostos CLI =====")
        print("1 - Cadastrar")
        print("2 - Login")
        print("0 - Sair")
        opcao = ler_inteiro("Escolha uma opção: ", minimo=0, maximo=2)
        if opcao == 1:
            cadastrar_usuario()
        elif opcao == 2:
            usuario_email, nome_usuario, usuario_tipo, usuario_status = fazer_login()
            if usuario_email is not None:
                return usuario_email, nome_usuario, usuario_tipo, usuario_status
        elif opcao == 0:
            print("Encerrando o sistema. Até mais!")
            return None, None, None, None
