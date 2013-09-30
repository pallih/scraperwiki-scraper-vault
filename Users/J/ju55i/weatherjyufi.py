import scraperwiki
from datetime import datetime

html = scraperwiki.scrape("http://weather.jyu.fi/")
source = html.split('\n') # The page is so broken that it doesn't make sense to use lxml
weather_data = {}
        
# Time
time_str = source[21][15:]
time = datetime.strptime(time_str, ("%H:%M:%S %d.%m.%Y"))
weather_data.update({"time":time})
        
# Temperature outside and wind chill
temp_out = float(source[24][22:-7])
wind_chill = float(source[25][11:-7])
weather_data.update({"temp_outside":temp_out,
                        "wind_chill":wind_chill})
        
# Wind speed and direction
wind_speed = float(source[28][11:16])
wind_speed_text = source[28][source[28].index("(")+1:source[28].index(")")]
wind_speed_highest = float(source[29][40:-8])
wind_direction = int(source[30][16:source[30].index("\xb0")])
wind_direction_text = source[30][source[30].index("(")+1:source[30].index(")")]
weather_data.update({"wind_speed":wind_speed,
                     "wind_speed_text":wind_speed_text,
                     "wind_speed_highest":wind_speed_highest,
                     "wind_direction":wind_direction,
                     "wind_direction_text":wind_direction_text})
                    
# Barrometric pressure and trend
bar_pressure = float(source[33][20:-8])
bar_trend = source[34][18:]
weather_data.update({"bar_pressure":bar_pressure,
                     "bar_trend":bar_trend})
        
# Temperature inside, humidity and vapor pressure
temp_inside = float(source[37][21:-6])
rel_hum_in = float(source[38][27:-5]) / 100
abs_hum = float(source[39][27:-32])
vapor_pressure = float(source[40][24:-8])
weather_data.update({"temp_inside":temp_inside,
                     "rel_hum_in":rel_hum_in,
                     "abs_hum":abs_hum,
                     "vapor_pressure":vapor_pressure})
        
scraperwiki.sqlite.save(unique_keys=['time'], data=weather_data)
import scraperwiki
from datetime import datetime

html = scraperwiki.scrape("http://weather.jyu.fi/")
source = html.split('\n') # The page is so broken that it doesn't make sense to use lxml
weather_data = {}
        
# Time
time_str = source[21][15:]
time = datetime.strptime(time_str, ("%H:%M:%S %d.%m.%Y"))
weather_data.update({"time":time})
        
# Temperature outside and wind chill
temp_out = float(source[24][22:-7])
wind_chill = float(source[25][11:-7])
weather_data.update({"temp_outside":temp_out,
                        "wind_chill":wind_chill})
        
# Wind speed and direction
wind_speed = float(source[28][11:16])
wind_speed_text = source[28][source[28].index("(")+1:source[28].index(")")]
wind_speed_highest = float(source[29][40:-8])
wind_direction = int(source[30][16:source[30].index("\xb0")])
wind_direction_text = source[30][source[30].index("(")+1:source[30].index(")")]
weather_data.update({"wind_speed":wind_speed,
                     "wind_speed_text":wind_speed_text,
                     "wind_speed_highest":wind_speed_highest,
                     "wind_direction":wind_direction,
                     "wind_direction_text":wind_direction_text})
                    
# Barrometric pressure and trend
bar_pressure = float(source[33][20:-8])
bar_trend = source[34][18:]
weather_data.update({"bar_pressure":bar_pressure,
                     "bar_trend":bar_trend})
        
# Temperature inside, humidity and vapor pressure
temp_inside = float(source[37][21:-6])
rel_hum_in = float(source[38][27:-5]) / 100
abs_hum = float(source[39][27:-32])
vapor_pressure = float(source[40][24:-8])
weather_data.update({"temp_inside":temp_inside,
                     "rel_hum_in":rel_hum_in,
                     "abs_hum":abs_hum,
                     "vapor_pressure":vapor_pressure})
        
scraperwiki.sqlite.save(unique_keys=['time'], data=weather_data)
