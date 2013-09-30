import scraperwiki

from bs4 import BeautifulSoup

import urllib

url = "http://www.radiobremen.de/nachrichten/wetter/wettermesswerte100.html"   

fh = urllib.urlopen(url)
# read website
html = fh.read()
soup = BeautifulSoup(html)


def get_weather_summary():

    entry = {}
    divs = soup.select('.right')
    if divs:
        date_and_time = divs[0].text.split(',')
        if len(date_and_time) > 1:

            date, time = date_and_time
            entry['datum'] = date.strip()
            entry['Uhrzeit'] = time.strip()
        else:
            return
    else:
        print "Could not parse date and time!"
        return

    divs = soup.select('.rubrik')
    if divs:
        divs = [i for i in divs if 'Wetter in' in i.text]
        if divs:
            p_before = divs[0]
            p = p_before.find_next()           
            entry['wetter_kurz'] = p.text.replace('Mehr...', '')

        else:
            return
    else:
        return

    scraperwiki.sqlite.save(unique_keys=['datum'], data=entry, table_name="wetter_bremen_kurz")

def get_regional_data():

    entry = {}
    divs = soup.select('.right')
    if divs:
        date_and_time = divs[0].text.split(',')
        if len(date_and_time) > 1:

            date, time = date_and_time
        
            entry['Datum'] = date.strip()
            entry['Uhrzeit'] = time.strip()
        else: 
            return 
    else:
        print "Could not parse date and time!"
        return

    tables = soup.select('.data')
    reg_table = tables[0]
    orte = []

    for rows in reg_table.find_all('tr'):
        
        field1 = rows.td
        if field1: 
            ort = field1.text
            entry['Ort'] = ort
            if "berechneter" in ort:
                continue
        else: 
            continue 
        field2 = field1.find_next()
        if field2: 
            entry['Temperatur'] = field2.text

        else:
            continue 
        field3 = field2.find_next()
        if field3:
            img = field3.findChild()
            print img
            description = img.get('alt')
            print description
            entry['Beschreibung'] = description        

        else:
            continue 
        print entry
        scraperwiki.sqlite.save(unique_keys=['Datum'], data=entry, table_name="Wetter in " + ort)

            


## main ##
get_weather_summary()
get_regional_data()      
import scraperwiki

from bs4 import BeautifulSoup

import urllib

url = "http://www.radiobremen.de/nachrichten/wetter/wettermesswerte100.html"   

fh = urllib.urlopen(url)
# read website
html = fh.read()
soup = BeautifulSoup(html)


def get_weather_summary():

    entry = {}
    divs = soup.select('.right')
    if divs:
        date_and_time = divs[0].text.split(',')
        if len(date_and_time) > 1:

            date, time = date_and_time
            entry['datum'] = date.strip()
            entry['Uhrzeit'] = time.strip()
        else:
            return
    else:
        print "Could not parse date and time!"
        return

    divs = soup.select('.rubrik')
    if divs:
        divs = [i for i in divs if 'Wetter in' in i.text]
        if divs:
            p_before = divs[0]
            p = p_before.find_next()           
            entry['wetter_kurz'] = p.text.replace('Mehr...', '')

        else:
            return
    else:
        return

    scraperwiki.sqlite.save(unique_keys=['datum'], data=entry, table_name="wetter_bremen_kurz")

def get_regional_data():

    entry = {}
    divs = soup.select('.right')
    if divs:
        date_and_time = divs[0].text.split(',')
        if len(date_and_time) > 1:

            date, time = date_and_time
        
            entry['Datum'] = date.strip()
            entry['Uhrzeit'] = time.strip()
        else: 
            return 
    else:
        print "Could not parse date and time!"
        return

    tables = soup.select('.data')
    reg_table = tables[0]
    orte = []

    for rows in reg_table.find_all('tr'):
        
        field1 = rows.td
        if field1: 
            ort = field1.text
            entry['Ort'] = ort
            if "berechneter" in ort:
                continue
        else: 
            continue 
        field2 = field1.find_next()
        if field2: 
            entry['Temperatur'] = field2.text

        else:
            continue 
        field3 = field2.find_next()
        if field3:
            img = field3.findChild()
            print img
            description = img.get('alt')
            print description
            entry['Beschreibung'] = description        

        else:
            continue 
        print entry
        scraperwiki.sqlite.save(unique_keys=['Datum'], data=entry, table_name="Wetter in " + ort)

            


## main ##
get_weather_summary()
get_regional_data()      
