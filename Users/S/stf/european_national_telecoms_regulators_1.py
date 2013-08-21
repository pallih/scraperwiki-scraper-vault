# Blank Python
import lxml.html
import scraperwiki, datetime
from urlparse import urljoin

base="http://erg.eu.int/links/index_en.htm"

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
         ('Name', toText),
         ('Abbrev', toText),
         )


html = scraperwiki.scrape("http://erg.eu.int/links/index_en.htm")
tree = lxml.html.fromstring(html)

table=tree.xpath('//table//table')[0]
for obj in toObj(table,Fields):
    scraperwiki.sqlite.save(unique_keys=['Country','Name','Abbrev'], data=obj)
