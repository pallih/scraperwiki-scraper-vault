import scraperwiki
import lxml.html

# Blank Python

def fetch_html(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)
    
front_page_url = "http://moblog.net/Molescroft"
front_page = fetch_html(front_page_url)
base_url = "http://moblog.net"

links = {}

for content_box in front_page.find_class('contentbox'):
    try:
        title = content_box.get_element_by_id('blogshot-title').text
    except:
        title = "No Title"
    for i in content_box.iterlinks():
        if i[2].startswith('/view/'):
            #print i
            links[title] = i[2]
    #if link[2].startswith('/view/'):
        #if links.has_key()
        #print link
        #links.append(link[2])
        #print link[2].spli()

print links
for title, link in links.iteritems():
    try:
        photo_page = fetch_html(base_url + link)

        for post in photo_page.find_class('blogshot-img'):
            print base_url + post.xpath('a/img/@src')[0]

            scraperwiki.sqlite.save(unique_keys=['url'], data={'title': title, 'url': base_url + post.xpath('a/img/@src')[0]}, table_name='Photos')

    except:
        passimport scraperwiki
import lxml.html

# Blank Python

def fetch_html(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)
    
front_page_url = "http://moblog.net/Molescroft"
front_page = fetch_html(front_page_url)
base_url = "http://moblog.net"

links = {}

for content_box in front_page.find_class('contentbox'):
    try:
        title = content_box.get_element_by_id('blogshot-title').text
    except:
        title = "No Title"
    for i in content_box.iterlinks():
        if i[2].startswith('/view/'):
            #print i
            links[title] = i[2]
    #if link[2].startswith('/view/'):
        #if links.has_key()
        #print link
        #links.append(link[2])
        #print link[2].spli()

print links
for title, link in links.iteritems():
    try:
        photo_page = fetch_html(base_url + link)

        for post in photo_page.find_class('blogshot-img'):
            print base_url + post.xpath('a/img/@src')[0]

            scraperwiki.sqlite.save(unique_keys=['url'], data={'title': title, 'url': base_url + post.xpath('a/img/@src')[0]}, table_name='Photos')

    except:
        pass