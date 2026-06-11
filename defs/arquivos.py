import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, "db")
os.makedirs(DB_DIR, exist_ok=True)
USUARIOS_ARQUIVO = os.path.join(DB_DIR, "usuarios.txt")
POSTOS_ARQUIVO = os.path.join(DB_DIR, "postos.txt")


def cria_arquivo(name_file):
    if not os.path.exists(name_file):
        with open(name_file, "w", encoding="utf-8") as file:
            file.write("")
    return 

def gerar_id(itens):
    if not itens:
        return 1
    return max(item[0] for item in itens) + 1


def ler_list_user():
    cria_arquivo(USUARIOS_ARQUIVO)

    usuarios = []
    with open(USUARIOS_ARQUIVO, "r", encoding="utf-8") as file:
        for linha in file:
            linha = linha.strip()

            if not linha:
                continue

            lineuser = linha.split(",")

            if len(lineuser) >= 4 and "@" in lineuser[0]:
                email = lineuser[0].strip().lower()
                nome = lineuser[1].strip()
                senha = lineuser[2]
                tipo = lineuser[3].strip()
                if len(lineuser) > 4:
                    status = lineuser[4].strip().lower()
                else:
                    status = "out"
                posto_atual = lineuser[5].strip() if len(lineuser) > 5 else ""
                usuarios.append([email, nome, senha, tipo, status, posto_atual])

    return usuarios


def save_user(user):
    with open(USUARIOS_ARQUIVO, "w", encoding="utf-8") as file:
        for usuario in user:
            status = usuario[4] if len(usuario) > 4 else "out"
            posto_atual = usuario[5] if len(usuario) > 5 else ""
            linha = f"{usuario[0]},{usuario[1]},{usuario[2]},{usuario[3]},{status},{posto_atual}\n"
            file.write(linha)


def ler_postos():
    cria_arquivo(POSTOS_ARQUIVO)
    postos = []
    with open(POSTOS_ARQUIVO, "r", encoding="utf-8") as file:
        for linha in file:
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
    with open(POSTOS_ARQUIVO, "w", encoding="utf-8") as file:
        for posto in postos:
            dono_email = posto[5] if len(posto) > 5 else ""
            linha = f"{posto[0]},{posto[1]},{posto[2]:.6f},{posto[3]:.6f},{posto[4]},{dono_email}\n"
            file.write(linha)
