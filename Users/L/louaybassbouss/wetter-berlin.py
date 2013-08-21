# http://www.wetter-berlin-online.de/j2003.htm --> http://www.wetter-berlin-online.de/j2011.htm

import scraperwiki
from BeautifulSoup import BeautifulSoup
from datetime import date
from datetime import datetime
from datetime import timedelta

baseURL = "http://www.wetter-berlin-online.de/"
observationNames = []
station = 'Berlin'

def scrape_single_page(d):
    html = scraperwiki.scrape(baseURL+'j'+str(d.year)+".htm")
    html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    table = html.findAll('table')[1]
    headers = table.find('tr').findAll('th')
    for header in headers:
        j = 1
        name = header.text
        try:
            j = int(header['colspan'])
        except:
            j=1
        while j>0:
            observationNames.append(name)
            j = j-1

    rows = table.findAll('tr')
    d1 = d
    for row in rows:
        i=0;
        cols = row.findAll('td')
        
        for col in cols:
            if i==0:
                try:
                    d1 = datetime.strptime(col.text, "%d.%m.%Y").date()
                    if d1 <= d:
                        continue
                except:
                    continue
            else:
                observation = {}
                observation['name'] = observationNames[i]
                observation['station'] = station
                observation['date'] = d1
                br = col.find('br')
                line = None
                if br == None:
                    observation['indicator'] = 'Avg.'
                    observation['time'] = None
                    line = col.text
                else:
                    split = br.previousSibling.split(' ')
                    observation['indicator'] = split[0]
                    observation['time'] = split[1]
                    line = br.nextSibling
                split = line.split(' ')
                if len(split) == 1:
                    observation['value']= split[0]
                else:
                    observation['value']= float(split[0].replace(',','.'))
                    observation['unit']= split[1]

                print observation
                scraperwiki.sqlite.save(unique_keys=['name','indicator','station','date'], data = observation,table_name="observations")
            i = i+1
    if d1 < d:
        d1 = d
    return d1+timedelta(days=1)

if scraperwiki.sqlite.get_var('last_run') == None:
    scraperwiki.sqlite.save_var('last_run',date(2003,1,1).toordinal())
d = date.fromordinal(scraperwiki.sqlite.get_var('last_run'))
now = date.today()

while d<now:
    try:
        d = scrape_single_page(d)
        scraperwiki.sqlite.save_var('last_run',d.toordinal())
    except:
         pass