from scraperwiki import scrape
from lxml.html import fromstring
from scraperwiki.sqlite import save
import re

URL="http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm"

def slugify(text):
    text=text.replace('#','num').replace(' ','_')
    text=re.sub(r'[*\r\n]','',text)
    return text

def getTableRows(tree):
    tables=tree.cssselect('table')
    table=tables[2]
    trs=table.cssselect('tr')
    return trs

def getRowText(tableRow):
    cells=tableRow.cssselect('th,td')
    cellsText=[cell.text_content() for cell in cells]
    return cellsText

html=scrape(URL)
tree=fromstring(html)
tableRows=getTableRows(tree)

header=tableRows.pop(0)

headerText=getRowText(header)
columnNames=map(slugify,headerText)

for tableRow in tableRows:
    rowText=getRowText(tableRow)
    data=dict(zip(columnNames,rowText))
    save([],data)
from scraperwiki import scrape
from lxml.html import fromstring
from scraperwiki.sqlite import save
import re

URL="http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm"

def slugify(text):
    text=text.replace('#','num').replace(' ','_')
    text=re.sub(r'[*\r\n]','',text)
    return text

def getTableRows(tree):
    tables=tree.cssselect('table')
    table=tables[2]
    trs=table.cssselect('tr')
    return trs

def getRowText(tableRow):
    cells=tableRow.cssselect('th,td')
    cellsText=[cell.text_content() for cell in cells]
    return cellsText

html=scrape(URL)
tree=fromstring(html)
tableRows=getTableRows(tree)

header=tableRows.pop(0)

headerText=getRowText(header)
columnNames=map(slugify,headerText)

for tableRow in tableRows:
    rowText=getRowText(tableRow)
    data=dict(zip(columnNames,rowText))
    save([],data)
