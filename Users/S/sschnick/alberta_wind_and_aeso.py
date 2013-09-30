import scraperwiki
import scraperwiki.sqlite as sql

sql.attach("aeso_current_supply_demand_report", "aeso")
sql.attach("alberta_wind_farms", "wind")

data = sql.select("aeso.swdata.name, wind.swdata.lat, wind.swdata.lon, aeso.swdata.mc, aeso.swdata.tng, wind.swdata.turbineType FROM aeso.swdata LEFT JOIN wind.swdata ON aeso.swdata.name = wind.swdata.name")

print data

sql.save(unique_keys=["name"], data=data)
import scraperwiki
import scraperwiki.sqlite as sql

sql.attach("aeso_current_supply_demand_report", "aeso")
sql.attach("alberta_wind_farms", "wind")

data = sql.select("aeso.swdata.name, wind.swdata.lat, wind.swdata.lon, aeso.swdata.mc, aeso.swdata.tng, wind.swdata.turbineType FROM aeso.swdata LEFT JOIN wind.swdata ON aeso.swdata.name = wind.swdata.name")

print data

sql.save(unique_keys=["name"], data=data)
