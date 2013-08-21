import scraperwiki
from bs4 import BeautifulSoup
import re
import requests
import traceback

MAX_PAGE = 995

def tagtext(element, sep =' ', strip=False, nocr=False):
    """
    Remove the html tags from a BeautifulSoup element,
    and return the text
    strip: whether to pass the text through 'strip' before returning it
    False: do not strip (default)
    True:  strip with standard strip() function
    [string]: pass the string to the strip() function, e.g. to remove particular characters
    sep: string to use when re-joining blocks of text
    """
    def dostrip(item):
        if not strip:
            return item
        elif strip is True:
            return item.strip()
        elif isinstance(strip, unicode) or isinstance(strip, str):
            return item.strip(strip)
        else:
            raise ValueError(
                "tagtext recieved an invalid argument for strip \
                - should be True, or unicode/string")
    items = []
    if not element:
        return ""
    if isinstance(element, unicode) or isinstance(element, str):
        return dostrip(element)
    for x in element.recursiveChildGenerator():
        if not isinstance(x, unicode):
            continue
        items.append(dostrip(x))
    if nocr:
        items = filter(lambda i: i != '\n', items)
    text = sep.join(items)
    return text

pdf_baseurl = 'http://www.csm1909.ro/csm/'

def details_from_page(pagetext):
    results = []
    soup = BeautifulSoup(pagetext)
    label = soup.find('center', text = re.compile('Rezultate:.*'))
    maintable = label.findNext('table')
    for row in maintable.findChildren('tr')[1:]:
        if row.parent != maintable:
            # I am not sure why this happens, but it does
            continue
        cells = [tagtext(x) for x in row.findAll('td')]
        try:
            rowdata = {
            'numar': cells[0],
            'data_hotarare': cells[1],
            'tip': cells[2],
            'categorie': cells[3],
            'referitor': cells[4],
            'data_publicare': cells[5],
            'download_url': pdf_baseurl + row.find('a')['href']}
            scraperwiki.sqlite.save(unique_keys = ['numar', 'data_hotarare'], data = rowdata)
            results.append(rowdata)
        except Exception:
          traceback.print_exc()
          print(row)
          continue
    return results

def iterate_pages():
    # there are 993 pages
    url = 'http://www.csm1909.ro/csm/index.php?cmd=0301'
    pagenum = scraperwiki.sqlite.get_var('csm_pagenum', 1)
    while pagenum < MAX_PAGE:
        try:
            postdata ={'pg' : pagenum}
            r = requests.post(url, postdata).text
            details_from_page(r)
            print('done page %s' % pagenum)
            pagenum += 1
            scraperwiki.sqlite.save_var('csm_pagenum', pagenum)
        except scraperwiki.CPUTimeExceededError:
            print('out of CPU')
            break
        
    #'tip_hotarare=&categorie=&numar=&dh_zi=&dh_luna=&dh_an=&camp=&pg_l=1&pg=2;

iterate_pages()