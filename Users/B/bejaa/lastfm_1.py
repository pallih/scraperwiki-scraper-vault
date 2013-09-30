import requests
text = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1326024000').text
text = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1326628800').text
import lxml.html
root=lxml.html.fromstring(text)
items=root.cssselect("span[class='rankItem-title']")
print [item.text_content() for item in items]
import requests
text = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1326024000').text
text = requests.get('http://www.last.fm/charts/tracks/top/place/Netherlands?ending=1326628800').text
import lxml.html
root=lxml.html.fromstring(text)
items=root.cssselect("span[class='rankItem-title']")
print [item.text_content() for item in items]
