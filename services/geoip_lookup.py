import geoip2.database

DB_PATH = "data/geoip/GeoLite2-City.mmdb"

reader = geoip2.database.Reader(DB_PATH)

def lookup_ip(ip):
    try:
        response = reader.city(ip)
        return {
            "country": response.country.name,
            "city": response.city.name,
            "latitude": response.location.latitude,
            "longitude": response.location.longitude
        }
    except Exception:
        return {
            "country": "Unknown",
            "city": "Unknown",
            "latitude": None,
            "longitude": None
        }
