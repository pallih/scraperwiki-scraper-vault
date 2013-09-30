import scraperwiki
from BeautifulSoup import BeautifulSoup
from datetime import date
from datetime import timedelta

baseURL = "http://www.berlin.de/sen/umwelt/luftqualitaet/de/messnetz/tageswerte/download/"
observationNames = [
'',
'Partikel-PM10',
'Partikel-PM10',
'Ruß',
'Ruß',
'Stickstoffdioxid',
'Stickstoffdioxid',
'Benzol',
'Benzol',
'Kohlenmonoxid',
'Kohlenmonoxid',
'Ozon',
'Ozon',
'Schwefeldioxid',
'Schwefeldioxid']

observationIndicators = [
'',
'Tagesmittel',
'Anzahl der Überschreitungen/Jahr', 
'Tagesmittel', 
'Max. 3Std. wert', 
'Tagesmittel', 
'Max. 1Std. wert',
'Tagesmittel', 
'Max. 1Std. wert',
'Tagesmittel', 
'Max. gleitender 8-Std. Mittelw.', 
'Max. 1Std. wert',
'Max. gleitender 8-Std.- Mittelw.',
'Tagesmittel', 
'Max. 1Std. wert']

observationUnits = [u'','µg/m³','#','µg/m³','µg/m³','µg/m³','µg/m³','µg/m³','µg/m³','mg/m³','mg/m³','µg/m³','µg/m³','µg/m³','µg/m³']

def scrape_single_page(date):
    d = str(date).replace('-','')
    html = scraperwiki.scrape(baseURL+d+".html")
    html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    table = html.find('table', {'class': 'datenhellgrauklein'})
    rows = table.findAll('tr')
    for row in rows:
        i=0;
        cols = row.findAll('td', {'class': None})
        observation = None
        for col in cols:
            if i==0:
                observation = {}
                observation['station'] = col.text
            else:
                observation['name'] = observationNames[i]
                observation['indicator'] = observationIndicators[i]
                observation['unit'] = observationUnits[i]
                try:
                    observation['value'] = float(col.text)
                except ValueError:
                    observation['value'] = None
                observation['date'] = date
                scraperwiki.sqlite.save(unique_keys=['name','indicator','station','date'], data = observation,table_name="observations")
            i = i+1

if scraperwiki.sqlite.get_var('last_run') == None:
    scraperwiki.sqlite.save_var('last_run',date(2007,1,26).toordinal())
d = date.fromordinal(scraperwiki.sqlite.get_var('last_run'))
now = date.today()
while d<now:
    d = d+timedelta(days=1)
    try:
        scrape_single_page(d)
        scraperwiki.sqlite.save_var('last_run',d.toordinal())
    except:
        pass
    
import scraperwiki
from BeautifulSoup import BeautifulSoup
from datetime import date
from datetime import timedelta

baseURL = "http://www.berlin.de/sen/umwelt/luftqualitaet/de/messnetz/tageswerte/download/"
observationNames = [
'',
'Partikel-PM10',
'Partikel-PM10',
'Ruß',
'Ruß',
'Stickstoffdioxid',
'Stickstoffdioxid',
'Benzol',
'Benzol',
'Kohlenmonoxid',
'Kohlenmonoxid',
'Ozon',
'Ozon',
'Schwefeldioxid',
'Schwefeldioxid']

observationIndicators = [
'',
'Tagesmittel',
'Anzahl der Überschreitungen/Jahr', 
'Tagesmittel', 
'Max. 3Std. wert', 
'Tagesmittel', 
'Max. 1Std. wert',
'Tagesmittel', 
'Max. 1Std. wert',
'Tagesmittel', 
'Max. gleitender 8-Std. Mittelw.', 
'Max. 1Std. wert',
'Max. gleitender 8-Std.- Mittelw.',
'Tagesmittel', 
'Max. 1Std. wert']

observationUnits = [u'','µg/m³','#','µg/m³','µg/m³','µg/m³','µg/m³','µg/m³','µg/m³','mg/m³','mg/m³','µg/m³','µg/m³','µg/m³','µg/m³']

def scrape_single_page(date):
    d = str(date).replace('-','')
    html = scraperwiki.scrape(baseURL+d+".html")
    html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    table = html.find('table', {'class': 'datenhellgrauklein'})
    rows = table.findAll('tr')
    for row in rows:
        i=0;
        cols = row.findAll('td', {'class': None})
        observation = None
        for col in cols:
            if i==0:
                observation = {}
                observation['station'] = col.text
            else:
                observation['name'] = observationNames[i]
                observation['indicator'] = observationIndicators[i]
                observation['unit'] = observationUnits[i]
                try:
                    observation['value'] = float(col.text)
                except ValueError:
                    observation['value'] = None
                observation['date'] = date
                scraperwiki.sqlite.save(unique_keys=['name','indicator','station','date'], data = observation,table_name="observations")
            i = i+1

if scraperwiki.sqlite.get_var('last_run') == None:
    scraperwiki.sqlite.save_var('last_run',date(2007,1,26).toordinal())
d = date.fromordinal(scraperwiki.sqlite.get_var('last_run'))
now = date.today()
while d<now:
    d = d+timedelta(days=1)
    try:
        scrape_single_page(d)
        scraperwiki.sqlite.save_var('last_run',d.toordinal())
    except:
        pass
    
