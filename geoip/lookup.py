import geoip2.database
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "geoip" / "GeoLite2-City.mmdb"

_reader = None

def get_reader():
    global _reader
    if _reader is None:
        _reader = geoip2.database.Reader(str(DB_PATH))
    return _reader


def lookup_ip(ip: str) -> dict:
    try:
        reader = get_reader()
        response = reader.city(ip)

        return {
            "lat": response.location.latitude,
            "lon": response.location.longitude,
            "country": response.country.iso_code,
            "city": response.city.name
        }

    except Exception:
        # fallback for private / unknown IPs
        return {
            "lat": None,
            "lon": None,
            "country": "UNKNOWN",
            "city": None
        }
