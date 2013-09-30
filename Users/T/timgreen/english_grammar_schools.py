import urllib2
import urllib
import lxml.html

url = 'http://en.wikipedia.org/wiki/List_of_grammar_schools_in_England'

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
req = urllib2.Request(url, '', headers)
response = urllib2.urlopen(req)
htmlSource = response.read()

list_tree = lxml.html.parse(htmlSource, base_url=url)

#scraperwiki.sqlite.execute('drop table schools')

for a in list_tree.xpath('//div[@id="bodyContent"]//ul/li/a[1]'):
    if '/wiki' in a.attrib['href']:
        url = "http://en.wikipedia.org%s" % a.attrib['href']
        name = a.text

        response = urllib2.urlopen(url)
        tree = lxml.html.parse(response, base_url=url)
        postcode = None
        for noteth in tree.xpath('//span[@class="postal-code"]'):
            postcode = noteth.text

        scraperwiki.sqlite.save(['url'], {'name': name, 'url': url, 'postcode': postcode}, table_name='schools')

import urllib2
import urllib
import lxml.html

url = 'http://en.wikipedia.org/wiki/List_of_grammar_schools_in_England'

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
req = urllib2.Request(url, '', headers)
response = urllib2.urlopen(req)
htmlSource = response.read()

list_tree = lxml.html.parse(htmlSource, base_url=url)

#scraperwiki.sqlite.execute('drop table schools')

for a in list_tree.xpath('//div[@id="bodyContent"]//ul/li/a[1]'):
    if '/wiki' in a.attrib['href']:
        url = "http://en.wikipedia.org%s" % a.attrib['href']
        name = a.text

        response = urllib2.urlopen(url)
        tree = lxml.html.parse(response, base_url=url)
        postcode = None
        for noteth in tree.xpath('//span[@class="postal-code"]'):
            postcode = noteth.text

        scraperwiki.sqlite.save(['url'], {'name': name, 'url': url, 'postcode': postcode}, table_name='schools')

