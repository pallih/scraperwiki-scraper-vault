import scraperwiki
import lxml.html   

symbol="bp"
html = scraperwiki.scrape('http://www.google.com/finance?q='+symbol)
root = lxml.html.fromstring(html)

for quote in root.cssselect(".pr span"):
    print quote.text_content()







#m = re.search('span id="ref.*>(.*)<', root.text_content())
#if root.cssselect(".pr span"):
#    for quote in root.cssselect(".pr span"):
#        print quote.text_content()
#else:
#    quote = 'no quote for symbol: ' + symbol
# print(quote)

import scraperwiki
import lxml.html   

symbol="bp"
html = scraperwiki.scrape('http://www.google.com/finance?q='+symbol)
root = lxml.html.fromstring(html)

for quote in root.cssselect(".pr span"):
    print quote.text_content()







#m = re.search('span id="ref.*>(.*)<', root.text_content())
#if root.cssselect(".pr span"):
#    for quote in root.cssselect(".pr span"):
#        print quote.text_content()
#else:
#    quote = 'no quote for symbol: ' + symbol
# print(quote)

import scraperwiki
import lxml.html   

symbol="bp"
html = scraperwiki.scrape('http://www.google.com/finance?q='+symbol)
root = lxml.html.fromstring(html)

for quote in root.cssselect(".pr span"):
    print quote.text_content()







#m = re.search('span id="ref.*>(.*)<', root.text_content())
#if root.cssselect(".pr span"):
#    for quote in root.cssselect(".pr span"):
#        print quote.text_content()
#else:
#    quote = 'no quote for symbol: ' + symbol
# print(quote)

