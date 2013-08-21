import scraperwiki
import datetime


#Sydney
city = "Sydney"
html = scraperwiki.scrape("http://www.bom.gov.au/nsw/forecasts/sydney.shtml")
cnt = 0
now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day
forcast = 0
while cnt<6 :
    start = html.find("/images/symbols/large/")
    html = html[start+22:]
    end = html.find(".png")
    descrip = html[:end]
    

    if cnt>0 :
        start = html.find('em class="max">')
        html = html[start+15:]
        end = html.find("</em>")
        forcast = html[:end]
    data = {
                                'Date' : str(year) + '-' + str(month) + '-' + str(day),
                                'Year' : year,
                                'Month' : month,
                                'Day' : day,
                                'Advance' : cnt,
                                'City' : city,
                                'Forcast' : forcast,
                                'Description' : descrip,
                                'Key' : city + '-' + str(cnt) + ' - ' + str(year) + '-' + str(month) + '-' + str(day)
                            }
    cnt = cnt + 1
    scraperwiki.sqlite.save(unique_keys=['Key'], data=data)


#Melbourne
city = "Melbourne"
html = scraperwiki.scrape("http://www.bom.gov.au/vic/forecasts/melbourne.shtml")
cnt = 0
now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day
forcast = 0
while cnt<5 :
    start = html.find("/images/symbols/large/")
    html = html[start+22:]
    end = html.find(".png")
    descrip = html[:end]
    

    if cnt>0 :
        start = html.find('em class="max">')
        html = html[start+15:]
        end = html.find("</em>")
        forcast = html[:end]
    data = {
                                'Date' : str(year) + '-' + str(month) + '-' + str(day),
                                'Year' : year,
                                'Month' : month,
                                'Day' : day,
                                'Advance' : cnt,
                                'City' : city,
                                'Forcast' : forcast,
                                'Description' : descrip,
                                'Key' : city + '-' + str(cnt) + ' - ' + str(year) + '-' + str(month) + '-' + str(day)
                            }
    cnt = cnt + 1
    scraperwiki.sqlite.save(unique_keys=['Key'], data=data)


#Brisbane
city = "Brisbane"
html = scraperwiki.scrape("http://www.bom.gov.au/vic/forecasts/melbourne.shtml")
cnt = 0
now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day
forcast = 0
while cnt<5 :
    start = html.find("/images/symbols/large/")
    if start>0:
        html = html[start+22:]
        end = html.find(".png")
        descrip = html[:end]
    

    if cnt>0 :
        start = html.find('em class="max">')
        html = html[start+15:]
        end = html.find("</em>")
        forcast = html[:end]
    data = {
                                'Date' : str(year) + '-' + str(month) + '-' + str(day),
                                'Year' : year,
                                'Month' : month,
                                'Day' : day,
                                'Advance' : cnt,
                                'City' : city,
                                'Forcast' : forcast,
                                'Description' : descrip,
                                'Key' : city + '-' + str(cnt) + ' - ' + str(year) + '-' + str(month) + '-' + str(day)
                            }
    cnt = cnt + 1
    
    scraperwiki.sqlite.save(unique_keys=['Key'], data=data)


#Perth
city = "Perth"
html = scraperwiki.scrape("http://www.bom.gov.au/wa/forecasts/perth.shtml")
cnt = 0
now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day
forcast = 0
while cnt<5 :
    start = html.find("/images/symbols/large/")
    if start>0:
        html = html[start+22:]
        end = html.find(".png")
        descrip = html[:end]
    

    if cnt>0 :
        start = html.find('em class="max">')
        html = html[start+15:]
        end = html.find("</em>")
        forcast = html[:end]
    data = {
                                'Date' : str(year) + '-' + str(month) + '-' + str(day),
                                'Year' : year,
                                'Month' : month,
                                'Day' : day,
                                'Advance' : cnt,
                                'City' : city,
                                'Forcast' : forcast,
                                'Description' : descrip,
                                'Key' : city + '-' + str(cnt) + ' - ' + str(year) + '-' + str(month) + '-' + str(day)
                            }
    cnt = cnt + 1

    scraperwiki.sqlite.save(unique_keys=['Key'], data=data)

#Adelaide
city = "Adelaide"
html = scraperwiki.scrape("http://www.bom.gov.au/sa/forecasts/adelaide.shtml")
cnt = 0
now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day
forcast = 0
while cnt<5 :
    start = html.find("/images/symbols/large/")
    if start>0:
        html = html[start+22:]
        end = html.find(".png")
        descrip = html[:end]
    

    if cnt>0 :
        start = html.find('em class="max">')
        html = html[start+15:]
        end = html.find("</em>")
        forcast = html[:end]
    data = {
                                'Date' : str(year) + '-' + str(month) + '-' + str(day),
                                'Year' : year,
                                'Month' : month,
                                'Day' : day,
                                'Advance' : cnt,
                                'City' : city,
                                'Forcast' : forcast,
                                'Description' : descrip,
                                'Key' : city + '-' + str(cnt) + ' - ' + str(year) + '-' + str(month) + '-' + str(day)
                            }
    cnt = cnt + 1

    scraperwiki.sqlite.save(unique_keys=['Key'], data=data)

#Hobart
city = "Hobart"
html = scraperwiki.scrape("http://www.bom.gov.au/tas/forecasts/hobart.shtml")
cnt = 0
now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day
forcast = 0
while cnt<5 :
    start = html.find("/images/symbols/large/")
    if start>0:
        html = html[start+22:]
        end = html.find(".png")
        descrip = html[:end]
    

    if cnt>0 :
        start = html.find('em class="max">')
        html = html[start+15:]
        end = html.find("</em>")
        forcast = html[:end]
    data = {
                                'Date' : str(year) + '-' + str(month) + '-' + str(day),
                                'Year' : year,
                                'Month' : month,
                                'Day' : day,
                                'Advance' : cnt,
                                'City' : city,
                                'Forcast' : forcast,
                                'Description' : descrip,
                                'Key' : city + '-' + str(cnt) + ' - ' + str(year) + '-' + str(month) + '-' + str(day)
                            }
    cnt = cnt + 1

    scraperwiki.sqlite.save(unique_keys=['Key'], data=data)

#Canberra
city = "Canberra"
html = scraperwiki.scrape("http://www.bom.gov.au/act/forecasts/canberra.shtml")
cnt = 0
now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day
forcast = 0
while cnt<5 :
    start = html.find("/images/symbols/large/")
    if start>0:
        html = html[start+22:]
        end = html.find(".png")
        descrip = html[:end]
    

    if cnt>0 :
        start = html.find('em class="max">')
        html = html[start+15:]
        end = html.find("</em>")
        forcast = html[:end]
    data = {
                                'Date' : str(year) + '-' + str(month) + '-' + str(day),
                                'Year' : year,
                                'Month' : month,
                                'Day' : day,
                                'Advance' : cnt,
                                'City' : city,
                                'Forcast' : forcast,
                                'Description' : descrip,
                                'Key' : city + '-' + str(cnt) + ' - ' + str(year) + '-' + str(month) + '-' + str(day)
                            }
    cnt = cnt + 1

    scraperwiki.sqlite.save(unique_keys=['Key'], data=data)



