import scraperwiki
import time
import re
from BeautifulSoup import BeautifulSoup
import csv
import urlparse

base_url = 'http://www.fxstreet.com/news/forex-news/article.aspx?storyid='


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def ara():
    '''return a UNIX style timestamp representing now'''
    return int(time.time())


data = scraperwiki.scrape("https://dl.dropbox.com/s/ch0930nn1y8cjij/News2.csv?dl=1")
#print data

reader = csv.reader(data.splitlines(), quotechar='"', delimiter=';')


for row in reader:
    print row
    urlNoti = 'http://www.fxstreet.com/news/forex-news/article.aspx?storyid=' + row[0]
    print urlNoti
    #urlparse.urljoin('http://example.com/mypage', '?name=joe')
    #urlNoti = join('http://www.fxstreet.com/news/forex-news/article.aspx', noti)
    #print urlNoti
    html = scraperwiki.scrape(urlNoti)
    #print  '--->html:\n', html
    soup = BeautifulSoup(html)
    print '--->soup:\n', soup
    textNoti = soup.find('div', {'class': 'article-text'}).text
    print '--->textNoti:\n', textNoti
    #p = re.compile( 'TITOL*.*FITITOL')
    #textNotiNet = p.sub( '', 'textNoti')
    #print '--->textNotiNet:\n', textNotiNet
    #row['textNoti'] = textNoti
    camps = ['news', 'tipus', 'data', 'hora']
    colector = dict(zip(camps,row))

    colector['textNoti'] = textNoti
    colector['id'] = ara()
    
    #article = colector.str[id]
    #url = base_url + article
    #print url
    #html = scraperwiki.scrape(url)
    #print html


    scraperwiki.sqlite.save(['id'], colector, table_name="nov2012")

#data1 = csv.reader(data, delimiter='\t', quotechar='"')















#base_url = 'http://www.shortoftheweek.com/films/'

#starting_url = urlparse.urljoin(base_url, 'page/1/')
#scrape_and_look_for_next_link(base_url)