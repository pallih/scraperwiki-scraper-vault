# Blank Python
import lxml.html
import scraperwiki, datetime
from urlparse import urljoin

base="http://www.mkogy.hu/hivatal/uveg/"

def toDate(node):
    text=''.join([x.strip() for x in node.xpath(".//text()") if x.strip()]).replace(u"\u00A0",' ').strip()
    if text is None or not len(text): return
    lines=text.split('\n')
    if len(lines)>1:
        result=[]
        for text in lines:
            value=[int(x) for x in text.strip().split('.') if x]
            result.append(datetime.date(value[0], value[1], value[2]))
        return result
    else:
        value=[int(x) for x in text.strip().split('.') if x]
        return datetime.date(value[0], value[1], value[2])

def toText(node):
    if node is None: return ''
    return ''.join([x.strip() for x in node.xpath(".//text()") if x.strip()]).replace(u"\u00A0",' ').strip()

def convertRow(cells,fields):
    res={}
    if not len(cells)==len(fields): return None
    for i,cell in enumerate(cells):
        tmp=fields[i][1](cell)
        if tmp: res[fields[i][0]]=tmp
    return res

def toObj(table,fields):
    res=[]
    for row in table.xpath('tr')[1:]:
        items=row.xpath('td')
        value=convertRow(items,fields)
        if value:
            res.append(value)
    return res

Fields=( ('Azonosito', toText),
         ('Szerzodes vagy modositas datuma', toDate),
         ('Modositas sorszama', toText),
         ('Modositas oka', toText),
         ('Targy', toText),
         ('Tipus', toText),
         ('Szallitasi mod', toText),
         ('Megrendelo fel', toText),
         ('Megrendelo Alairo', toText),
         ('Szallito fel', toText),
         ('Szallito Alairo', toText),
         ('ertek', toText),
         ('Tel', toDate),
         ('Ig',toDate)
         )


html = scraperwiki.scrape("http://www.mkogy.hu/hivatal/uveg/uvegzseb.htm")
tree = lxml.html.fromstring(html)

table=tree.xpath('//table')[0]
for obj in toObj(table,Fields):
    scraperwiki.sqlite.save(unique_keys=['Azonosito'], data=obj)