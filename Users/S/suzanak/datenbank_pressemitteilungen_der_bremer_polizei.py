import scraperwiki
from bs4 import BeautifulSoup
import urllib
import re


def make_soup(url):
    fh = urllib.urlopen(url)
    # read website
    html = fh.read()
    soup = BeautifulSoup(html)
    return soup


def get_press_releases(soup):

    dates = soup.select('.date')
    link = dates[0].find_next()
    if not link:
        return
    url = link.get('href')
    if '#' in url:
        url = url.split('#')[0]
    soup2 = make_soup(url)
    headlines = soup2.find_all('h2')
    for h in headlines:
        print h
        entry = {}
        entry['Headline'] = h.text
        ps = h.find_next_siblings('p')
        if len(ps) < 3:
            continue
        date = ps[1].text
        date = re.sub("\)|\(", '', date)
        entry['Datum'] = date

        description = ps[2].text
        # this website is awful! 
        pnext = ps[2].find_next()
        while pnext:
            if pnext.name == 'h2':
                break
            if pnext.name == 'p':
                description += '\n' + pnext.text 
            pnext = pnext.find_next()

        entry['Beschreibung'] = description
        entry['id'] = date + " " + entry['Headline'][:20] + "..."
        print entry
        scraperwiki.sqlite.save(unique_keys=['id'], data=entry, table_name="Pressemitteilungen der Bremer Polizei")
        
## main ## 
#url = "http://www.polizei.bremen.de/sixcms/detail.php?gsid=bremen09.c.4435.de"   
url = "http://www.polizei.bremen.de/sixcms/detail.php?gsid=bremen09.c.5034.de"

soup = make_soup(url)
get_press_releases(soup)



