import scraperwiki 
import datetime

start_year= 2012
now = datetime.datetime.now()

#Sydney Rainfall
year = start_year
while year <= now.year:
    web = 'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=' + str(year) + "&p_c=-872839501&p_stn_num=066062"
    month = 1
    day = -1
    city = "Sydney"
    html = scraperwiki.scrape(web)
    
    import lxml.html
    root = lxml.html.fromstring(html)
    
    
    for tr in root.cssselect("table[id='dataTable'] tr"):
        tds = tr.cssselect("td")
        if len(tds)==12:
            day= day+ 1
            if day>0:
                if month==13:
                    month=1
                for month in range(1,12):
                    if day<32 :
                        data = {
                            'Date' : str(year) + '-' + str(month) + '-' + str(day),
                            'Year' : year,
                            'Month' : month,
                            'Day' : day,
                            'rainfall' : tds[0].text_content(),
                            'City' : city,
                            'Key' : city + ' - ' + str(year) + '-' + str(month) + '-' + str(day)
                        }
                        scraperwiki.sqlite.save(unique_keys=['Key'], data=data)
                    month = month + 1
    year = year + 1



#Melbourne Rainfall
year = start_year

while year <= now.year:
    web = 'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=' + str(year) + "&p_c=-1481645340&p_stn_num=086071"
    month = 1
    day = -1
    city = "Melbourne"
    html = scraperwiki.scrape(web)
    
    import lxml.html
    root = lxml.html.fromstring(html)
    
    
    for tr in root.cssselect("table[id='dataTable'] tr"):
        tds = tr.cssselect("td")
        if len(tds)==12:
            day= day+ 1
            if day>0:
                if month==13:
                    month=1
                for month in range(1,12):
                    if day<32 :
                        data = {
                            'Date' : str(year) + '-' + str(month) + '-' + str(day),
                            'Year' : year,
                            'Month' : month,
                            'Day' : day,
                            'rainfall' : tds[0].text_content(),
                            'City' : city,
                            'Key' : city + ' - ' + str(year) + '-' + str(month) + '-' + str(day)
                        }
                        scraperwiki.sqlite.save(unique_keys=['Key'], data=data)
                    month = month + 1
    year = year + 1

#Brisbane Rainfall
year = start_year

while year <= now.year:
    web = 'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=' + str(year) + "&p_c=-334776646&p_stn_num=040913"
    month = 1
    day = -1
    city = "Brisbane"
    html = scraperwiki.scrape(web)
    
    import lxml.html
    root = lxml.html.fromstring(html)
    
    
    for tr in root.cssselect("table[id='dataTable'] tr"):
        tds = tr.cssselect("td")
        if len(tds)==12:
            day= day+ 1
            if day>0:
                if month==13:
                    month=1
                for month in range(1,12):
                    if day<32 :
                        data = {
                            'Date' : str(year) + '-' + str(month) + '-' + str(day),
                            'Year' : year,
                            'Month' : month,
                            'Day' : day,
                            'rainfall' : tds[0].text_content(),
                            'City' : city,
                            'Key' : city + ' - ' + str(year) + '-' + str(month) + '-' + str(day)
                        }
                        scraperwiki.sqlite.save(unique_keys=['Key'], data=data)
                    month = month + 1
    year = year + 1

#Perth Rainfall
year = start_year

while year <= now.year:
    web = 'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=' + str(year) + "&p_c=-17022057&p_stn_num=009225"
    month = 1
    day = -1
    city = "Perth"
    html = scraperwiki.scrape(web)
    
    import lxml.html
    root = lxml.html.fromstring(html)
    
    
    for tr in root.cssselect("table[id='dataTable'] tr"):
        tds = tr.cssselect("td")
        if len(tds)==12:
            day= day+ 1
            if day>0:
                if month==13:
                    month=1
                for month in range(1,12):
                    if day<32 :
                        data = {
                            'Date' : str(year) + '-' + str(month) + '-' + str(day),
                            'Year' : year,
                            'Month' : month,
                            'Day' : day,
                            'rainfall' : tds[0].text_content(),
                            'City' : city,
                            'Key' : city + ' - ' + str(year) + '-' + str(month) + '-' + str(day)
                        }
                        scraperwiki.sqlite.save(unique_keys=['Key'], data=data)
                    month = month + 1
    year = year + 1

