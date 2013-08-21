from urllib2 import urlopen
from lxml.html import fromstring
from scraperwiki.sqlite import save

html = urlopen("http://www.gsa.gov/portal/indexpage/category/26640/hostUri/portal").read()
print html
1/0

x = fromstring(html)

pastyears = [a.attrib['href'] for a in x.cssselect('.forms a')]

rows = x.cssselect('.Datatable > tr')
for row in rows:
    date, title = [cell.text_content() for cell in row.cssselect('td')]
    href = row.cssselect('a')[0].attrib['href']
    data = {
        "date": date,
        "title": title,
        "href": href
    }
    html = urlopen("http://www.gsa.gov" + href).read()
    data['document'] =  html
    data['health'] = "health" in html.lower()
    save(['href'],data)