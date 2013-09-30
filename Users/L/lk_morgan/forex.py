#import scraperwiki
import requests
import lxml.html

html = requests.get('http://www.xe.com/').text

root = lxml.html.fromstring(html)

links = root.xpath('//a[contains(@href, "/currencycharts/")]')

for l in links:
  if l.text !='Currency Charts':
    print l.attrib['href'][22:25],l.attrib['href'][29:32],l.text
#    scraperwiki.sqlite.save(unique_keys=["Currency One","Currency Two"],data={"Currency One":l.attrib['href'][22:25],"Currency Two":l.attrib['href'][29:32],"Rate":l.text})
