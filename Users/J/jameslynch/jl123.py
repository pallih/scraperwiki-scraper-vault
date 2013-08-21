import scraperwiki
from BeautifulSoup import BeautifulSoup

baseUrl = 'http://www.att.com'

masterlist = ['7700008','2800006','800349','7800011','1900004']

def scrapeSupportTopicsList(homeUrl):
    homeHtml = scraperwiki.scrape(homeUrl)
    homeUrlSoup = BeautifulSoup(homeHtml)
    lis = homeUrlSoup.find('ul', attrs={ 'class' : 'tree-default tree-esupport' }).findAll('li')
    for li in lis:
        print li['id'] + ' ' + li['class']
        if li['class'] != 'closed':
            scrapeQuestionList(li['id'])
            # print 'closed!!'
            #scrapeMenu(li['id'])
        #else:
            # scrapeQuestionList(li['id'])
            # print 'open!!'

def scrapeQuestionList(lid):
    qUrl = baseUrl + '/esupport/main/middleColumn.jsp?ct=' + lid + '&pv=2&rpp=300&sv=1'
    qHtml = scraperwiki.scrape(qUrl)
    qSoup = BeautifulSoup(qHtml)
    divs = qSoup.findAll('div', attrs={ 'class' : 'desclft'} )
    for div in divs:
        print div.input['value'] + ' - ' + div.a['href']

def scrapeMenu(lid):
    menuUrl = baseUrl + '/esupport/main.jsp?cv=820&ct=' + lid
    menuHtml = scraperwiki.scrape(menuUrl)
    menuSoup = BeautifulSoup(menuHtml)
    subs = menuSoup.find('li', attrs={ 'class' : 'open' }).find('ul').findAll('li')
    for sub in subs:
        print sub['id']

# anchor = li.find('a')
# print anchor.text + ": " + anchor['href']
# scrapeTopic(baseUrl + anchor['href'])

#def scrapeTopic(anchor.text, topic, topicUrl):
#    topicHtml = scraperwiki.scrape(topicUrl)

#def scrapeTopicIds(homeUrl):
#    homeHtml = scraperwiki.scrape(homeUrl)
#    homeUrlSoup = BeautifulSoup(homeHtml)
#    listItems = homeUrlSoup.findAll('li', attrs={ 'class' : 'leaf' })
#    for l in listItems :
#        idStr = l['id']
#        print 'id: ' + idStr


scrapeSupportTopicsList(baseUrl + '/esupport/main.jsp?cv=820')

# scrapeTopic('Account', baseUrl + '/esupport/main.jsp?pv=2&br=BR&ct=800349&cv=820')