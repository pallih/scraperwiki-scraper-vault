from lxml import html
import urllib2
import urlparse
import scraperwiki

ROOT = "https://isir.justice.cz/InsSpravci/public/seznamFiltr.do"
OSOBA = "https://isir.justice.cz/InsSpravci/public/detailVerObchSpol.jsp?osoba=3715"
# ROOT = "https://isir.justice.cz/InsSpravci/public/seznamAction.do?setName=seznam&path=/public/seznamAction.do&scroll=34&size=10&lastSize=10"
PAGING_TABLE = 5
DATA_TABLE  = 3

def download(url):
    handle = urllib2.urlopen(url)
    data = unicode(handle.read(), "windows-1250")
    tree = html.fromstring(data)
    handle.close()
    return tree
    
def parse_osoba(url):
    print "OSOBA: %s" % url

    tree = download(url)
    tables = tree.cssselect('table')
    
    table = tables[3]
    # for i, row in enumerate(table.cssselect('tr')):
    #     print "%d: %s" % (i, row.text_content())

    record = {}

    for inp in table.cssselect('input'):
        key = inp.attrib["name"]
        value = inp.attrib["value"]
        record[key] = value

    record["url"] = url
    return record
        
def parse_page(url):
    print "PARSING: %s" % url
    
    tree = download(url)
    tables = tree.cssselect('table')

    table = tables[PAGING_TABLE]
    pages = table.cssselect("a")

    for table in tables[DATA_TABLE]:
        for row in table.cssselect('tr'):
            cells = row.cssselect('td')
            if not len(cells):
                continue
            osoba_url = cells[2].cssselect("a")[0].attrib["href"]
            # print "NAME: %s" % cells[0].text_content()
            # print "ADDR: %s" % cells[1].text_content()
            # print "URL : %s" % cells[2].cssselect("a")[0].attrib["href"]
            
            osoba_url = urlparse.urljoin(url, osoba_url)
            record = parse_osoba(osoba_url)
            
            scraperwiki.datastore.save(["url"], record)
            # output.append(record)
            # print record.keys()


    next_page = None
    for page in pages:
        if unicode(page.text_content()).startswith("dal"):
            next_page = page
    if next_page is not None:
        next_page_url = next_page.attrib["href"]
    else:
        next_page_url = None

    if next_page_url:
        next_page_url = urlparse.urljoin(url, next_page_url)
    # print "NEXT WILL BE: %s" % next_page_url
    return next_page_url


scraperwiki.metadata.save( "data_columns", 
                [
                 'jmeno', 'prijmeni', 'titulPred', 'titulZa',
                 'rodneCislo', 'datumNarozeni', 'nazev',
                 'ulice_S', 'cp_S', 'mesto_S', 'psc_S', 'okres_S', 'ico', 
                 'ulice_TP', 'cp_TP', 'okres_TP',
                 'predesleNazvy', 
                 'denVzniku', 'denZaniku', 
                 'duvodZaniku', 'denPozastaveni',  'duvodPozastaveni',  
                 'dosVzdelani', 'url'
                ]
        )

next_url = ROOT
while next_url:
    next_url = parse_page(next_url)

