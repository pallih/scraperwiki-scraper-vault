import scraperwiki
import re
import string
import lxml.html
import json
from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
import urllib2
import datetime
import time
import uuid
random_string = str(uuid.uuid4())
num = 0
#modifications
#first iteration create table
#second iteration comment out create table
#further iterations comment out updatecategory()

#scraperwiki.sqlite.execute("create table wikitable (th string,formula string, proof string, roc string)")

#scraperwiki.sqlite.execute("CREATE TABLE wikitables3 (id text,formula text,roc text,th text,proof text)")

def get_html(title):
    raw_json = scraperwiki.scrape("http://en.wikipedia.org/w/api.php?action=parse&format=json&page=" + title)
    html = json.loads(raw_json)['parse']['text']['*']
    print html

    return html
soup = BeautifulSoup(get_html('Z-transform'))
soup.prettify().encode('utf8')        
for table in soup.find_all("table", "wikitable"):
    print(table.find('caption'))
    for row in table.find_all('tr'):
        cells = []
        alt1=''
        alt2=''
        for th in row.find_all('th'):
            if th is not None:
                title = th.string
            else:
                for img in th.find_all('img'):
                   if img is not None:
                       print img['alt']
                       title=th.string
                else:
                    cells.append(cell.text_content())
        for cell in row.find_all('td'):
            num=0
            for img in cell.find_all('img'):
                if img is not None:
                    if num is not 2:
                        num+=1
                        if 'R' or 'ROC' in img['alt']:
                            alt2 = img['alt']
                        elif '=' in img['alt']:
                            alt1 = img['alt']
                        else:
                            alt1=' & '
                            alt2=' & '
                    else:
                        num=0
                else:
                    cells.append(cell.text_content())
            num+=1
        scraperwiki.sqlite.save([{'id':random_string}],{'id': random_string,'formula': alt1,'roc': title,'th': alt2,'proof': alt1},'wikitables3')
        print(' & '.join(cells))

"""
import scraperwiki

import lxml.html
import json
import urllib
index = 'http://en.wikipedia.org/w/api.php?action=parse&format=json&page=List_of_Occupy_movement_protest_locations_in_the_United_States';
print 'Scraping ' + index + '...'
raw_json = scraperwiki.scrape(index)
print raw_json
python_json = json.loads(raw_json)
html = python_json['parse']['text']['*']

print 'Extracting HTML...'
print html
"""
