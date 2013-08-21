import scraperwiki
import urllib
from bs4 import BeautifulSoup

url = 'http://www.radiobremen.de/bremenvier/musik/playlists/topviervier100.html'

# webseite oeffnen
fh = urllib.urlopen(url)
# webseite einlesen
html = fh.read()
soup = BeautifulSoup(html)

def scrape_playlist():

  tab = soup.select('.top44_table')
  if tab:
    tr = tab[0].find_all('tr')
  else:
    print "Tabelle nicht gefunden"
    return

  if not tr:
    print "Tabellenzeilen nicht gefunden"
    return

  headlines =  soup.find_all('h2')
  if headlines:
    datum = headlines[0].text
    datum = datum.replace('Die 44 besten Songs vom ', '')
    datum = datum.strip().replace('"', '')

  else:
    print "Datum nicht gefunden"
    return

  for row in tr[1:]:

    entry = {}
    entry['Datum'] = datum
    feld1 = row.find_next('td', 'top44_table_zelle')
    if feld1:
        entry['Platzierung'] = feld1.text

    feld2 = feld1.find_next_sibling()
    if feld2: 
        entry['Vorwoche'] = feld2.text
    feld3 = feld2.find_next_sibling()
    if feld3:
        interpret = feld3.text
        entry['Interpret'] = interpret
    feld4 = feld3.find_next_sibling()    
    if feld4:
        titel = feld4.text
        entry['Titel'] = titel
    
    if interpret and titel:
        id = datum + "-" + interpret + "-" + titel  
        entry['id'] = id
        scraperwiki.sqlite.save(unique_keys=['id'], data=entry, table_name="Playlist Top44 Bremen4")

## MAIN ##
scrape_playlist()



