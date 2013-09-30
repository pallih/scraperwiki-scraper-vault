# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup

soup = BeautifulSoup(scraperwiki.scrape('http://cityfruit.org/classes.htm'))

class_anchors = soup.find('td', {'class': 'style26'}).findAll('a')
class_anchors = class_anchors[1:]
for classa in class_anchors:
    href = classa.get('href')
    title = classa.text
    sibling = classa.findNextSibling('span')
    sibling = sibling.findNextSibling('span') or sibling
    time = sibling.next
    location = time.next
    while not location or hasattr(location, 'name'):
        print 'going'
        location = location.next
    description = classa.findParent('p').findNextSibling('p').text
    print location
    scraperwiki.sqlite.save(['class_name'], {'class_name': title, 
                                 'class_link': href, 
                                 'class_time': time,
                                 'class_location': location,
                                 'class_description': description})# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup

soup = BeautifulSoup(scraperwiki.scrape('http://cityfruit.org/classes.htm'))

class_anchors = soup.find('td', {'class': 'style26'}).findAll('a')
class_anchors = class_anchors[1:]
for classa in class_anchors:
    href = classa.get('href')
    title = classa.text
    sibling = classa.findNextSibling('span')
    sibling = sibling.findNextSibling('span') or sibling
    time = sibling.next
    location = time.next
    while not location or hasattr(location, 'name'):
        print 'going'
        location = location.next
    description = classa.findParent('p').findNextSibling('p').text
    print location
    scraperwiki.sqlite.save(['class_name'], {'class_name': title, 
                                 'class_link': href, 
                                 'class_time': time,
                                 'class_location': location,
                                 'class_description': description})