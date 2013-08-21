import scraperwiki
import lxml.html


xpath = '//ol[@class="tracks"]/li'
url = 'http://soundcloud.com/iceland-airwaves/sets'
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
results = root.xpath(xpath)

for x in results:
    record = {}
    record['soundcloud_id'] = x.attrib['data-sc-track']
    record['title'] = x[1][1].text.encode('iso-8859-1')
    record['artist'] = x[1][1].text.encode('iso-8859-1').partition('-')[0].strip()
    record['song_title'] = x[1][1].text.encode('iso-8859-1').partition('-')[2].strip()
    scraperwiki.sqlite.save(unique_keys=["soundcloud_id"], data=record)