#Adelaide Rainfall
year = start_year

while year <= now.year:
    web = 'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=' + str(year) + "&p_startYear=2013&p_c=-106317759&p_stn_num=023056"
    month = 1
    day = -1
    city = "Adelaide"
    html = scraperwiki.scrape(web)
    
    import lxml.html
    root = lxml.html.fromstring(html)
    
    
    for tr in root.cssselect("table[id='dataTable'] tr"):
        tds = tr.cssselect("td")
        if len(tds)==12:
            day= day+ 1
            if day>0:
                if month==13:
                    month=1
                for month in range(1,12):
                    if day<32 :
                        data = {
                            'Date' : str(year) + '-' + str(month) + '-' + str(day),
                            'Year' : year,
                            'Month' : month,
                            'Day' : day,
                            'rainfall' : tds[0].text_content(),
                            'City' : city,
                            'Key' : city + ' - ' + str(year) + '-' + str(month) + '-' + str(day)
                        }
                        scraperwiki.sqlite.save(unique_keys=['Key'], data=data)
                    month = month + 1
    year = year + 1

#Canberra Rainfall
year = start_year

while year <= now.year:
    web = 'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=' + str(year) + "&p_c=-986930134&p_stn_num=070247"
    month = 1
    day = -1
    city = "Canberra"
    html = scraperwiki.scrape(web)
    
    import lxml.html
    root = lxml.html.fromstring(html)
    
    
    for tr in root.cssselect("table[id='dataTable'] tr"):
        tds = tr.cssselect("td")
        if len(tds)==12:
            day= day+ 1
            if day>0:
                if month==13:
                    month=1
                for month in range(1,12):
                    if day<32 :
                        data = {
                            'Date' : str(year) + '-' + str(month) + '-' + str(day),
                            'Year' : year,
                            'Month' : month,
                            'Day' : day,
                            'rainfall' : tds[0].text_content(),
                            'City' : city,
                            'Key' : city + ' - ' + str(year) + '-' + str(month) + '-' + str(day)
                        }
                        scraperwiki.sqlite.save(unique_keys=['Key'], data=data)
                    month = month + 1
    year = year + 1

#Hobart Rainfall
year = start_year

while year <= now.year:
    web = 'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=' + str(year) + "&p_c=-1768292500&p_stn_num=094029"
    month = 1
    day = -1
    city = "Hobart"
    html = scraperwiki.scrape(web)
    
    import lxml.html
    root = lxml.html.fromstring(html)
    
    
    for tr in root.cssselect("table[id='dataTable'] tr"):
        tds = tr.cssselect("td")
        if len(tds)==12:
            day= day+ 1
            if day>0:
                if month==13:
                    month=1
                for month in range(1,12):
                    if day<32 :
                        data = {
                            'Date' : str(year) + '-' + str(month) + '-' + str(day),
                            'Year' : year,
                            'Month' : month,
                            'Day' : day,
                            'rainfall' : tds[0].text_content(),
                            'City' : city,
                            'Key' : city + ' - ' + str(year) + '-' + str(month) + '-' + str(day)
                        }
                        scraperwiki.sqlite.save(unique_keys=['Key'], data=data)
                    month = month + 1
    year = year + 1

#Darwin Rainfall
year = start_year

while year <= now.year:
    web = 'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=' + str(year) + "&p_c=-40142710&p_stn_num=014167"
    month = 1
    day = -1
    city = "Darwin"
    html = scraperwiki.scrape(web)
    
    import lxml.html
    root = lxml.html.fromstring(html)
    
    
    for tr in root.cssselect("table[id='dataTable'] tr"):
        tds = tr.cssselect("td")
        if len(tds)==12:
            day= day+ 1
            if day>0:
                if month==13:
                    month=1
                for month in range(1,12):
                    if day<32 :
                        data = {
                            'Date' : str(year) + '-' + str(month) + '-' + str(day),
                            'Year' : year,
                            'Month' : month,
                            'Day' : day,
                            'rainfall' : tds[0].text_content(),
                            'City' : city,
                            'Key' : city + ' - ' + str(year) + '-' + str(month) + '-' + str(day)
                        }
                        scraperwiki.sqlite.save(unique_keys=['Key'], data=data)
                    month = month + 1
    year = year + 1
