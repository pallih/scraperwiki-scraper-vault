import scraperwiki

from bs4 import BeautifulSoup

import urllib

url_tea = "http://www.freebase.com/search?limit=50&start=0&query=tea"
url_earl = "http://www.freebase.com/search?limit=50&start=0&query=earl+grey"
url_cup = "http://www.freebase.com/search?limit=50&start=0&query=cup"
urls = [url_tea, url_earl, url_cup]

def get_hypernyms():

    summary = []
    id = 1
    for url in urls:
        # open url
        fh = urllib.urlopen(url)
        # read website
        html = fh.read()
        soup = BeautifulSoup(html)
    
        hypernym_results = soup.select(".result-list")
    
        for li in hypernym_results:
            i = iter(soup.select(".result-item-title"))
            hypernyms = li.select(".result-item-types")
            
            # create dictionary entries containing name of synonym and relating hypernyms
            for span in hypernyms:
                synonym = i.next().text
                filter = span.text.split(',')
                for s in filter:
                    three_tuple = {}
                    three_tuple['id'] = id
                    three_tuple['object 1'] = synonym
                    three_tuple['relation'] = "has hypernym"
                    three_tuple['object 2'] = s
                    id += 1
                    summary.append(three_tuple)
    
        scraperwiki.sqlite.save(unique_keys=['id'], data=summary, table_name="hyperynms")

get_hypernyms()
