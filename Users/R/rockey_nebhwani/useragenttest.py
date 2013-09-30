import scraperwiki
import lxml.html
import requests


# Global settings

base_url = 'http://groceries.asda.com/asda-estore/search/searchcontainer.jsp?trailSize=1&searchString=beer'
headers_dict = {'user-agent': 'Mozilla/5.0'}


# Helper functions

def get_dates():
    dates = []
    print '-- Scraping the list of dates'
    url = base_url 
    html = requests.get(url, headers=headers_dict)
    print html;
    dom = lxml.html.fromstring(html.text)
    root = lxml.html.fromstring(html)
    for el in root.cssselect("div#facetedSearch"):           
        print el
#    for option in dom.cssselect('#communityByRegionfilterDayTorch option'):
#        if option.get('value'):
#            dates.append({'url': base_url + option.get('value'), 'date': option.text})
#    print '-- Saving the list of dates'
#    scraperwiki.sqlite.save(['url'], dates, 'dates')


try:
    # Do we have a list of dates?
    print scraperwiki.sqlite.select('count(*) as count from dates')[0]['count'], 'dates found'
except:
    # No we don't. So get them…
    get_dates()
import scraperwiki
import lxml.html
import requests


# Global settings

base_url = 'http://groceries.asda.com/asda-estore/search/searchcontainer.jsp?trailSize=1&searchString=beer'
headers_dict = {'user-agent': 'Mozilla/5.0'}


# Helper functions

def get_dates():
    dates = []
    print '-- Scraping the list of dates'
    url = base_url 
    html = requests.get(url, headers=headers_dict)
    print html;
    dom = lxml.html.fromstring(html.text)
    root = lxml.html.fromstring(html)
    for el in root.cssselect("div#facetedSearch"):           
        print el
#    for option in dom.cssselect('#communityByRegionfilterDayTorch option'):
#        if option.get('value'):
#            dates.append({'url': base_url + option.get('value'), 'date': option.text})
#    print '-- Saving the list of dates'
#    scraperwiki.sqlite.save(['url'], dates, 'dates')


try:
    # Do we have a list of dates?
    print scraperwiki.sqlite.select('count(*) as count from dates')[0]['count'], 'dates found'
except:
    # No we don't. So get them…
    get_dates()
import scraperwiki
import lxml.html
import requests


# Global settings

base_url = 'http://groceries.asda.com/asda-estore/search/searchcontainer.jsp?trailSize=1&searchString=beer'
headers_dict = {'user-agent': 'Mozilla/5.0'}


# Helper functions

def get_dates():
    dates = []
    print '-- Scraping the list of dates'
    url = base_url 
    html = requests.get(url, headers=headers_dict)
    print html;
    dom = lxml.html.fromstring(html.text)
    root = lxml.html.fromstring(html)
    for el in root.cssselect("div#facetedSearch"):           
        print el
#    for option in dom.cssselect('#communityByRegionfilterDayTorch option'):
#        if option.get('value'):
#            dates.append({'url': base_url + option.get('value'), 'date': option.text})
#    print '-- Saving the list of dates'
#    scraperwiki.sqlite.save(['url'], dates, 'dates')


try:
    # Do we have a list of dates?
    print scraperwiki.sqlite.select('count(*) as count from dates')[0]['count'], 'dates found'
except:
    # No we don't. So get them…
    get_dates()
import scraperwiki
import lxml.html
import requests


# Global settings

base_url = 'http://groceries.asda.com/asda-estore/search/searchcontainer.jsp?trailSize=1&searchString=beer'
headers_dict = {'user-agent': 'Mozilla/5.0'}


# Helper functions

def get_dates():
    dates = []
    print '-- Scraping the list of dates'
    url = base_url 
    html = requests.get(url, headers=headers_dict)
    print html;
    dom = lxml.html.fromstring(html.text)
    root = lxml.html.fromstring(html)
    for el in root.cssselect("div#facetedSearch"):           
        print el
#    for option in dom.cssselect('#communityByRegionfilterDayTorch option'):
#        if option.get('value'):
#            dates.append({'url': base_url + option.get('value'), 'date': option.text})
#    print '-- Saving the list of dates'
#    scraperwiki.sqlite.save(['url'], dates, 'dates')


try:
    # Do we have a list of dates?
    print scraperwiki.sqlite.select('count(*) as count from dates')[0]['count'], 'dates found'
except:
    # No we don't. So get them…
    get_dates()
