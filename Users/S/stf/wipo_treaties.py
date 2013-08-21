# Blank Python
import lxml.html
import scraperwiki, datetime
from urlparse import urljoin

base="http://www.wipo.int/treaties/en/"

def toText(node):
    if node is None: return ''
    text=''.join([x.strip() for x in node.xpath(".//text()") if x.strip()]).replace(u"\u00A0",' ').strip()

    links=node.xpath('a')
    if not links: return text
    return (text, unicode(urljoin(base,links[0].get('href')),'utf8'))

def convertRow(cells,fields):
    res={}
    if not len(cells)==len(fields): return None
    for i,cell in enumerate(cells):
        tmp=fields[i][1](cell)
        if tmp:
            if type(tmp)==type(tuple()):
                res['url']=tmp[1]
                res[fields[i][0]]=tmp[0]
            else:
                res[fields[i][0]]=tmp
    return res

def toObj(table,fields):
    res=[]
    for row in table.xpath('tr'):
        items=row.xpath('td')
        value=convertRow(items,fields)
        if value:
            res.append(value)
    return res

Fields=( ('Country', toText),
         ('Status', toText),
         ('Date', toText),
         ('Details', toText),
         )


html = scraperwiki.scrape(base)
tree = lxml.html.fromstring(html)

for treaty in tree.xpath('//div[@class="list-01"]//a'):
     url=urljoin(base, treaty.get('href'))
     tpage=lxml.html.fromstring(scraperwiki.scrape(url))
     members=tpage.xpath('//a[text()="Contracting Parties"]')
     if len(members)<2: 
         continue
     url=urljoin(base, members[0].get('href'))
     table=lxml.html.fromstring(scraperwiki.scrape(url)).xpath('//table[@class="table-02"]')[0]
     for obj in toObj(table,Fields):
         obj['treaty']=treaty.xpath('text()')[0]
         del obj['Details']
         scraperwiki.sqlite.save(unique_keys=['Country','treaty'], data=obj)