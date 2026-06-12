import math

R = 6371.0


def hav(lat1, lon1, lat2, lon2):
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def br(lat_a, lon_a, lat_b, lon_b):
    lat_a_rad = math.radians(lat_a)
    lat_b_rad = math.radians(lat_b)
    dlon_rad = math.radians(lon_b - lon_a)
    x = math.sin(dlon_rad) * math.cos(lat_b_rad)
    y = math.cos(lat_a_rad) * math.sin(lat_b_rad) - math.sin(lat_a_rad) * math.cos(lat_b_rad) * math.cos(dlon_rad)
    return math.atan2(x, y)


def rota_postos(lat_o, lon_o, lat_d, lon_d, postos, raio_m):
    def dist_m(a_lat, a_lon, b_lat, b_lon):
        return hav(a_lat, a_lon, b_lat, b_lon) * 1000

    # validações simples
    if not (-90.0 <= lat_o <= 90.0 and -90.0 <= lat_d <= 90.0 and -180.0 <= lon_o <= 180.0 and -180.0 <= lon_d <= 180.0):
        raise ValueError("Coordenadas inválidas")

    def dist_point_seg(lo, ln, latd, lond, latp, lonp):
        d_op = hav(lo, ln, latp, lonp) / R
        d_od = hav(lo, ln, latd, lond) / R
        if d_od == 0:
            return dist_m(lo, ln, latp, lonp)

        t12 = br(lo, ln, latd, lond)
        t13 = br(lo, ln, latp, lonp)
        d_xt = math.asin(math.sin(d_op) * math.sin(t13 - t12)) * R
        d_at = math.acos(max(-1.0, min(1.0, math.cos(d_op) / math.cos(d_xt / R)))) * R

        if d_at < 0 or d_at > d_od * R:
            d1 = dist_m(latp, lonp, lo, ln)
            d2 = dist_m(latp, lonp, latd, lond)
            return min(d1, d2)
        return abs(d_xt) * 1000

    total = dist_m(lat_o, lon_o, lat_d, lon_d)
    res = []
    for p in postos:
        d = dist_point_seg(lat_o, lon_o, lat_d, lon_d, p[2], p[3])
        if d <= raio_m:
            res.append([p[0], p[1], p[2], p[3], p[4], round(d, 2)])
    return total, res
