from django.contrib.gis.geoip2 import GeoIP2
from django.core.validators import validate_ipv4_address

from django.core.exceptions import ValidationError


def is_valid_ip(ip_str: str) -> bool:
    try:
        validate_ipv4_address(ip_str)
        return True
    except ValidationError:
        return False


def is_valid_lat_long(lat: float | str, lng: float | str) -> bool:
    lat = float(lat)
    lng = float(lng)

    if lat < -90 or lat > 90 or lng < -180 or lng > 180:
        return False
    return True


def get_location_from_ip(ip_address: str) -> (float, float):
    geo_ip = GeoIP2()
    lat, lng = geo_ip.lat_lon(ip_address)
    return lat, lng
