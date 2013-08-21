import scraperwiki
import lxml.html
from datetime import datetime,timedelta
import re

BASE='http://www.librarything.com'
URL=BASE+'/topic/151746'

PATTERN=re.compile('.*?(\d{2,4}).*?')


def main():
    today = datetime.today()
    yesterday=today-timedelta(1)
    year=str(today.year)

    url = URL

    while url:
        print 'Processing ',url
        html = scraperwiki.scrape(url)
        page = lxml.html.fromstring(html)
        nextprev = page.cssselect('div.continuation p')
        if nextprev:
            previous = nextprev[0]
            prevurl = previous.cssselect('a')[0].get('href')
            url = BASE+prevurl
        else:
            url = None

        if len(nextprev)>1:
            next = nextprev[1]
    
        posts = page.cssselect('div.fp')

        for post in posts:
            dt = post.cssselect('h3.mh div')[0].text_content().replace('Edited:','').strip()
            if dt.find('yesterday') > 0:
                dt = dt.replace('yesterday',yesterday.strftime('%b %d, %Y'))
            elif dt.find('today') > 0:
                dt = dt.replace('today',today.strftime('%b %d, %Y'))
            elif len(dt.split(',')) == 2: # previous years have the year appended already
                dt = dt.replace(',',', '+year+',')
            date=datetime.strptime(dt,'%b %d, %Y, %I:%M%p')
            text = post.cssselect('div.mT')[0].text_content().strip()
            if text.find('|') > 0 or text.find(u'¦') > 0: # May need a more general regex   
                try:
                    books = int(text.split(' ')[0].replace(',',''))
                    # Text can be in a variety of localized languages, so we need to be flexible
                    users = PATTERN.search(' '.join(text.split(' ')[1:]))
                    if users:
                        users = int(users.group(1))
                        rec = { 'date': date,
                                'books': books,
                                'users': users,
                            }
                        # We'll overwrite if there's more than one record per minute but who cares
                        scraperwiki.sqlite.save(['date'],rec) 
                        #print date, books,users
                except ValueError:
                    print '***Error processing: ',text
            else:
                print '***Skipping***',text
main()

