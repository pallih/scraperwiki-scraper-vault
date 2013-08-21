import scraperwiki
from urllib2 import urlopen
from lxml.html import fromstring

gasp_helper = scraperwiki.utils.swimport("gasp_helper")
# http://services.sunlightlabs.com/gasp/legislators/
gasp = gasp_helper.GaspHelper("889590f337454382b5ecb23e1a6710aa", "F00010")

#index_html = fromstring(urlopen('http://www.house.gov/faleomavaega/').read())
bio_html = fromstring(urlopen('http://www.house.gov/faleomavaega/bio.shtml').read())

def bio(html):
    biography = html.xpath('//td[h1[text()="Biography"]]')[0].text_content()
    gasp.add_biography(biography)

def office(html):
    for office in html.cssselect('.address'):
        #name = address.xpath('strong/text()')
        officelines = office.xpath('text()')
        address = '\n'.join(officelines[0:3])
        phone = officelines[3]
        fax = officelines[4]
        gasp.add_office(address, phone, fax)

bio(bio_html)
office(bio_html)

#gasp.finish()