import scraperwiki
import lxml.html

def printHtml(html):
    print lxml.html.tostring(html)

          
html = scraperwiki.scrape("http://allestoringen.nl/overzicht/")
root = lxml.html.fromstring(html)

data = []
for table in root.cssselect("table.table"):           
    for tr in table.cssselect("tr"):
        date = ""
        target = ""
        story = ""
        for div in tr.cssselect("div.date"):
            date = div.text_content().strip()
        for td in tr.cssselect("td.span7"):
            contents = []
            for a in td.cssselect("a"):
                contents.append(a.text_content().strip())
            target = contents[0]
            story = contents[1]
        data.append({'date' : date, 'target' : target, 'story' : story})

result = '"date","target","story"\n'
for d in data:
    result += '"{0}","{1}","{2}"\n'.format(d['date'], d['target'], d['story'])

print result


