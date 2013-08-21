import scraperwiki
import lxml.html
import dateutil.parser
import subprocess
import tempfile
import datetime
import os
from httplib import BadStatusLine
from urllib2 import URLError

DEFAULT_YEAR = 2012
DETERMINE_URI = 'http://www2.comune.rovereto.tn.it/iride/extra/cerca_determine/'
IMPEGNO_STR = 'provvedimento con impegno di spesa'
HTTP_RETRIES = 3

def getRowsBatch(anno, numero_dal='',numero_al='', oggetto='', servizio='TUTTI'):
    if numero_al and not anno:
        raise ValueError('Cannot fget by number if year is not defined')
    if numero_dal and not numero_al:
        # the selection by number doesn't work so well. It always
        # needs an upper closed interval, so let's use an extremely
        # high number as upper limit if it'ss not defined
        numero_al = '100000'
    params = dict(anno=anno, numero_dal=numero_dal, numero_al=numero_al, oggetto=oggetto,
                  servizio=servizio)
    # get the page
    html = scrape(DETERMINE_URI, params)
    # now parse it and get the links to the details
    root = lxml.html.fromstring(html)
    root.make_links_absolute(DETERMINE_URI)
    trs = root.cssselect('#tblgrid tr')
    details = []
    for tr in trs:
        if tr.find('td') is None:
            # jump over headers
            continue
        else:
            item = {}
            tds = tr.findall('td')
            for ix, td in enumerate(tds):
                if ix == 0:
                    link = td.iter('a').next()
                    item['uri'] = link.get('href')
                    item['numero'] = int(link.find('span').text.strip())
                    item['anno'] = int(link.find('font').text.strip())
                elif ix == 1:
                    item['sigla_dirigente'] = td.text.strip()
            details.append(item)
                    
    return details

def getNextBatch():
    last_year = scraperwiki.sqlite.get_var('anno', DEFAULT_YEAR)
    last_number = scraperwiki.sqlite.get_var('numero', '')
    return getRowsBatch(anno=last_year, numero_dal=last_number)
    

def parseDetail(uri):
    html = scrape(uri)
    root = lxml.html.fromstring(html.decode('utf-8'))
    root.make_links_absolute(DETERMINE_URI)
    data = {}
    tds = root.cssselect('table td')
    for ix, td in enumerate(tds):
        if ix == 1:
            data['dirigente'] = d = td.find('strong').text.strip()
        elif ix == 3:
            data['numero'] = int(td.find('b').text.strip())
        elif ix == 5:
            data['anno'] = int(td.find('b').text.strip())
        elif ix == 7:
            date = td.find('b').text.strip()
            data['data'] = dateutil.parser.parse(date, dayfirst=True).date()
        elif ix == 9:
            data['oggetto'] = td.find('b').text.strip()
        elif ix == 11:
            date = td.find('b').text.strip()
            data['data_esecutivita'] = dateutil.parser.parse(date, dayfirst=True).date()
        elif ix == 13:
            data['con_impegno'] = int(td.find('b').text.strip() == IMPEGNO_STR)
        elif ix == 15:
            allegati = []
            for li in td.iter('li'):
                # get always the second link which contains a title                
                link = li.findall('a')[1]
                if link.get('href').endswith('.pdf'):
                    allegati.append({'uri': link.get('href'), 'titolo': link.text.strip()})
            data['allegati'] = allegati
    return data

def dataExists(anno, numero):
    table = 'swdata'
    try:
        rows = scraperwiki.sqlite.execute("select anno, numero from %s where anno = ? and numero = ?" % table,
                                          (int(anno), int(numero)))
        return len(rows['data']) > 0
    except:
        # trap sqlite3.Error: no such table:
        return False

def getAttachment(uri):
    pdf = scrape(uri)
    name = ''
    with tempfile.NamedTemporaryFile() as f:
        f.write(pdf)
        f.flush()
        text = subprocess.check_output(['/usr/bin/pdftotext', '-layout', f.name, '-'])
        name = f.name
    # avoid filling up tmp space 
    if os.path.exists(name):
        os.remove(name)
    return text    

def scrape(*args, **kw):
    "Scrape and retry if known error"
    result = None
    last_error = None
    uri = args[0] if len(args) > 0 else kw['url']
    for i in range(HTTP_RETRIES):
        try:
            result = scraperwiki.scrape(*args, **kw)
            break
        except BadStatusLine as err:
            print "BadStatusLine while getting '%s' retry %d of %d" % (uri, i+1, HTTP_RETRIES)
            last_error = err
        except URLError as err:
            print "URLError while getting '%s' retry %d of %d" % (uri, i+1, HTTP_RETRIES)
            last_error = err
    if result is None and last_error is not None:
        raise last_error
    return result
    
def main():
    today = datetime.date.today()
    while True:
        last_year = scraperwiki.sqlite.get_var('anno', DEFAULT_YEAR)
        last_number = scraperwiki.sqlite.get_var('numero', '<inizio>')
        print "Searching for new items starting from number %s/%s" % (last_number, last_year)
        batch = getNextBatch()
        new_items = [i for i in batch if not dataExists(i['anno'], i['numero'])]
        if len(new_items) == 0:
            if today.year > last_year:
                scraperwiki.sqlite.save_var('anno', last_year + 1)
                scraperwiki.sqlite.save_var('numero', 1)
                continue
            else:
                break
        else:
            print "Preparing to save %s new items" % len(new_items)
            for i in new_items:
                data = parseDetail(i['uri'])
                data['sigla_dirigente'] = i['sigla_dirigente']
                data['uri'] = i['uri']
                data['importo'] = 0
                anno = data['anno']
                numero = data['numero']
                if len(data['allegati']) > 0:
                    for ix, a in enumerate(data['allegati']):
                        attachment = getAttachment(a['uri'])
                        scraperwiki.sqlite.save(('anno', 'numero', 'indice'), dict(anno=anno, numero=numero, testo=attachment,
                                                indice=ix, titolo=a['titolo'], uri=a['uri']), table_name='allegati')
                scraperwiki.sqlite.save(('anno', 'numero'), data)
                scraperwiki.sqlite.save_var('anno', anno)
                scraperwiki.sqlite.save_var('numero', numero)
                print "Saved determina number %s/%s" % (numero, anno)


try:
    main()
except scraperwiki.CPUTimeExceededError:
    print "Exiting due to exceeded time"


# d = parseDetail('http://www2.comune.rovereto.tn.it/iride/extra/determina_dettaglio/529740')
# print d
# import chardet
# print chardet.detect(d['dirigente'])

# details = getDetailsBatch(anno='2012')

# for det in details:
#    form = parseDetail(det['uri'])
#    form['sigla_dirigente'] = det['sigla_dirigente']
#    form['uri'] = det['uri']
#    print scraperwiki.sqlite.save(('anno', 'numero'), form)


#print getAttachment('http://www2.comune.rovereto.tn.it/iride/extra/scarica_file/allegato_iride_38003.pdf')
