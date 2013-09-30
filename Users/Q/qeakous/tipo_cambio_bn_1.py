import scraperwiki
import lxml.html

html = scraperwiki.scrape('http://www.bn.com.pe/tipo-cambio.asp')
a = lxml.html.fromstring(html)
textos = a.cssselect('strong') 

data = {
    'id' : 2,
    'cambio' : textos[0].text_content()
}

scraperwiki.sqlite.save(['id'],data) 


# Blank Python

import scraperwiki
import lxml.html

html = scraperwiki.scrape('http://www.bn.com.pe/tipo-cambio.asp')
a = lxml.html.fromstring(html)
textos = a.cssselect('strong') 

data = {
    'id' : 2,
    'cambio' : textos[0].text_content()
}

scraperwiki.sqlite.save(['id'],data) 


# Blank Python

