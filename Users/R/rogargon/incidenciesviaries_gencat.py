import scraperwiki
import BeautifulSoup
import re

def trim(v):
    p = re.compile('^\s*(.*?)\s*$')
    m = p.match(str(v))
    if m:
        return m.group(1)
    else:
        return str(v)

url = "http://www10.gencat.cat/pls/cit/p101.llista_pub?sw=1&v_tipus=0&v_tipus=2&v_tipus=3&v_tipus=4&v_tipus=5&v_tipus=6&v_ordre=1&v_pais=C&v_pro=0&v_com=0"

# Retencions: v_tipus=2
# Obres: v_tipus=3
# Cons: v_tipus=4
# Metereologia: v_tipus=5
# Ports: v_tipus=6
# Ordre: v_ordre=1 (Carretera) 2 (Comarca) 3 (Població)
# País: v_pais=C (Catalunya)
# Demarcació: v_pro=0 (Total Catalunya)
# Comarca: v_com=0 (Totes)

html = scraperwiki.scrape(url)
soup = BeautifulSoup.BeautifulSoup(html)

afectacions = soup.find(id='FW_tAfectacions')

# Capçaleres: Tipus, Causes i observacions, Nivell d'afectació, Ctra., Km inicial, Km final, Sentit, Cap a, Població, Demarcació, Data hora inicial
thead = afectacions.find('thead')
tbody = afectacions.find('tbody')

for tr in tbody.findAll('tr'):
    data = {}
    data['type'] = trim(tr.contents[1].string)
    data['cause'] = trim(tr.contents[3].string)
    data['level'] = trim(tr.contents[5].string)
    data['road'] = trim(tr.contents[7].string)
    data['start_km'] = trim(tr.contents[9].string)
    data['end_km'] = trim(tr.contents[11].string)
    data['direction'] = trim(tr.contents[13].string)
    data['heading'] = trim(tr.contents[15].string)
    data['city'] = trim(tr.contents[17].string)
    data['district'] = trim(tr.contents[19].string)
    data['date-time'] = trim(tr.contents[21].string)

    print data

    #crufts_date = datetime.datetime(2003, 8, 4, 12, 30, 45)

    scraperwiki.sqlite.save(['date-time','road','start_km','end_km','direction','heading'], data)
import scraperwiki
import BeautifulSoup
import re

def trim(v):
    p = re.compile('^\s*(.*?)\s*$')
    m = p.match(str(v))
    if m:
        return m.group(1)
    else:
        return str(v)

url = "http://www10.gencat.cat/pls/cit/p101.llista_pub?sw=1&v_tipus=0&v_tipus=2&v_tipus=3&v_tipus=4&v_tipus=5&v_tipus=6&v_ordre=1&v_pais=C&v_pro=0&v_com=0"

# Retencions: v_tipus=2
# Obres: v_tipus=3
# Cons: v_tipus=4
# Metereologia: v_tipus=5
# Ports: v_tipus=6
# Ordre: v_ordre=1 (Carretera) 2 (Comarca) 3 (Població)
# País: v_pais=C (Catalunya)
# Demarcació: v_pro=0 (Total Catalunya)
# Comarca: v_com=0 (Totes)

html = scraperwiki.scrape(url)
soup = BeautifulSoup.BeautifulSoup(html)

afectacions = soup.find(id='FW_tAfectacions')

# Capçaleres: Tipus, Causes i observacions, Nivell d'afectació, Ctra., Km inicial, Km final, Sentit, Cap a, Població, Demarcació, Data hora inicial
thead = afectacions.find('thead')
tbody = afectacions.find('tbody')

for tr in tbody.findAll('tr'):
    data = {}
    data['type'] = trim(tr.contents[1].string)
    data['cause'] = trim(tr.contents[3].string)
    data['level'] = trim(tr.contents[5].string)
    data['road'] = trim(tr.contents[7].string)
    data['start_km'] = trim(tr.contents[9].string)
    data['end_km'] = trim(tr.contents[11].string)
    data['direction'] = trim(tr.contents[13].string)
    data['heading'] = trim(tr.contents[15].string)
    data['city'] = trim(tr.contents[17].string)
    data['district'] = trim(tr.contents[19].string)
    data['date-time'] = trim(tr.contents[21].string)

    print data

    #crufts_date = datetime.datetime(2003, 8, 4, 12, 30, 45)

    scraperwiki.sqlite.save(['date-time','road','start_km','end_km','direction','heading'], data)
