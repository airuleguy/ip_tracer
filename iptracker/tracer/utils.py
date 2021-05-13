import math


EARTH_RADIUS = 6371


def deg2rad(deg):
    return deg * (math.pi/180)


def get_distance_in_km(lat1, lon1, lat2, lon2):
    d_lat = deg2rad(lat2 - lat1)
    d_lon = deg2rad(lon2 - lon1)
    a = math.sin(d_lat/2) * math.sin(d_lat/2) + \
        math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * \
        math.sin(d_lon/2) * math.sin(d_lon/2)
    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1-a)
    )
    result = EARTH_RADIUS * c
    return result


def ip_is_valid(ip: str) -> bool:
    try:
        parts = ip.split('.')
        return (
            len(parts) == 4 and
            all(0 < len(part) < 4 and 0 <= int(part) < 256 for part in parts)
        )
    except (AttributeError, TypeError, ValueError):
        return False
