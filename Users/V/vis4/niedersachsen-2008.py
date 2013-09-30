# encoding: utf-8

import scraperwiki
import requests
from bs4 import BeautifulSoup

# Scraper für die Wahlergebnisse der Landtagswahl in Niedersachsen 2013

# Hoffen wir mal die Wahlergebnisseiten der Wahlkreise sehen so aus wie
# hier: http://www.nls.niedersachsen.de/LW2008/023.htm :)

base_url = "http://www.aktuelle-wahlen-niedersachsen.de/LW2013/"

# zum testen scrapen wir mal die alten wahlergebnisse
base_url = "http://www.nls.niedersachsen.de/LW2008/"

election = "08"

base_wk_url = base_url + "%03d.html"

wk_ids = range(1, 88)

def get_int(s):
    s = s.strip()
    if s == '-' or s == '':
        return 0
    try:
        return int(s.replace('.', ''))
    except:
        print s
        print "Error"
        return 0

keys = {
    'Christlich Demokratische Union Deutschlands': 'CDU',
    'Sozialdemokratische Partei Deutschlands': 'SPD',
    'Freie Demokratische Partei': 'FDP',
    u'BÜNDNIS 90/DIE GRÜNEN': 'GRUENE',
    'DIE LINKE. Landesverband Niedersachsen': 'LINKE',
    'DIE REPUBLIKANER': 'REP',
    'Nationaldemokratische Partei Deutschlands': 'NPD',
    'Mensch Umwelt Tierschutz': 'MUT',
    u'Ökologisch-Demokratische Partei': 'OEDP',
    u'Gültige Stimmen': 'valid',
    u'Ungültige Stimmen': 'invalid',
    u'Ab jetzt...Bündnis für Deutschland, Partei für Demokratie durch Volksabstimmung': 'ABJETZT',
    'Demokratische Alternative': 'DA',
    'Die Friesen': 'FRIESEN',
    'DIE GRAUEN - Graue Panther': 'GRAUE',
    'Familien-Partei Deutschlands': 'FAMILIE',
    u'Freie Wähler Niedersachsen - Bürgerinitiativen, Bürgerlisten und unabhängige Wählergemeinschaften': 'FW',
    'Partei Bibeltreuer Christen': 'CHRISTEN',
    'Sonstige 2)': 'others',
}

for id in wk_ids:
    wk_url = base_wk_url % id
    r = requests.get(wk_url)
    soup = BeautifulSoup(r.text)
    rows = soup.find_all("tr")
    
    # Die erste Zeile enthält den Namen des Wahlkreises
    wk_name = rows[0].td.text.replace("Wahlkreis: ", "").strip()

    wk_id, wk_name = wk_name.split(" ", 1)
    try:
        wk_id = int(wk_id)
    except:
        print "Fehler!"
    if int(wk_id) == id:
        # Prima: Wahlkreisnummer stimmt mit der URL überein!
        print 'id:', wk_id, 'name:', wk_name

        # Direkt gewählt:
        direkt = rows[1].find_all('td')[1].text.strip()
        #print 'Direkt gewählt:', direkt
        
        # Wahlberechtigte
        voters = get_int(rows[5].find_all('td')[1].text)
        #print 'Wahlberechtigte:', voters
        
        # Wähler
        votes = get_int(rows[6].find_all('td')[1].text)
        #print 'Wählerinnen/Wähler:', votes

        # Wahlbeteiligung
        turnout = float(votes) / voters
        #print 'Wahlbeteiligung:', round(turnout*100,1), '%'

        def get_vote(r):
            cols1 = rows[r].find_all('td')
            cols2 = rows[r+1].find_all('td')
            party = cols1[0].b.text.strip()
            if party in keys:
                party = keys[party]
            else:
                print 'ignoring unknown party', party
                return (None, 0, 0)
            # Erststimmen
            v1 = get_int(cols1[1].text)
            # Zweitstimmen
            v2 = get_int(cols2[0].text)
            return (party, v1, v2)
        
        wk_data = dict(id=id, name=wk_name, year=election, voters=voters, votes=votes, turnout=round(turnout,3), winner=direkt)

        for r in range(8, len(rows)-2, 2):
            party, v1, v2 = get_vote(r)
            if party:
                wk_data[party+'-1'] = v1
                wk_data[party+'-2'] = v2

        # Ergebnis speichern
        scraperwiki.sqlite.save(unique_keys=['id', 'year'], data=wk_data)  
         


    


