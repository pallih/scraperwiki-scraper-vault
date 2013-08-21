import itertools
import scraperwiki
from lxml.html import parse
from lxml import etree

for i in itertools.count(1):
    url = "http://www.number10.gov.uk/news/speeches-and-transcripts/page/%d" % i
    try:
        for l in parse(url).xpath("//h3[@class='posts_list_post']/a"):
            title = l.text.strip()
            permalink = l.get('href')

            record = {'title': title, 'permalink': permalink, 'minister_name': "David Cameron"}

            speech = parse(permalink)

            record['given_on'] = speech.xpath("//*[@class='timestamp']")[0].text.strip()
            record['body'] = etree.tostring(speech.xpath("//*[@class='entry']")[0])
            record['department'] = "Prime Minister's Office"

            print "Saving %s" % permalink
            scraperwiki.datastore.save(['permalink'], record)
    except Exception, ex:
        break
