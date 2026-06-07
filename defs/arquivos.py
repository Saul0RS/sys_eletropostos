import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, "db")
os.makedirs(DB_DIR, exist_ok=True)
USUARIOS_ARQUIVO = os.path.join(DB_DIR, "usuarios.txt")
POSTOS_ARQUIVO = os.path.join(DB_DIR, "postos.txt")


def criar_arquivo_se_nao_existe(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write("")


def gerar_id(lista_itens):
    if not lista_itens:
        return 1
    return max(item[0] for item in lista_itens) + 1


def ler_usuarios():
    criar_arquivo_se_nao_existe(USUARIOS_ARQUIVO)
    usuarios = []
    with open(USUARIOS_ARQUIVO, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha:
                continue
            partes = linha.split(",")
            if len(partes) >= 4 and "@" in partes[0]:
                email = partes[0].strip().lower()
                nome = partes[1].strip()
                senha = partes[2]
                tipo = partes[3].strip()
                status = partes[4].strip().lower() if len(partes) >= 5 else "out"
                posto_atual = partes[5].strip() if len(partes) >= 6 else ""
                usuarios.append([email, nome, senha, tipo, status, posto_atual])
    return usuarios


def salvar_usuarios(usuarios):
    with open(USUARIOS_ARQUIVO, "w", encoding="utf-8") as arquivo:
        for usuario in usuarios:
            status = usuario[4] if len(usuario) > 4 else "out"
            posto_atual = usuario[5] if len(usuario) > 5 else ""
            linha = f"{usuario[0]},{usuario[1]},{usuario[2]},{usuario[3]},{status},{posto_atual}\n"
            arquivo.write(linha)


def ler_postos():
    criar_arquivo_se_nao_existe(POSTOS_ARQUIVO)
    postos = []
    with open(POSTOS_ARQUIVO, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha:
                continue
            partes = linha.split(",")
            if len(partes) >= 5:
                try:
                    posto_id = int(partes[0])
                    lat = float(partes[2])
                    lon = float(partes[3])
                except ValueError:
                    continue
                dono_email = partes[5].strip() if len(partes) >= 6 else ""
                postos.append([posto_id, partes[1], lat, lon, partes[4], dono_email])
    return postos


def salvar_postos(postos):
    with open(POSTOS_ARQUIVO, "w", encoding="utf-8") as arquivo:
        for posto in postos:
            dono_email = posto[5] if len(posto) > 5 else ""
            linha = f"{posto[0]},{posto[1]},{posto[2]:.6f},{posto[3]:.6f},{posto[4]},{dono_email}\n"
            arquivo.write(linha)
