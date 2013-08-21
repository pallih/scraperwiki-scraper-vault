import scraperwiki
from itertools import count
from urlparse import urljoin
from pprint import pprint

# HTTP-Anfragen stellen:
import requests 

# HTML-Dokumente interpretieren:
from lxml import html

# Quell-URL:
BASE_URL = "http://ec.europa.eu/competition/elojade/isef/index.cfm"

# "count" gibt uns eine Seitenzahl:
for i in countyyyy():
    # "for" ist eine Schleife. Alle eingerueckten Anweisungen werden wiederholt.

    offset = (30 * i) + 1
    
    # Daten, die wir dem Server senden wollen:
    data = {
        'fuseaction': 'dsp_result',
        'sort': 'proc_code asc,proc_year asc,proc_nb asc',
        'fromrow': offset
        }

    # Eine HTTP-Anfrage stellen:
    response = requests.post(BASE_URL, data=data)

    # Das erhaltene HTML-Dokument interpretieren:
    document = html.fromstring(response.content)

    # Jede Zeile der Ergenis-Tabelle auswerten:
    for row in document.findall('.//table/tr'):
        case = row.find('./td[@class="case"]/a')

        # Enthaelt diese Zeile eine Fallbeschreibung?
        if case is None:
            continue
        
        # Ergebnisdaten sammeln:
        case_data = {
            'id': case.text,
            'title': row.find('./td[@class="tittle"]').text
            }
        
        # Detailinformationen anfragen:
        details_url = urljoin(BASE_URL, case.get('href'))
        details_response = requests.get(details_url)
        details_document = html.fragment_fromstring("<div>"+details_response.content+"</div>")
        
        # Detail-Daten zur Fallbeschreibung hinzufuegen:
        for detail in details_document.findall('.//table[@class="details"]/tr'):
            key, value = detail.findall("./td")
            key = key.text.strip(":").replace('(', '').replace(')', '').replace(' ', '_')
            case_data[key] = value.xpath('string()').strip()


        # Ergebnis speichern:
        scraperwiki.sqlite.save(unique_keys=['id'], data=case_data)
