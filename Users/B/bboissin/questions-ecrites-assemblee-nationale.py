import scraperwiki
import urllib2, sys, os
import re
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup, NavigableString, Tag

from scraperwiki import datastore


# todo: erratum question / reponse
#start_url = 'http://recherche2.assemblee-nationale.fr/questions/resultats-questions.jsp?NumLegislature=13Questions&C1=QE&C2=QG&C3=QOSD&C4=RET&C5=AR&C6=SR&C7=NR'
# SortField=NAT&SortOrder=ASC&ResultCount=25
# NumLegislature=13Questions&ResultMaxDocs=500&C1=QE&C2=QG&C3=QOSD&C5=AR&C6=SR&C4=RET&C7=NR&T2=&S1=TEXTEINTEGRAL&AUT=&DEPT=&GROUPE=&RUB=&MINI=&MINA=&CRET=&T1=&Dates=DPQ&DATINF=01%2F02%2F2010&DATSUP=01%2F03%2F2010&DATEX=&Crit2=&T4=&Oper1=AND&Crit3=&T5=&Oper2=AND&Crit4=&T6=&SortField=NAT&SortOrder=ASC&ResultCount=25&format=HTML

def date2iso(s):
    d, m, y = s.split('/')
    return '-'.join((y, m, d))

_clean_html_re = re.compile("<.*?>")
def clean_html(s):
    return _clean_html_re.sub('', s)

lastbr_re = re.compile('\s*<br\s*/?>$', re.U|re.M)
def extracttext(t):
    div = t.parent.findNextSibling('div', attrs={'class': 'contenutexte'})
    text = div.renderContents(encoding=None).strip()
    return lastbr_re.sub('', text)

# extract information associated with a span
def extractspan(t):
    span = t.findNextSibling('span', attrs={'class': 'contenu'})
    return span.renderContents(encoding=None)

spandict = {
    'ministere_interroge': re.compile(u'^Minist\xe8re interrog\xe9 >'),
    'ministere_attribue': re.compile(u'^Minist\xe8re attributaire >'),
    'rubrique': re.compile(u'^Rubrique >'),
    'tete_analyse': re.compile(u"^T\xeate d'analyse >"),
    'analyse': re.compile(u'^Analyse >'),
}

def getspans(soup):
    for k, v in spandict.iteritems():
        yield k, extractspan(soup.find(text=v))

datedict = {
    u'Question publi\xe9e au JO le': (('date', 'date_question'),
                                      ('page', 'page_question')),
    u'Question retir\xe9e le': (('date', 'date_retrait'),
                                ('motif', 'motif_retrait')),
    u'R\xe9ponse publi\xe9e au JO le': (('date', 'date_reponse'),
                                        ('page', 'page_reponse')),
    u"Date de changement d'attribution": (('date', 'date_cht_attr'),),
    u'Date de signalement': (('date', 'date_signalement'),),
    u'Erratum de la r\xe9ponse publi\xe9 au JO le':
        (('date', 'date_erratum_reponse'),
         ('page', 'page_erratum_reponse')),
    u'Erratum de la question publi\xe9 au JO le':
        (('date', 'date_erratum_question'),
         ('page', 'page_erratum_question')),
}

date_re = re.compile(u'''(?P<type>[A-Z].*?)\s*:\s* # date type
                         (?P<date>\d+/\d+/\d+)\s* # date
                         (page\s*:\s*(?P<page>\d*))? # optional page number
                         (\(\s*(?P<motif>.*?)\s*\))? # optional motif
                                                     # (for retrait)
                         \s*''', re.U|re.M|re.X)

def extractdates(dates):
    for l in dates:
        if not l:
            continue
        for m in date_re.finditer(clean_html(l)):
            for k, v in datedict[m.group('type')]:
                value = m.group(k)
                if value is None:
                    value = ''
                if k == 'date':
                    value = date2iso(value)
                yield v, value

url = 'http://questions.assemblee-nationale.fr/q13/13-%sQE.htm'

fieldorder = (
    'source',
    'legislature',
    'type',
    'numero',
    'date_question',
    'date_retrait',
    'date_reponse',
    'date_signalement',
    'date_cht_attr',
    'page_question',
    'page_reponse',
    'ministere_attribue',
    'ministere_interroge',
    'tete_analyse',
    'analyse',
    'rubrique',
    'question',
    'reponse',
    'motif_retrait',
    'auteur',
)

def parseone(html):
    d = dict.fromkeys(fieldorder, '')

    # this is always the same currently
    d['legislature'] = '13'
    d['type'] = 'QE'

    s = BeautifulSoup(html, convertEntities=BeautifulStoneSoup.ALL_ENTITIES)

    # feed with information embedded in spans
    d.update(getspans(s))

    # extrait les dates / pages
    # split par lignes
    dates = s.find(text=re.compile(u'^Question publi\xe9e au JO le')).parent
    dates = dates.renderContents(encoding=None).split('<br />')

    # integre le deuxieme emplacement de retrait
    retrait = s.find(text=re.compile(u'^Question retir\xe9e le'))
    if retrait:
        try:
            span = extractspan(retrait)
        except:
            pass
        else:
            dates.append(u'%s %s' % (retrait, span))

    # get all dates / pages / motif
    d.update(extractdates(dates))

    # pour les questions au gvt, avec dates identiques
    if d['date_reponse'] and not d['date_question']:
        d['date_question'] = d['date_reponse']

    num = s.find(text=re.compile(u'^Question N\xb0 : '))
    d['numero'] = num.findNextSibling('b').renderContents(encoding=None)

    auteur = num.parent.findNextSibling('td').findNext('b').renderContents(encoding=None)
    preauteur = (u'M.\xa0', u'Mme\xa0', u'Mlle\xa0')
    for p in preauteur:
        if auteur.startswith(p):
            auteur = auteur[len(p):]
            break
    d['auteur'] = auteur.replace(u'\xa0', u' ')

    q = s.find(text=re.compile(u'^\s*Texte de la question\s*$'))
    d['question'] = extracttext(q)

    if d.get('date_reponse'):
        r = s.find(text=re.compile(u'^\s*Texte de la r\xe9ponse\s*$'))
        d['reponse'] = extracttext(r)

    d['source'] = url % d['numero']
    d['motif_retrait'] = d['motif_retrait'].lower()
    return d

for i in xrange(1, 1000):
    fn = '13-%dQE.htm' % i
    questionurl = 'http://questions.assemblee-nationale.fr/q13/' + os.path.basename(fn)

    html = scraperwiki.scrape(questionurl)
    data = parseone(html)
    datastore.save(unique_keys=['legislature', 'numero', 'type'], data=data)

