import geoip2.database

DB_PATH = "data/geoip/GeoLite2-City.mmdb"


def lookup_ip(ip):
    try:
        with geoip2.database.Reader(DB_PATH) as reader:
            response = reader.city(ip)
            return {
                "country": response.country.name,
                "city": response.city.name,
                "lat": response.location.latitude,
                "lon": response.location.longitude,
            }
    except Exception:
        return {
            "country": None,
            "city": None,
            "lat": None,
            "lon": None,
        }
