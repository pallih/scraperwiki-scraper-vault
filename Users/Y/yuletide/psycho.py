import scraperwiki, lxml.html, re

# Blank Python
base_url = 'http://www.psychocydd.co.uk/'

def scrape_page(page):
    html = scraperwiki.scrape('http://www.psychocydd.co.uk/torrents.php?active=1&options=0&order=data&by=DESC&page='+str(page))
    root = lxml.html.fromstring(html)
    
    for index,tr in enumerate(root.cssselect('table.lista tr')):
        if index > 24 and index < 55:            
            item = {}
            for i,link in enumerate(tr.iterlinks()):
                if i == 1:
                    item['url'] = base_url + link[2]
                    item['id'] = link[2].split('details.php?id=')[1]
                if i == 3:
                    item['download'] = base_url + link[2]
            for i,td in enumerate(tr.cssselect('td')):
                if i == 0:
                    item['genre'] = td.text_content()
                if i == 1:
                    item['title'] = td.cssselect('a')[0].text_content()
                    item['subgenre'] = td.cssselect('span')[0].text_content()
                if i == 2:
                    item['comments'] = td.text_content()
                if i == 3:
                    img = td.cssselect('img')
                    if not len(img):
                        item['ratings'] = 0
                        item['rating'] = -1
                    else:
                        rat = re.split('(\d) votes \(rating: (\d\.?\d?)/5.0\)', img[0].get('title'))
                        item['ratings'] = rat[1]
                        item['rating'] = rat[2]

                if i == 5:
                    item['date'] = td.text_content()
                if i == 6:
                    item['size'] = td.text_content()
                if i == 7:
                    item['seeds'] = td.text_content()
                if i == 8:
                    item['leeches'] = td.text_content()
                if i == 9:
                    item['completed'] = td.text_content()
            print item
            scraperwiki.sqlite.save(unique_keys=['id'], data=item)
for i in range(0,5):
    scrape_page(i)import scraperwiki, lxml.html, re

# Blank Python
base_url = 'http://www.psychocydd.co.uk/'

def scrape_page(page):
    html = scraperwiki.scrape('http://www.psychocydd.co.uk/torrents.php?active=1&options=0&order=data&by=DESC&page='+str(page))
    root = lxml.html.fromstring(html)
    
    for index,tr in enumerate(root.cssselect('table.lista tr')):
        if index > 24 and index < 55:            
            item = {}
            for i,link in enumerate(tr.iterlinks()):
                if i == 1:
                    item['url'] = base_url + link[2]
                    item['id'] = link[2].split('details.php?id=')[1]
                if i == 3:
                    item['download'] = base_url + link[2]
            for i,td in enumerate(tr.cssselect('td')):
                if i == 0:
                    item['genre'] = td.text_content()
                if i == 1:
                    item['title'] = td.cssselect('a')[0].text_content()
                    item['subgenre'] = td.cssselect('span')[0].text_content()
                if i == 2:
                    item['comments'] = td.text_content()
                if i == 3:
                    img = td.cssselect('img')
                    if not len(img):
                        item['ratings'] = 0
                        item['rating'] = -1
                    else:
                        rat = re.split('(\d) votes \(rating: (\d\.?\d?)/5.0\)', img[0].get('title'))
                        item['ratings'] = rat[1]
                        item['rating'] = rat[2]

                if i == 5:
                    item['date'] = td.text_content()
                if i == 6:
                    item['size'] = td.text_content()
                if i == 7:
                    item['seeds'] = td.text_content()
                if i == 8:
                    item['leeches'] = td.text_content()
                if i == 9:
                    item['completed'] = td.text_content()
            print item
            scraperwiki.sqlite.save(unique_keys=['id'], data=item)
for i in range(0,5):
    scrape_page(i)