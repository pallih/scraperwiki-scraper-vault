import BeautifulSoup, scraperwiki

#scraperwiki.metadata.save('data_columns', ['name', 'code'])

colorsurl = 'http://www.graphviz.org/doc/info/colors.html'

html = scraperwiki.scrape(colorsurl)
soup = BeautifulSoup.BeautifulSoup(html)   
colors = []

for a in soup.findAll('a'):
    color['code'] = a['title']
    color['name'] = a.string
    colors.append(article)
    print color
    #scraperwiki.datastore.save(unique_keys=['link'], data=article)