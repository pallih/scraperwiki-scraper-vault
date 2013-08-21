import scraperwiki
import requests
import lxml.html
# Blank Python

def returnlink(node):
    links=node.cssselect('a')
    for i in links:
        if i.text!='diff' and i.text!='hist':
            return i


url='http://www.profounddecisions.co.uk/mediawiki-public/index.php?title=Special:RecentChanges&limit=500&days=1'
html=requests.get(url).text
root=lxml.html.fromstring(html)
root.make_links_absolute('http://www.profounddecisions.co.uk')
bits=root.xpath("//div[@id='article']//ul[@class='special']/li[@class]/strong[@class='mw-plusminus-pos']/..")
for x in bits:
    n=returnlink(x)
    print n.get('href'), n.text, n.tail