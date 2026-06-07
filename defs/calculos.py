import math

RADIUS_TERRA_KM = 6371.0


def haversine(lat1, lon1, lat2, lon2):
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return RADIUS_TERRA_KM * c


def validacao_latitude(valor):
    return -90.0 <= valor <= 90.0


def validacao_longitude(valor):
    return -180.0 <= valor <= 180.0


def distancia_entre_pontos_metros(lat1, lon1, lat2, lon2):
    return haversine(lat1, lon1, lat2, lon2) * 1000


def distancia_ponto_segmento(lat_origem, lon_origem, lat_destino, lon_destino, lat_ponto, lon_ponto):
    d_origem_ponto = haversine(lat_origem, lon_origem, lat_ponto, lon_ponto) / RADIUS_TERRA_KM
    d_origem_destino = haversine(lat_origem, lon_origem, lat_destino, lon_destino) / RADIUS_TERRA_KM
    if d_origem_destino == 0:
        return distancia_entre_pontos_metros(lat_origem, lon_origem, lat_ponto, lon_ponto)

    def angulo_bearing(lat_a, lon_a, lat_b, lon_b):
        lat_a_rad = math.radians(lat_a)
        lat_b_rad = math.radians(lat_b)
        dlon_rad = math.radians(lon_b - lon_a)
        x = math.sin(dlon_rad) * math.cos(lat_b_rad)
        y = math.cos(lat_a_rad) * math.sin(lat_b_rad) - math.sin(lat_a_rad) * math.cos(lat_b_rad) * math.cos(dlon_rad)
        return math.atan2(x, y)

    theta_12 = angulo_bearing(lat_origem, lon_origem, lat_destino, lon_destino)
    theta_13 = angulo_bearing(lat_origem, lon_origem, lat_ponto, lon_ponto)
    d_xt = math.asin(math.sin(d_origem_ponto) * math.sin(theta_13 - theta_12)) * RADIUS_TERRA_KM
    d_at = math.acos(max(-1.0, min(1.0, math.cos(d_origem_ponto) / math.cos(d_xt / RADIUS_TERRA_KM)))) * RADIUS_TERRA_KM

    if d_at < 0 or d_at > d_origem_destino * RADIUS_TERRA_KM:
        distancia1 = distancia_entre_pontos_metros(lat_ponto, lon_ponto, lat_origem, lon_origem)
        distancia2 = distancia_entre_pontos_metros(lat_ponto, lon_ponto, lat_destino, lon_destino)
        return min(distancia1, distancia2)

    return abs(d_xt) * 1000


def filtrar_postos_no_buffer(lat_ori, lon_ori, lat_des, lon_des, raio_m, postos):
    resultado = []
    for posto in postos:
        distancia = distancia_ponto_segmento(lat_ori, lon_ori, lat_des, lon_des, posto[2], posto[3])
        if distancia <= raio_m:
            resultado.append([posto[0], posto[1], posto[2], posto[3], posto[4], round(distancia, 2)])
    return resultado
