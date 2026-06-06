from arquivos import ler_usuarios, salvar_usuarios, ler_postos, salvar_postos
from utils import ler_texto, ler_inteiro, ler_senha


def cadastrar_usuario():
    print("\n== Cadastro de novo usuário ==")
    nome = ler_texto("Nome do usuário: ")
    email = ler_texto("E-mail do usuário: ").lower()
    usuarios = ler_usuarios()
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
    usuarios.append([email, nome, senha, tipo])
    salvar_usuarios(usuarios)
    print(f"Usuário cadastrado com e-mail {email} e nome {nome}.")


def fazer_login():
    print("\n== Login ==")
    email = ler_texto("E-mail do usuário: ").lower()
    senha = ler_senha("Senha: ")
    usuarios = ler_usuarios()
    for usuario in usuarios:
        if usuario[0] == email and usuario[2] == senha:
            print(f"Bem-vindo, {usuario[1]}!")
            return usuario[0], usuario[1], usuario[3]
    print("E-mail ou senha incorretos. Tente novamente.")
    return None, None, None


def alterar_nome(email_usuario):
    usuarios = ler_usuarios()
    for usuario in usuarios:
        if usuario[0] == email_usuario:
            novo_nome = ler_texto("Novo nome: ")
            usuario[1] = novo_nome
            salvar_usuarios(usuarios)
            print("Nome atualizado com sucesso.")
            return
    print("Usuário não encontrado.")


def alterar_senha(email_usuario):
    usuarios = ler_usuarios()
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
            salvar_usuarios(usuarios)
            print("Senha atualizada com sucesso.")
            return
    print("Usuário não encontrado.")


def deletar_usuario(email_usuario):
    usuarios = ler_usuarios()
    usuarios_ativos = [usuario for usuario in usuarios if usuario[0] != email_usuario]
    if len(usuarios_ativos) == len(usuarios):
        print("Usuário não encontrado.")
        return False
    salvar_usuarios(usuarios_ativos)
    postos = ler_postos()
    postos_ativos = [posto for posto in postos if posto[5].lower() != email_usuario.lower()]
    salvar_postos(postos_ativos)
    print("Usuário deletado com sucesso. Seus postos também foram removidos.")
    return True


def menu_gerenciar_usuario(email_usuario):
    while True:
        print("\n== Gerenciar meu usuário ==")
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
        print("\n===== Sistema de eletropostos CLI =====")
        print("1 - Cadastrar")
        print("2 - Login")
        print("0 - Sair")
        opcao = ler_inteiro("Escolha uma opção: ", minimo=0, maximo=2)
        if opcao == 1:
            cadastrar_usuario()
        elif opcao == 2:
            usuario_email, nome_usuario, usuario_tipo = fazer_login()
            if usuario_email is not None:
                return usuario_email, nome_usuario, usuario_tipo
        elif opcao == 0:
            print("Encerrando o sistema. Até mais!")
            return None, None, None
