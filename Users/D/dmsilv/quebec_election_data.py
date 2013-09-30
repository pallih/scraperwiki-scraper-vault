# -=- encoding: utf-8 -=-
import scraperwiki

#import lxml.html.soupparser
import lxml.html
import re

from urlparse import urljoin

#ELECTION_URL = 'http://www.electionsquebec.qc.ca/francais/provincial/resultats-electoraux/elections-generales.php?e=3&s=1&c=tous#s'
ELECTION_URL = 'http://infojdem.com/2012/pageElection/results2008.html'

CANDIDAT_REGX = re.compile(r'(.*)\s\((.+)\)', re.LOCALE)

partis = partis = {'P.Q.' : u'Parti québécois',
              'P.L.Q./Q.L.P.' : u'Parti libéral du Québec',
              u'A.D.Q./É.M.D.' : u'Action démocratique du Québec',
              'Q.S.' : u'Québec solidaire',
              'P.V.Q./G.P.Q.' : u'Parti vert du Québec',
              'P.I.' : u'Parti indépendantiste',
              'P.M.L.Q.' : u'Parti marxiste-léniniste du Québec',
              'P.D.Q.' : u'Parti démocrate du Québec',
              'P.R.Q.' : u'Parti république du Québec',
              'IND.' : u'Indépendant',
              'S.D.' : 'S.D.',
              }

def extract_details(candidat, match):
#    match = CANDIDAT_REGX.match(text)
    candidat['nom'] = match.group(1).strip()
    if partis.has_key(match.group(2)):
        candidat['parti'] = partis.get(match.group(2))


def is_to_add(myrange, value):
    if myrange.count(value):
        return True
    else:
        return False

def main():
    html = scraperwiki.scrape(ELECTION_URL)
    root = lxml.html.fromstring(html)
    circonscriptions = []
    circonscription = ''
    candidat = {}
    index = -1
    myrange = []
    tableau = root.cssselect('table.tableau')
    tableau = tableau[0][0]
    #print 'table:', tableau.tag
    for tr in tableau:
        for td in tr.getchildren():
            #print '--', td.tag, td.attrib
            if td.attrib.get('class') is not None:
                if len(td.getchildren()) > 0:
                    div = td.getchildren()
                    circonscription = div[0].tail
                else:
                    circonscription = td.text
                #circonscription['candidats'] = []
                    
            elif td.attrib.get('colspan') is None and td.tag == 'td':
                #print 'debug', td.tag, td.text
                if td.text is None: # dans le cas d'une balise strong
                    if len(td.getchildren()) > 0:
                        strong = td[0]    
                        match = CANDIDAT_REGX.match(strong.text)
                        extract_details(candidat, match)
                        myrange = range(0,3)
                        myrange.reverse()
                        index = myrange.pop()
                elif CANDIDAT_REGX.match(td.text) is not None:
                    match = CANDIDAT_REGX.match(td.text)
                    extract_details(candidat, match)
                    myrange = range(0,2)
                    myrange.reverse()
                    index = myrange.pop()
                elif index == 0:
                    #print 'Nombre de bulletins valides:', td.text
                    candidat['bulletins_valides'] = int(td.text.replace(' ',''))
                    index = myrange.pop()
                elif index == 1:
                    #print 'pourcentage:', td.text
                    candidat['pourcentage'] = td.text
                    if len(myrange) > 0:
                        index = myrange.pop()
                    else:
                        index = -1
                    
                elif index == 2:
                    #print 'majorite:', td.text
                    candidat['majorite'] = int(td.text.replace(' ',''))
                    index = -1
                else:
                    print 'rejeter:', td.text, type(td.text)
        if len(myrange) is 0 and candidat.get('pourcentage') is not None:
            #print candidat
            candidat['circonscription'] = circonscription
            scraperwiki.sqlite.save(unique_keys=['nom'], data=candidat)
            candidat = {}
                

main()
# -=- encoding: utf-8 -=-
import scraperwiki

#import lxml.html.soupparser
import lxml.html
import re

from urlparse import urljoin

#ELECTION_URL = 'http://www.electionsquebec.qc.ca/francais/provincial/resultats-electoraux/elections-generales.php?e=3&s=1&c=tous#s'
ELECTION_URL = 'http://infojdem.com/2012/pageElection/results2008.html'

CANDIDAT_REGX = re.compile(r'(.*)\s\((.+)\)', re.LOCALE)

partis = partis = {'P.Q.' : u'Parti québécois',
              'P.L.Q./Q.L.P.' : u'Parti libéral du Québec',
              u'A.D.Q./É.M.D.' : u'Action démocratique du Québec',
              'Q.S.' : u'Québec solidaire',
              'P.V.Q./G.P.Q.' : u'Parti vert du Québec',
              'P.I.' : u'Parti indépendantiste',
              'P.M.L.Q.' : u'Parti marxiste-léniniste du Québec',
              'P.D.Q.' : u'Parti démocrate du Québec',
              'P.R.Q.' : u'Parti république du Québec',
              'IND.' : u'Indépendant',
              'S.D.' : 'S.D.',
              }

def extract_details(candidat, match):
#    match = CANDIDAT_REGX.match(text)
    candidat['nom'] = match.group(1).strip()
    if partis.has_key(match.group(2)):
        candidat['parti'] = partis.get(match.group(2))


def is_to_add(myrange, value):
    if myrange.count(value):
        return True
    else:
        return False

def main():
    html = scraperwiki.scrape(ELECTION_URL)
    root = lxml.html.fromstring(html)
    circonscriptions = []
    circonscription = ''
    candidat = {}
    index = -1
    myrange = []
    tableau = root.cssselect('table.tableau')
    tableau = tableau[0][0]
    #print 'table:', tableau.tag
    for tr in tableau:
        for td in tr.getchildren():
            #print '--', td.tag, td.attrib
            if td.attrib.get('class') is not None:
                if len(td.getchildren()) > 0:
                    div = td.getchildren()
                    circonscription = div[0].tail
                else:
                    circonscription = td.text
                #circonscription['candidats'] = []
                    
            elif td.attrib.get('colspan') is None and td.tag == 'td':
                #print 'debug', td.tag, td.text
                if td.text is None: # dans le cas d'une balise strong
                    if len(td.getchildren()) > 0:
                        strong = td[0]    
                        match = CANDIDAT_REGX.match(strong.text)
                        extract_details(candidat, match)
                        myrange = range(0,3)
                        myrange.reverse()
                        index = myrange.pop()
                elif CANDIDAT_REGX.match(td.text) is not None:
                    match = CANDIDAT_REGX.match(td.text)
                    extract_details(candidat, match)
                    myrange = range(0,2)
                    myrange.reverse()
                    index = myrange.pop()
                elif index == 0:
                    #print 'Nombre de bulletins valides:', td.text
                    candidat['bulletins_valides'] = int(td.text.replace(' ',''))
                    index = myrange.pop()
                elif index == 1:
                    #print 'pourcentage:', td.text
                    candidat['pourcentage'] = td.text
                    if len(myrange) > 0:
                        index = myrange.pop()
                    else:
                        index = -1
                    
                elif index == 2:
                    #print 'majorite:', td.text
                    candidat['majorite'] = int(td.text.replace(' ',''))
                    index = -1
                else:
                    print 'rejeter:', td.text, type(td.text)
        if len(myrange) is 0 and candidat.get('pourcentage') is not None:
            #print candidat
            candidat['circonscription'] = circonscription
            scraperwiki.sqlite.save(unique_keys=['nom'], data=candidat)
            candidat = {}
                

main()
