import BeautifulSoup, scraperwiki, datetime

dataUrl = 'http://arxiv.org/list/nlin/07?show=1120'

html = scraperwiki.scrape(dataUrl)
soup = BeautifulSoup.BeautifulSoup(html)

articles = []


for id in soup.findAll('span', 'list-identifier'):
    article = {}
    if id.find(title='Abstract'):
        article['id'] = id.find(title='Abstract').string.replace('arXiv:', '').strip()
    articles.append(article)

print 'ids: ' + str(len(articles))

a = 0
for title in soup.findAll('div', 'list-title'):
    articles[a]['title'] = str(title.contents[2])
    a += 1

a = 0
for author in soup.findAll('div', 'list-authors'):
    text = ''
    for auth in author.findAll('a'):
        text += auth.string + ',' 
    articles[a]['author'] = text
    a += 1

#save
for article in articles:
    scraperwiki.sqlite.save(unique_keys=['id'], data=article)
import BeautifulSoup, scraperwiki, datetime

dataUrl = 'http://arxiv.org/list/nlin/07?show=1120'

html = scraperwiki.scrape(dataUrl)
soup = BeautifulSoup.BeautifulSoup(html)

articles = []


for id in soup.findAll('span', 'list-identifier'):
    article = {}
    if id.find(title='Abstract'):
        article['id'] = id.find(title='Abstract').string.replace('arXiv:', '').strip()
    articles.append(article)

print 'ids: ' + str(len(articles))

a = 0
for title in soup.findAll('div', 'list-title'):
    articles[a]['title'] = str(title.contents[2])
    a += 1

a = 0
for author in soup.findAll('div', 'list-authors'):
    text = ''
    for auth in author.findAll('a'):
        text += auth.string + ',' 
    articles[a]['author'] = text
    a += 1

#save
for article in articles:
    scraperwiki.sqlite.save(unique_keys=['id'], data=article)
