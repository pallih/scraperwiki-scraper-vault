###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.matlabtips.com'
html = scraperwiki.scrape(starting_url)
print html
tree = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
storyNodes = tree.findAll('div', 'post')# encontrando items... 
if not storyNodes:
    print '[SCRIPT] - No se encuentran items (articulos)...'
    self.items = 0
            #return self.items
else:
    print storyNodes
for node in storyNodes:
    ases = node.findAll('a')
    print ases
    title = ases[0].string
    print title
    #title = node.find('h3').string
    link = ases[1]['href']
    print link
    #link = node.find('a')['name']
    texto = node.find('div', 'post-content')
    if not texto:
        texto = node.find('div', 'entry-content')
    description = texto.text
    print description
    #description = self.cleanHTML(node.find('div', attrs={'class': 'separator'}).contents)
    difecha = node.find('p', 'post-date')
    if difecha:
        fecha = difecha.string + ' - '
    else:
        fecha = ''
    print fecha
    try:
        image = node.find('img')['src']
        if image:
            imagen = image
        else:
            imagen = 'No hay imagen'
    except:
        imagen = 'excepcion image'
    print imagen
    print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    
    
