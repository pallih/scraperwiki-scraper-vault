import scraperwiki
import lxml.html    
import requests       


url = 'http://www.sleeps.com/dictionary/xxx.html'
headers_dict = {'user-agent': 'Mozilla/5.0'}


html = requests.get(url, headers=headers_dict)
root = lxml.html.fromstring(html.text)

#print html

count = 1
dts = root.cssselect('p') 


for dt in dts:
    dream =  dt.text
    data = {'count' : count, 'Dream': dream}
    scraperwiki.sqlite.save(unique_keys=['count'], data = data)
    count = count + 1
    print dream

url = 'http://www.sleeps.com/dictionary/yyy.html'

html = requests.get(url, headers=headers_dict)
root = lxml.html.fromstring(html.text)

dts = root.cssselect('p') 

for dt in dts:
    dream =  dt.text
    data = {'count' : count, 'Dream': dream}
    scraperwiki.sqlite.save(unique_keys=['count'], data = data)
    count = count + 1
    print dream



url = 'http://www.sleeps.com/dictionary/zzz.html'

html = requests.get(url, headers=headers_dict)
root = lxml.html.fromstring(html.text)

dts = root.cssselect('p') 

for dt in dts:
    dream =  dt.text
    data = {'count' : count, 'Dream': dream}
    scraperwiki.sqlite.save(unique_keys=['count'], data = data)
    count = count + 1
    print dream

