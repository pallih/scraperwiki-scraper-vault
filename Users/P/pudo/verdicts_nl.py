import scraperwiki
from urllib import urlopen, urlencode
from lxml import html
from pprint import pprint

# Blank Python

TOPICS = ["Handelszaak", "Faillissement", "Civiel overig", "Straf", "Belasting", "Ambtenarenrecht",
          "Bijstandszaken", "Bouwen", "Sociale zekerheid", "Vreemdelingen", "Bestuursrecht overig",
          "Personen-en familierecht"]

#for each topic of law:
for topic in TOPICS:
    doc = html.parse("http://zoeken.rechtspraak.nl/default.aspx")
    inputs = doc.findall('//input')
    selects = doc.findall('//select')
    request = [(i.get('name'), i.get('value', '').encode('utf-8')) for i in inputs]
    request.append(('ctl00$ContentPlaceHolder1$BistroSearchUitspraakControl$ddlRechtsgebieden', topic))
    data = urlopen("http://zoeken.rechtspraak.nl/default.aspx", urlencode(request))
    print data.read()
    #doc = html.parse(data)
    
    #pprint(dict([(i.get('name'), s.find('option[@selected]')) for i in selects]))
#    do a search with that topic set
#    for page in the result set:
#        i want to get a list of all links on that
#        for each link:
#            fetch the case data
#            turn the case data into structured information
#            save it