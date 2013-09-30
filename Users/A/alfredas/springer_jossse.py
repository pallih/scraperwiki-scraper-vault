import BeautifulSoup, scraperwiki

scraperwiki.metadata.save('data_columns', ['link', 'volume', 'number', 'abstract'])

journalUrl = 'http://www.springerlink.com/content/1004-3756/'
baseUrl = 'http://www.springerlink.com'

items = []

for volumeNo in range(16, 20):
    
    for numberNo in range(1, 5):
        
        issueUrl = journalUrl + str(volumeNo) + "/" + str(numberNo)
        html = scraperwiki.scrape(issueUrl)
        soup = BeautifulSoup.BeautifulSoup(html)     

        for p in soup.findAll('p', 'title'):           
            aLink = p.find('a')

            article = {'link' : aLink['href']}

            article['volume'] = volumeNo
            article['number'] = numberNo
            items.append(article)
            print article

for article in items:
    link = baseUrl + article['link']
    try:
        html = scraperwiki.scrape(link)
        soup = BeautifulSoup.BeautifulSoup(html)    
    except:
        print 'Error reading ' + link
    else:
    
        for abs in soup.findAll('div', 'Abstract'):
            if len(abs.contents) > 1:
                absText = abs.contents[1]
                article['abstract'] = absText
                scraperwiki.datastore.save(unique_keys=['link'], data=article)
import BeautifulSoup, scraperwiki

scraperwiki.metadata.save('data_columns', ['link', 'volume', 'number', 'abstract'])

journalUrl = 'http://www.springerlink.com/content/1004-3756/'
baseUrl = 'http://www.springerlink.com'

items = []

for volumeNo in range(16, 20):
    
    for numberNo in range(1, 5):
        
        issueUrl = journalUrl + str(volumeNo) + "/" + str(numberNo)
        html = scraperwiki.scrape(issueUrl)
        soup = BeautifulSoup.BeautifulSoup(html)     

        for p in soup.findAll('p', 'title'):           
            aLink = p.find('a')

            article = {'link' : aLink['href']}

            article['volume'] = volumeNo
            article['number'] = numberNo
            items.append(article)
            print article

for article in items:
    link = baseUrl + article['link']
    try:
        html = scraperwiki.scrape(link)
        soup = BeautifulSoup.BeautifulSoup(html)    
    except:
        print 'Error reading ' + link
    else:
    
        for abs in soup.findAll('div', 'Abstract'):
            if len(abs.contents) > 1:
                absText = abs.contents[1]
                article['abstract'] = absText
                scraperwiki.datastore.save(unique_keys=['link'], data=article)
