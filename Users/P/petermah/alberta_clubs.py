import scraperwiki           
import lxml.html  


def get_links(page):
    html = scraperwiki.scrape("https://alberta.collegiatelink.net/organizations?SearchType=None&SelectedCategoryId=0&CurrentPage=%s" % page)
             
    root = lxml.html.fromstring(html)
    for div in root.cssselect('div#results div'):
        item = div.cssselect('h5 a')
        if item:
            data = {
                    'name': item[0].text.strip(),
                    'link': item[0].get('href'),
                }
            scraperwiki.sqlite.save(unique_keys=['name'], data=data)


def get_xpath(content, xpath):
    item = content.xpath(xpath)
    if item:
        item = item[0].text.strip()
    else:
        item = ""
    return item.strip()

def parse_page(name, link):
    html = scraperwiki.scrape("https://alberta.collegiatelink.net%s" % link)
    root = lxml.html.fromstring(html)
    content = lxml.html.etree.HTML(html)

    url = root.cssselect('div[id="smallColumn"] div')[2].cssselect('div a')
    if url:
        url = url[0].get('href')
    else:
        url = ""
    data = {
        'url': url,
        'address': get_xpath(content, '//*[@id="smallColumn"]/div[3]/div[1]/div[1]'),
        'email': get_xpath(content, '//*[@id="smallColumn"]/div[3]/div[1]/div[2]'),
        'phone': get_xpath(content, '//*[@id="smallColumn"]/div[3]/div[1]/div[3]'),
        'person': get_xpath(content, '//*[@id="smallColumn"]/div[3]/div[2]/div[1]/div[2]/div[2]'),
        'name': name,
        'link': link,
        }

    scraperwiki.sqlite.save(unique_keys=['name'], data=data)


#for i in range(32):
 #   get_links(i)

data = scraperwiki.sqlite.execute("select * from swdata")['data']

for item in data:
    parse_page(item[1], item[0])import scraperwiki           
import lxml.html  


def get_links(page):
    html = scraperwiki.scrape("https://alberta.collegiatelink.net/organizations?SearchType=None&SelectedCategoryId=0&CurrentPage=%s" % page)
             
    root = lxml.html.fromstring(html)
    for div in root.cssselect('div#results div'):
        item = div.cssselect('h5 a')
        if item:
            data = {
                    'name': item[0].text.strip(),
                    'link': item[0].get('href'),
                }
            scraperwiki.sqlite.save(unique_keys=['name'], data=data)


def get_xpath(content, xpath):
    item = content.xpath(xpath)
    if item:
        item = item[0].text.strip()
    else:
        item = ""
    return item.strip()

def parse_page(name, link):
    html = scraperwiki.scrape("https://alberta.collegiatelink.net%s" % link)
    root = lxml.html.fromstring(html)
    content = lxml.html.etree.HTML(html)

    url = root.cssselect('div[id="smallColumn"] div')[2].cssselect('div a')
    if url:
        url = url[0].get('href')
    else:
        url = ""
    data = {
        'url': url,
        'address': get_xpath(content, '//*[@id="smallColumn"]/div[3]/div[1]/div[1]'),
        'email': get_xpath(content, '//*[@id="smallColumn"]/div[3]/div[1]/div[2]'),
        'phone': get_xpath(content, '//*[@id="smallColumn"]/div[3]/div[1]/div[3]'),
        'person': get_xpath(content, '//*[@id="smallColumn"]/div[3]/div[2]/div[1]/div[2]/div[2]'),
        'name': name,
        'link': link,
        }

    scraperwiki.sqlite.save(unique_keys=['name'], data=data)


#for i in range(32):
 #   get_links(i)

data = scraperwiki.sqlite.execute("select * from swdata")['data']

for item in data:
    parse_page(item[1], item[0])