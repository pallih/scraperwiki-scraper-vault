import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

# Hello World Example #

#scrape page
html = scraperwiki.scrape('http://www.bristol.gov.uk/ccm/content/Transport-Streets/Marine-waterway-services/Local-notices-to-mariners.en?page=2')
page = BeautifulSoup.BeautifulSoup(html)

for items in page.findAll('div', {'class': 'itemContent mpaContent'}):
    for item in items.findAll('p'):
        link = item.find('a')
        print link
        if link.get('name'):
            print 'break'
            break
        else:
            if link['href'][0] == '#':
                title = link.string
                number = page.find('a', {'name': link['href'][1:]}).parent.findNext('h2').contents[0]
                detail = page.find('a', {'name': link['href'][1:]}).parent.findNext('p').contents[0]
                
                print 'title:' +  title
                print 'number' + number
                print 'detail' + detail
                print '-----------------------------'
            #print detail
        #save to datastore
        data = {'message' : row.td.string,}
        datastore.save(unique_keys=['message'], data=data)




