import requests
import lxml.html
html = requests.get('http://www.top40.nl/top40/2012/week-1').text
dom = lxml.html.fromstring(html)
for items in dom.cssselect ("div.title"):
    rank = 1
    while rank < 41: 
        rank = rank +1
        print rank, items.text_content()
            