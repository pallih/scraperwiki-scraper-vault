import GeoIP

gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
print gi.country_code_by_addr("74.125.39.106")

