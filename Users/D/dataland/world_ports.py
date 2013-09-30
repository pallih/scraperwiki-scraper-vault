import scraperwiki
import lxml.html
import urllib
import datetime

base_url = "http://www.worldportsource.com/countries.php"
ctry_base_url = "http://www.worldportsource.com"

html = scraperwiki.scrape(base_url)
root = lxml.html.fromstring(html)
for count, tr in enumerate(root.cssselect('tr')):
    row = [td.text_content() for td in tr.cssselect('td')]
    if len(row)==3:
        for ahref in tr.cssselect('a'):
            detailink = ahref.attrib['href']
            ctry_final_url = ctry_base_url + detailink
            html2 = scraperwiki.scrape(ctry_final_url)
            root2 = lxml.html.fromstring(html2)
            for count, tr in enumerate(root2.cssselect('tr')):
                for td in tr.cssselect('td'):
                    for ahref in td.cssselect('a'):
                        d = ahref.attrib
                        if d.get('href',0) != 0:
                            portlink = ahref.attrib['href']
                            if portlink[:6] == "/ports":
                                portdetail_url = ctry_base_url + portlink
                                html3 = scraperwiki.scrape(portdetail_url)
                                root3 = lxml.html.fromstring(html3)
                                for count, tr in enumerate(root3.cssselect('tr')):
                                    row = [td.text_content() for td in tr.cssselect('td')]
                                    if len(row)==2 and row[0] != '':
                                        print rowimport scraperwiki
import lxml.html
import urllib
import datetime

base_url = "http://www.worldportsource.com/countries.php"
ctry_base_url = "http://www.worldportsource.com"

html = scraperwiki.scrape(base_url)
root = lxml.html.fromstring(html)
for count, tr in enumerate(root.cssselect('tr')):
    row = [td.text_content() for td in tr.cssselect('td')]
    if len(row)==3:
        for ahref in tr.cssselect('a'):
            detailink = ahref.attrib['href']
            ctry_final_url = ctry_base_url + detailink
            html2 = scraperwiki.scrape(ctry_final_url)
            root2 = lxml.html.fromstring(html2)
            for count, tr in enumerate(root2.cssselect('tr')):
                for td in tr.cssselect('td'):
                    for ahref in td.cssselect('a'):
                        d = ahref.attrib
                        if d.get('href',0) != 0:
                            portlink = ahref.attrib['href']
                            if portlink[:6] == "/ports":
                                portdetail_url = ctry_base_url + portlink
                                html3 = scraperwiki.scrape(portdetail_url)
                                root3 = lxml.html.fromstring(html3)
                                for count, tr in enumerate(root3.cssselect('tr')):
                                    row = [td.text_content() for td in tr.cssselect('td')]
                                    if len(row)==2 and row[0] != '':
                                        print row