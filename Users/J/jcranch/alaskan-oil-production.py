"""
Monthly Alaskan oil production figures

http://www.tax.state.ak.us/programs/oil/production.aspx
"""

from urllib2 import urlopen
from html5lib import HTMLParser, treebuilders
import re
from scraperwiki import datastore


def main():
    url = "http://www.tax.state.ak.us/programs/oil/production.aspx"

    parser = HTMLParser(tree=treebuilders.getTreeBuilder("lxml"))
    page = parser.parse(urlopen(url))

    dates = []

    for o in page.findall("body/form/div/div/div/div/select/option"):
        d = o.attrib["value"]
        if processDate(d):
            dates.append(d)

    for d in dates:
        extractMonthlyData(d)

        

fields = ["Date",
          "Prudhoe Bay",
          "Kuparuk",
          "Milne Point",
          "Endicott",
          "Lisburne",
          "Alpine",
          "Northstar",
          "ANS",
          "Cook Inlet",
          "Alaska",
          "Inventories",
          "PS# Temperature"]



def extractMonthlyData(d):
    print "Date: " + d
    
    url = "http://www.tax.state.ak.us/programs/oil/production/ans.aspx?" + d

    parser = HTMLParser(tree=treebuilders.getTreeBuilder("lxml"))
    page = parser.parse(urlopen(url))
        
    for r in page.findall("body/form/div/div/div/div/table/tbody/tr"):
        l = list(c.text for c in r.findall("td"))
        d = processDate(l[0])
        if d:
            l[0] = d
            data = dict(zip(fields,l))
            datastore.save(unique_keys=["Date"], data=data)
        


datere = re.compile("([0-9]+)/([0-9]+)/([0-9][0-9][0-9][0-9])")
def processDate(d):
    if d and datere.match(d):
        return datere.sub("\\3/\\1/\\2",d)
    else:
        return False

    

main()
