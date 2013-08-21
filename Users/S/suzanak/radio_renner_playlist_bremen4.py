import scraperwiki
import urllib 
from bs4 import BeautifulSoup


url = 'http://www.radiobremen.de/bremenvier/musik/playlists/radiorenner104.html'
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
    datum = datum.replace('Radio Renner mit Tim Renner vom ', '')

  else: 
    print "Datum nicht gefunden"
    return 

  for row in tr[1:]:

    entry = {}
    entry['Datum'] = datum 
    feld1 = row.find_next('td', 'top44_table_zelle')
    feld2 = feld1.find_next_sibling()
    if feld2:
        interpret = feld2.text
        entry['Interpret'] = interpret 
    feld3 = feld2.find_next_sibling()
    if feld3:
        titel = feld3.text 
        entry['Titel'] = titel 
        entry['ID'] = interpret + " - " + titel
        
        scraperwiki.sqlite.save(unique_keys=['ID'], data=entry, table_name="Playlist Radio Renner Bremen4")

    else:
        print "Titel nicht gefunden"

## MAIN ## 
scrape_playlist()


