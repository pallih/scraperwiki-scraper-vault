# Blank Python
import lxml.html
import scraperwiki, datetime
from urlparse import urljoin

base="http://conventions.coe.int/Treaty/Commun/ListeTraites.asp?CM=8&CL=ENG"

def toText(node):
    if node is None: return ''
    text=''.join([x.strip() for x in node.xpath(".//text()") if x.strip()]).replace(u"\u00A0",' ').strip()

    links=node.xpath('a')
    if not links: return text
    return (text, unicode(urljoin(base,links[0].get('href')),'utf8'))

def convertRow(cells,fields):
    res={}
    if not len(cells)==len(fields): 
        if len(cells)==13:
             fields=signatoryFields13
        else:
             return None
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
    for row in table.xpath('tr')[1:]:
        items=row.xpath('td')
        value=convertRow(items,fields)
        if value:
            res.append(value)
    return res

Fields=( ('ID', toText),
         ('Title', toText),
         ('Opening', toText),
         ('Entry', toText),
         ('Non-EU European', toText),
         ('Non-european', toText),
         ('EU', toText),         
         )
signatoryFields=( ('Country', toText),
         ('Signature', toText),
         ('Ratification', toText),
         ('Entry', toText),
         ('Note', toText),
         ('Reservations', toText),
         ('Declarations', toText),
         ('Authorities', toText),
         ('Territorial Application', toText),
         ('Communication', toText),
         ('Objection', toText),
         )
signatoryFields13=( ('Country', toText),
         ('Signature', toText),
         ('Ratification', toText),
         ('Entry', toText),
         ('Note', toText),
         ('Reservations', toText),
         ('Denunciation', toText),
         ('Effect denunciation', toText),
         ('Declarations', toText),
         ('Authorities', toText),
         ('Territorial Application', toText),
         ('Communication', toText),
         ('Objection', toText),
         )
html = scraperwiki.scrape("http://conventions.coe.int/Treaty/Commun/ListeTraites.asp?CM=8&CL=ENG")
tree = lxml.html.fromstring(html)

table=tree.xpath('//table//table')[0]
for obj in toObj(table,Fields):
    scraperwiki.sqlite.save(unique_keys=['ID'], data=obj)
    sigtree=lxml.html.fromstring(scraperwiki.scrape("http://conventions.coe.int/Treaty/Commun/ChercheSig.asp?NT=%s&CM=&DF=&CL=ENG" % obj['ID']))
    #print "http://conventions.coe.int/Treaty/Commun/ChercheSig.asp?NT=%s&CM=&DF=&CL=ENG" % obj['ID']
    for ttable in sigtree.xpath('//table//table'):
         for country in toObj(ttable,signatoryFields):
             country['treaty']=obj['Title']
             #print country
             scraperwiki.sqlite.save(unique_keys=['treaty', "Country"], table_name='members', data=country)
