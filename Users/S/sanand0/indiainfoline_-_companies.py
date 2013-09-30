"""
Data will be stored in the following format: (one row for each company)

URL, Company Name, Revenue, ....


"""
import scraperwiki
from lxml import etree

def get_company_info(url):
    print url
    text = scraperwiki.scrape(url)
    tree = etree.HTML(text)
    data = {
        'url': url,
        'name': tree.find('.//h1').text,
        'industry':tree.findall('.//*[@class="MCnt1"]').text
    }
    print repr(data)
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)

def get_companies(letter):
    print letter
    url = 'http://www.indiainfoline.com/Markets/Company/%s.aspx' % letter
    text = scraperwiki.scrape(url)
    tree = etree.HTML(text)
    for industry in tree.findall('.//*[@class="MCnt1"]'):
           print 'industry'+industry.text

    for link in tree.findall('.//div[@class="topnews_middle"]//a'):
        href = link.get('href')
        if href and href.startswith('/Markets/Company/'):
            get_company_info('http://www.indiainfoline.com' + href)


# for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
for letter in 'A':
    get_companies(letter)
"""
Data will be stored in the following format: (one row for each company)

URL, Company Name, Revenue, ....


"""
import scraperwiki
from lxml import etree

def get_company_info(url):
    print url
    text = scraperwiki.scrape(url)
    tree = etree.HTML(text)
    data = {
        'url': url,
        'name': tree.find('.//h1').text,
        'industry':tree.findall('.//*[@class="MCnt1"]').text
    }
    print repr(data)
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)

def get_companies(letter):
    print letter
    url = 'http://www.indiainfoline.com/Markets/Company/%s.aspx' % letter
    text = scraperwiki.scrape(url)
    tree = etree.HTML(text)
    for industry in tree.findall('.//*[@class="MCnt1"]'):
           print 'industry'+industry.text

    for link in tree.findall('.//div[@class="topnews_middle"]//a'):
        href = link.get('href')
        if href and href.startswith('/Markets/Company/'):
            get_company_info('http://www.indiainfoline.com' + href)


# for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
for letter in 'A':
    get_companies(letter)
