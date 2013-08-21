import scraperwiki
import lxml.html

html = scraperwiki.scrape('http://www.lbth.org/ncma/gallery/ncmalistview.php?wstr=&alpha=%')

xpath = '//td[2]/table/tr/td/p/a'

root = lxml.html.fromstring(html)

persons = root.xpath(xpath)

for person in persons:
    record={}
    record['name'] = person.text_content()
    record['detail_url'] = person.get('href')
    scraperwiki.sqlite.save(['detail_url'], data=record, table_name='missing_names', verbose=2)
