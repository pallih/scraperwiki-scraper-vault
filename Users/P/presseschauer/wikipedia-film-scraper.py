import scraperwiki
import re
from BeautifulSoup import BeautifulSoup, Tag

import urllib2
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

year = '2011'
category = 'Category:'+year+' films'
base_url = 'http://en.wikipedia.org'
next_url = 'http://en.wikipedia.org/wiki/Category:'+year+'_films'
infile = opener.open(next_url)
cat_html = infile.read()

while cat_html != None:
    films = BeautifulSoup(cat_html).find("div",{ "id" :  "mw-pages"})
    for link in films.findAll('a'):
        if link.attrs[0][0] != 'name':
            if link.attrs[0][1].find("Wikipedia:FAQ") < 0 and link.attrs[0][1].find('films_of_'+year) < 0 and link.attrs[0][1].find(''+year+'_in_film') < 0:
                url = 'http://en.wikipedia.org'+link.attrs[0][1]
                print url
                html = opener.open(url).read()
                html = html.replace("<br",",<br")
                html = re.sub("\[.*\]","",html)
                table = BeautifulSoup(html).find("table", { "class" : "infobox vevent" })
                if table != None:
                    data = {}
                    data["Url"] = url
                    data["Year"] = year
                    for row in table.findAll('tr'):
                        hth = ""
                        th = row.findAll("th")
                        if th:
                            hth = th[0].text.replace("(","").replace(")","").replace(".","").replace("&"," ").replace(";"," ").replace("#"," ")
                        td = row.findAll("td")
                        if td and hth != '': 
                            data[hth] = td[0].text
                    scraperwiki.sqlite.save(["Url"], data)
    nexts = BeautifulSoup(cat_html).findAll("a",{ "title" :  category})
    cat_html = None        
    for links in BeautifulSoup(str(nexts)).findAll('a'):
        if links.text == 'next 200':
            next_url = links.attrs[0][1]
            infile = opener.open(base_url + next_url)
            cat_html = infile.read()
                  


