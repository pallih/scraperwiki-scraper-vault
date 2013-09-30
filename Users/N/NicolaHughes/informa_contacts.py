import scraperwiki
import lxml.html
from lxml import etree


for n in range(5):

    html = scraperwiki.scrape("http://www.informa.com/Contact-Us/Office-locator/?pn=%s&region=Americas_USA&company=&keywords=" % n) 
    root = lxml.html.fromstring(html)

    for el in root.find('.//div[@class="results"]'):    
    #    print el.text_content()
        name = el.cssselect('h3')[0].text_content()
        address = [el.cssselect('address')[0].text.strip()]
        address.extend([br.tail.strip() for br in el.cssselect('address')[0].getchildren() if br.tail is not None])
        location = ', '.join(address)
        contact = el.cssselect('.grid.g-c')[0].text_content().strip().replace('                                    ', '').replace('\r', ' ')
        #print name
        #print location
        #print contact
        data = {'Text': name, 'Location': location, 'Notes': contact}
        scraperwiki.sqlite.save(['Location'], data)
import scraperwiki
import lxml.html
from lxml import etree


for n in range(5):

    html = scraperwiki.scrape("http://www.informa.com/Contact-Us/Office-locator/?pn=%s&region=Americas_USA&company=&keywords=" % n) 
    root = lxml.html.fromstring(html)

    for el in root.find('.//div[@class="results"]'):    
    #    print el.text_content()
        name = el.cssselect('h3')[0].text_content()
        address = [el.cssselect('address')[0].text.strip()]
        address.extend([br.tail.strip() for br in el.cssselect('address')[0].getchildren() if br.tail is not None])
        location = ', '.join(address)
        contact = el.cssselect('.grid.g-c')[0].text_content().strip().replace('                                    ', '').replace('\r', ' ')
        #print name
        #print location
        #print contact
        data = {'Text': name, 'Location': location, 'Notes': contact}
        scraperwiki.sqlite.save(['Location'], data)
