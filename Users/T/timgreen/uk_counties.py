# UK counties
import scraperwiki
import lxml.html

tree = lxml.html.parse("http://en.wikipedia.org/wiki/List_of_counties_of_the_United_Kingdom")

for td in tree.xpath('//table[@class="wikitable"]/tr/td[1]'):
    a = td.xpath('a')[0]

    scraperwiki.sqlite.save(['url'], {'full_name': td.text_content(), 'name':a.text, 'url': 'http://en.wikipedia.org%s' % a.attrib['href']}, table_name='counties')