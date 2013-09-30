# ALL REGISTERED ICELANDIC AIRCRAFTS, WITH INFO - from: http://loftfaraskra.caa.is/home/


import scraperwiki,re
from BeautifulSoup import BeautifulSoup

starturl = 'http://loftfaraskra.caa.is/home/'

def scrape_aircraft_list(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    soup.prettify()

    link = soup.findAll('a')
    for a in link:
        url = a['href']
        if re.search('detail.php',url):
            url = "http://loftfaraskra.caa.is/home/" + url
            seen_before = scraperwiki.sqlite.get_var(url)
            if seen_before is not None:
                pass
                print "Seen before - skip: " + url
            else:
                scrape_aircraft(url)
    
def scrape_aircraft(url):
    aircraft = {}
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    soup.prettify()
    br = soup.findAll('br')
    for br in br:
        br.replaceWith(', ')

    #First table
    table = soup.find('table', {'class' : 'craft' })

    registration_id = table.findNext('tr')
    aircraft['registration_id'] = re.sub("Einkennisstafir:","",registration_id.text)
    registration_nr = registration_id.findNext('tr')
    aircraft['registration_nr'] = re.sub('Skr\xe1ningarn\xfamer:',"",registration_nr.text)
    registration_id = re.sub("Einkennisstafir:","",registration_id.text)
    
    #Second table
    table = table.findNext('table', {'class' : 'craft' })
    make = table.findNext('tr')
    aircraft['make'] = re.sub("Tegund:","",make.text)
    production_year = make.findNext('tr')
    aircraft['production_year'] = re.sub("Framlei\xf0slu\xe1r:","",production_year.text)    
    serial_nr = production_year.findNext('tr')
    aircraft['serial_nr'] = re.sub("Ra\xf0n\xfamer:","",serial_nr.text)    
    
    #Third table
    table = table.findNext('table', {'class' : 'craft' })
    max_weight = table.findNext('tr')
    aircraft['max_weight'] = re.sub("H\xe1marks\xfeungi:","",max_weight.text)
    passenger_nr = max_weight.findNext('tr')
    passenger_nr = re.sub('Far\xfeegafj\xf6ldi:',"",passenger_nr.text)
    if passenger_nr == u"Ekki skr\xe1\xf0ur":
        passenger_nr = "n/a"
    aircraft['passenger_nr'] = passenger_nr

    #Fourth table
    table = table.findNext('table', {'class' : 'craft' })
    owner = table.findNext('tr')
    aircraft['owner'] = re.sub("Eigandi:","",owner.text)
    address = owner.findNext('tr')
    address = address.findNext('td')
    address = address.findNext('td')
    aircraft['owner_address'] = address.text

    #Fifth table
    table = table.findNext('table', {'class' : 'craft' })
    operator = table.findNext('tr')
    aircraft['operator'] = re.sub("Umr\xe1\xf0andi:","",operator.text)
    address = operator.findNext('tr')
    address = address.findNext('td')
    address = address.findNext('td')
    aircraft['operator_address'] = address.text
    scraperwiki.datastore.save(["registration_id"], aircraft)
    scraperwiki.metadata.save(url, '1')

    print aircraft

        

scrape_aircraft_list(starturl)
# ALL REGISTERED ICELANDIC AIRCRAFTS, WITH INFO - from: http://loftfaraskra.caa.is/home/


import scraperwiki,re
from BeautifulSoup import BeautifulSoup

starturl = 'http://loftfaraskra.caa.is/home/'

def scrape_aircraft_list(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    soup.prettify()

    link = soup.findAll('a')
    for a in link:
        url = a['href']
        if re.search('detail.php',url):
            url = "http://loftfaraskra.caa.is/home/" + url
            seen_before = scraperwiki.sqlite.get_var(url)
            if seen_before is not None:
                pass
                print "Seen before - skip: " + url
            else:
                scrape_aircraft(url)
    
def scrape_aircraft(url):
    aircraft = {}
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    soup.prettify()
    br = soup.findAll('br')
    for br in br:
        br.replaceWith(', ')

    #First table
    table = soup.find('table', {'class' : 'craft' })

    registration_id = table.findNext('tr')
    aircraft['registration_id'] = re.sub("Einkennisstafir:","",registration_id.text)
    registration_nr = registration_id.findNext('tr')
    aircraft['registration_nr'] = re.sub('Skr\xe1ningarn\xfamer:',"",registration_nr.text)
    registration_id = re.sub("Einkennisstafir:","",registration_id.text)
    
    #Second table
    table = table.findNext('table', {'class' : 'craft' })
    make = table.findNext('tr')
    aircraft['make'] = re.sub("Tegund:","",make.text)
    production_year = make.findNext('tr')
    aircraft['production_year'] = re.sub("Framlei\xf0slu\xe1r:","",production_year.text)    
    serial_nr = production_year.findNext('tr')
    aircraft['serial_nr'] = re.sub("Ra\xf0n\xfamer:","",serial_nr.text)    
    
    #Third table
    table = table.findNext('table', {'class' : 'craft' })
    max_weight = table.findNext('tr')
    aircraft['max_weight'] = re.sub("H\xe1marks\xfeungi:","",max_weight.text)
    passenger_nr = max_weight.findNext('tr')
    passenger_nr = re.sub('Far\xfeegafj\xf6ldi:',"",passenger_nr.text)
    if passenger_nr == u"Ekki skr\xe1\xf0ur":
        passenger_nr = "n/a"
    aircraft['passenger_nr'] = passenger_nr

    #Fourth table
    table = table.findNext('table', {'class' : 'craft' })
    owner = table.findNext('tr')
    aircraft['owner'] = re.sub("Eigandi:","",owner.text)
    address = owner.findNext('tr')
    address = address.findNext('td')
    address = address.findNext('td')
    aircraft['owner_address'] = address.text

    #Fifth table
    table = table.findNext('table', {'class' : 'craft' })
    operator = table.findNext('tr')
    aircraft['operator'] = re.sub("Umr\xe1\xf0andi:","",operator.text)
    address = operator.findNext('tr')
    address = address.findNext('td')
    address = address.findNext('td')
    aircraft['operator_address'] = address.text
    scraperwiki.datastore.save(["registration_id"], aircraft)
    scraperwiki.metadata.save(url, '1')

    print aircraft

        

scrape_aircraft_list(starturl)
