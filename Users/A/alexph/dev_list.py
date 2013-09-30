import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://britishindie.com/developers/")
root = lxml.html.fromstring(html)

for el in root.cssselect('div#leftcontent table tr td'):
    location = 'unknown'

    for o in el.cssselect('p, h2'):
        if o.tag == 'h2':
            location = o.text_content()
        else:
            name = None
            urls = []

            infos = o.getchildren()

            for i, info in enumerate(infos):
                if i == 0:
                    name = info.text
                elif info.tag == 'a':
                    if 'href' in info.attrib:
                        urls.append(info.attrib['href'])

            if name != None:
                data = {
                    'name': name,
                    'location': location
                }
    
                for k, v in enumerate(urls):
                    new_k = 'url%d' % k
                    data[new_k] = v

                scraperwiki.sqlite.save(unique_keys=['name'], data=data)
import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://britishindie.com/developers/")
root = lxml.html.fromstring(html)

for el in root.cssselect('div#leftcontent table tr td'):
    location = 'unknown'

    for o in el.cssselect('p, h2'):
        if o.tag == 'h2':
            location = o.text_content()
        else:
            name = None
            urls = []

            infos = o.getchildren()

            for i, info in enumerate(infos):
                if i == 0:
                    name = info.text
                elif info.tag == 'a':
                    if 'href' in info.attrib:
                        urls.append(info.attrib['href'])

            if name != None:
                data = {
                    'name': name,
                    'location': location
                }
    
                for k, v in enumerate(urls):
                    new_k = 'url%d' % k
                    data[new_k] = v

                scraperwiki.sqlite.save(unique_keys=['name'], data=data)
