from defs.arquivos import ler_list_user, save_user, ler_postos, salvar_postos
from defs.utils import ler_inteiro, validar_email, limpar_tela


def cadastrar_usuario():
    print("== Cadastro de novo usuário ==")

    nome = input("Nome do usuário: ").strip()
    if not nome:
        print("Nome não pode ficar vazio.")
        return
    email = input("E-mail do usuário: ").strip().lower()
    if not validar_email(email):
        print("E-mail inválido. Utilize um domínio suportado e formato correto.")
        return
    
    usuarios = ler_list_user()
    if any(usuario[0] == email for usuario in usuarios):
        print("E-mail já cadastrado. Utilize outro e-mail.")
        return
    senha = input("Senha: ")
    if not senha:
        print("Senha não pode ficar vazia.")
        return
    senha_confirmacao = input("Confirme a senha: ")
    if senha != senha_confirmacao:
        print("As senhas não coincidem. Tente novamente.")
        return
    print("Escolha o tipo de usuário:")
    print("1 - Cliente")
    print("2 - Dono de posto")
    opcao_tipo = ler_inteiro("Tipo de usuário: ", minimo=1, maximo=2)
    if opcao_tipo == 1:
        tipo = "cliente"
    else:
        tipo = "dono_de_posto"
    usuarios.append([email, nome, senha, tipo, "out"])
    save_user(usuarios)
    print(f"Usuário cadastrado com e-mail {email} e nome {nome}.")


def fazer_login():
    print("== Login ==")
    email = input("E-mail do usuário: ").strip().lower()
    if not validar_email(email):
        print("E-mail inválido. Utilize um domínio suportado e formato correto.")
        return None, None, None, None
    senha = input("Senha: ")
    if not senha:
        print("Senha não pode ficar vazia.")
        return None, None, None, None
    usuarios = ler_list_user()
    for usuario in usuarios:
        if usuario[0] == email and usuario[2] == senha:
            print(f"Bem-vindo, {usuario[1]}!")
            if len(usuario) > 4:
                status = usuario[4]
            else:
                status = "out"
            return usuario[0], usuario[1], usuario[3], status
    print("E-mail ou senha incorretos. Tente novamente.")
    return None, None, None, None


def obter_status_usuario(email_usuario):
    usuarios = ler_list_user()
    for usuario in usuarios:
        if usuario[0] == email_usuario:
            if len(usuario) > 4:
                return usuario[4]
            return "out"
    return "out"


def obter_posto_usuario(email_usuario):
    usuarios = ler_list_user()
    for usuario in usuarios:
        if usuario[0] == email_usuario:
            if len(usuario) > 5 and usuario[5]:
                return usuario[5]
            return ""
    return ""


def atualizar_status_usuario(email_usuario, novo_status, posto_id=""):
    usuarios = ler_list_user()
    for usuario in usuarios:
        if usuario[0] == email_usuario:
            usuario[4] = novo_status
            # armazena o id do posto (string) quando estiver 'in'
            if posto_id is not None:
                usuario_atual = posto_id
            else:
                usuario_atual = ""
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
            novo_nome = input("Novo nome: ").strip()
            if not novo_nome:
                print("Nome não pode ficar vazio.")
                return
            usuario[1] = novo_nome
            save_user(usuarios)
            print("Nome atualizado com sucesso.")
            return
    print("Usuário não encontrado.")


def alterar_senha(email_usuario):
    usuarios = ler_list_user()
    for usuario in usuarios:
        if usuario[0] == email_usuario:
            senha_atual = input("Senha atual: ")
            if not senha_atual:
                print("Senha atual não pode ficar vazia.")
                return
            if senha_atual != usuario[2]:
                print("Senha atual incorreta.")
                return
            nova_senha = input("Nova senha: ")
            if not nova_senha:
                print("Nova senha não pode ficar vazia.")
                return
            confirmacao = input("Confirme a nova senha: ")
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
        limpar_tela()
        print("== Gerenciar meu usuário ==")
        print("1 - Alterar nome")
        print("2 - Alterar senha")
        print("3 - Deletar usuário")
        print("0 - Voltar")
        opcao = ler_inteiro("Escolha uma opção: ", minimo=0, maximo=3)
        if opcao == 1:
            limpar_tela()
            alterar_nome(email_usuario)
        elif opcao == 2:
            limpar_tela()
            alterar_senha(email_usuario)
        elif opcao == 3:
            limpar_tela()
            if deletar_usuario(email_usuario):
                return True
        elif opcao == 0:
            break
    return False


def menu_autenticacao():
    while True:
        limpar_tela()
        print("===== Sistema de eletropostos CLI =====")
        print("1 - Cadastrar")
        print("2 - Login")
        print("0 - Sair")
        opcao = ler_inteiro("Escolha uma opção: ", minimo=0, maximo=2)
        if opcao == 1:
            limpar_tela()
            cadastrar_usuario()
        elif opcao == 2:
            limpar_tela()
            usuario_email, nome_usuario, usuario_tipo, usuario_status = fazer_login()
            if usuario_email is not None:
                return usuario_email, nome_usuario, usuario_tipo, usuario_status
        elif opcao == 0:
            print("Encerrando o sistema. Até mais!")
            return None, None, None, None