# encoding: utf-8

import scraperwiki
import requests
from bs4 import BeautifulSoup

# Scraper für die Wahlergebnisse der Landtagswahl in Niedersachsen 2013

# Hoffen wir mal die Wahlergebnisseiten der Wahlkreise sehen so aus wie
# hier: http://www.nls.niedersachsen.de/LW2008/023.htm :)

base_url = "http://www.aktuelle-wahlen-niedersachsen.de/LW2013/"

# zum testen scrapen wir mal die alten wahlergebnisse
base_url = "http://www.nls.niedersachsen.de/LW2008/"

election = "08"

base_wk_url = base_url + "%03d.html"

wk_ids = range(1, 88)

def get_int(s):
    s = s.strip()
    if s == '-' or s == '':
        return 0
    try:
        return int(s.replace('.', ''))
    except:
        print s
        print "Error"
        return 0

keys = {
    'Christlich Demokratische Union Deutschlands': 'CDU',
    'Sozialdemokratische Partei Deutschlands': 'SPD',
    'Freie Demokratische Partei': 'FDP',
    u'BÜNDNIS 90/DIE GRÜNEN': 'GRUENE',
    'DIE LINKE. Landesverband Niedersachsen': 'LINKE',
    'DIE REPUBLIKANER': 'REP',
    'Nationaldemokratische Partei Deutschlands': 'NPD',
    'Mensch Umwelt Tierschutz': 'MUT',
    u'Ökologisch-Demokratische Partei': 'OEDP',
    u'Gültige Stimmen': 'valid',
    u'Ungültige Stimmen': 'invalid',
    u'Ab jetzt...Bündnis für Deutschland, Partei für Demokratie durch Volksabstimmung': 'ABJETZT',
    'Demokratische Alternative': 'DA',
    'Die Friesen': 'FRIESEN',
    'DIE GRAUEN - Graue Panther': 'GRAUE',
    'Familien-Partei Deutschlands': 'FAMILIE',
    u'Freie Wähler Niedersachsen - Bürgerinitiativen, Bürgerlisten und unabhängige Wählergemeinschaften': 'FW',
    'Partei Bibeltreuer Christen': 'CHRISTEN',
    'Sonstige 2)': 'others',
}

for id in wk_ids:
    wk_url = base_wk_url % id
    r = requests.get(wk_url)
    soup = BeautifulSoup(r.text)
    rows = soup.find_all("tr")
    
    # Die erste Zeile enthält den Namen des Wahlkreises
    wk_name = rows[0].td.text.replace("Wahlkreis: ", "").strip()

    wk_id, wk_name = wk_name.split(" ", 1)
    try:
        wk_id = int(wk_id)
    except:
        print "Fehler!"
    if int(wk_id) == id:
        # Prima: Wahlkreisnummer stimmt mit der URL überein!
        print 'id:', wk_id, 'name:', wk_name

        # Direkt gewählt:
        direkt = rows[1].find_all('td')[1].text.strip()
        #print 'Direkt gewählt:', direkt
        
        # Wahlberechtigte
        voters = get_int(rows[5].find_all('td')[1].text)
        #print 'Wahlberechtigte:', voters
        
        # Wähler
        votes = get_int(rows[6].find_all('td')[1].text)
        #print 'Wählerinnen/Wähler:', votes

        # Wahlbeteiligung
        turnout = float(votes) / voters
        #print 'Wahlbeteiligung:', round(turnout*100,1), '%'

        def get_vote(r):
            cols1 = rows[r].find_all('td')
            cols2 = rows[r+1].find_all('td')
            party = cols1[0].b.text.strip()
            if party in keys:
                party = keys[party]
            else:
                print 'ignoring unknown party', party
                return (None, 0, 0)
            # Erststimmen
            v1 = get_int(cols1[1].text)
            # Zweitstimmen
            v2 = get_int(cols2[0].text)
            return (party, v1, v2)
        
        wk_data = dict(id=id, name=wk_name, year=election, voters=voters, votes=votes, turnout=round(turnout,3), winner=direkt)

        for r in range(8, len(rows)-2, 2):
            party, v1, v2 = get_vote(r)
            if party:
                wk_data[party+'-1'] = v1
                wk_data[party+'-2'] = v2

        # Ergebnis speichern
        scraperwiki.sqlite.save(unique_keys=['id', 'year'], data=wk_data)  
         


    


