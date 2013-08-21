import scraperwiki
import os
import csv
# Blank Python
years = range(2000,2012)

headers = ['ICT',
 'Max_TemperatureC',
 'Mean_TemperatureC',
 'Min_TemperatureC',
 'Dew_PointC',
 'MeanDew_PointC',
 'Min_DewpointC',
 'Max_Humidity',
 'Mean_Humidity',
 'Min_Humidity',
 'Max_Sea_Level_PressurehPa',
 'Mean_Sea_Level_PressurehPa',
 'Min_Sea_Level_PressurehPa',
 'Max_VisibilityKm',
 'Mean_VisibilityKm',
 'Min_VisibilitykM',
 'Max_Wind_SpeedKm_h',
 'Mean_Wind_SpeedKm_h',
 'Max_Gust_SpeedKm_h',
 'Precipitationmm',
 'CloudCover',
 'Events',
 'WindDirDegrees']
cities = ['VVNB','VVTS','VLVT','VTBD','VDPP']
for city in cities:
    for year in years:
        url = "http://www.wunderground.com/history/airport/{city}/{year}/1/1/CustomHistory.html?dayend=31&monthend=12&yearend={year}&req_city=NA&req_state=NA&req_statename=NA&format=2".format(year=year,city=city)
        data = scraperwiki.scrape(url)
        data_clean = data.rstrip().split("<br />")
        #print url
        for item in data_clean[1:]:
            row = dict(zip(headers,item.split(",")))
            row['city']=city
            scraperwiki.sqlite.save(unique_keys=["city","ICT"],data = row)
    
    