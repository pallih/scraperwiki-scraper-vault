from __future__ import division
import sys, time, os
import mechanize
import lxml.html
import string
import scraperwiki


COMPACT_URL = 'http://www.amazon.co.uk/registry/wishlist/31LBH13Q90O5Q/ref=cm_wl_act_vv?_encoding=UTF8&filter=all&sort=date-added&layout=compact&visitor-view=1&reveal=all'
NORMAL_URL = 'http://www.amazon.co.uk/registry/wishlist/31LBH13Q90O5Q?visitor-view=1&reveal=all&filter=all&sort=date-added&layout=standard&x=9&y=13'
GIFTLISTNO = '442551'

br = mechanize.Browser()                # Create a browser
br.open(COMPACT_URL)            # Open the login page
print br.geturl()


datasheet = br.response().read()

#print datasheet

root = lxml.html.fromstring(datasheet)


prodstring = root.cssselect("tbody.itemWrapper span.productTitle")
print prodstring

prodtiny = root.cssselect("tbody.itemWrapper td.tiny")
print prodtiny

#INTEGER CHECK FUNCTION
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

#print RepresentsInt("+123")

#print RepresentsInt("10.0")

arrayprice = []
arraywant = []
arraygot = []
arrayprior = []
arrayname = []
arrayimage = []

for index, item in enumerate(prodtiny):
    varprodstrip = lxml.html.tostring(item)

    varprodstrip = string.replace(varprodstrip, '<td class="tiny"><span class="price"><strong>&#163;', '')
    varprodstrip = string.replace(varprodstrip, '</strong></span></td>', '')

    varprodstrip = string.replace(varprodstrip, '<td align="center" class="tiny">', '')
    varprodstrip = string.replace(varprodstrip, '</td>', '')
    varprodstrip = string.replace(varprodstrip, ' ', '')
    varprodstrip = string.join(string.split(varprodstrip), "")
    
    varprodpriceno = (index+4)%4
    varprodwantno = (index+3)%4
    varprodgotno = (index+2)%4
    varprodpriorno = (index+1)%4

    tinystring = "Tiny String = %s --- " % varprodstrip
    tinystring+= "index = %d --- " % index
    tinystring+= "After Sum Price - %d --- " % varprodpriceno
    tinystring+= "After Sum Want - %d --- " % varprodwantno
    tinystring+= "After Sum Got - %d" % varprodgotno
    tinystring+= "After Sum Prior - %d" % varprodpriorno
    print tinystring

    if varprodpriceno==0:
        print ' - divisible by 4 - price %s'% varprodstrip
        arrayprice.append(varprodstrip)

    if varprodwantno==0:
        print ' - divisible by 4 - want %s'% varprodstrip
        arraywant.append(varprodstrip)

    if varprodgotno==0:
        print ' - divisible by 4 - got %s'% varprodstrip
        arraygot.append(varprodstrip)

    if varprodpriorno==0:
        print ' - divisible by 4 - prior %s'% varprodstrip
        arrayprior.append(varprodstrip)

for index, item in enumerate(prodstring):
    varnamestrip = lxml.html.tostring(item)
    varnamestrip = string.replace(varnamestrip, '=', '')
    varnamestrip = string.replace(varnamestrip, '"', '')
    varnamestrip = string.replace(varnamestrip, '<', '')
    varnamestrip = string.replace(varnamestrip, '>', '')
    varnamestrip = string.replace(varnamestrip, '/', '')

    pat2 = 'word1\s(.*)\sword2'
    test2 = 'word1 will never be a word2'
    repl2 = 'replace'
    
    #span classsmall productTitlestronga
    pat = 'span\s(.*)\srelnofollow'
    test = varnamestrip
    repl = ''
   

    import re
    m = re.search(pat,test)
    
    if m and m.groups() > 0:
        line = test[0:m.start(1)] + repl + test[m.end(1):len(test)]
        #print line
        line = string.replace(line, 'span  relnofollow target_blank', '')
        line = string.replace(line, 'span classswSprite s_extLink spanshop this storespanspanastrongspan', '')
        line = string.join(string.split(line), " ")
        arrayname.append(line)
    else:
        print "the pattern didn't capture any text"


br2 = mechanize.Browser()                # Create a browser
br2.open(NORMAL_URL)            # Open the login page
print br2.geturl()


datasheet2 = br2.response().read()

#print datasheet

root2 = lxml.html.fromstring(datasheet2)


prodimage = root2.cssselect("td.productImage a img")

for index, item in enumerate(prodimage):
    varprodimage = item.attrib.get("src")
    arrayimage.append(varprodimage)

print arrayname
print arrayprice
print arraywant
print arraygot
print arrayprior
print arrayimage


print "There are %d items on your shopping list" % len(prodstring)


scraperwiki.sqlite.execute("drop table if exists swdata")

for index, item in enumerate(arrayname):
        
    varfinalname = arrayname[index]
    varfinalcatno = "n/a"
    varfinalquantity = int(arraywant[index]) - int(arraygot[index])
    varfinalquantitymax = int(arraywant[index])
    varfinalprice = arrayprice[index]
    varfinalimage = arrayimage[index]


    dataArray = { "productName":varfinalname, "catNo":varfinalcatno, "quantity":varfinalquantity, "quantitymax":varfinalquantitymax, "price":varfinalprice, "image":varfinalimage}
    print dataArray
    

    scraperwiki.sqlite.save(unique_keys=["productName"], data=dataArray)
   
print scraperwiki.sqlite.select("* from swdata")from __future__ import division
import sys, time, os
import mechanize
import lxml.html
import string
import scraperwiki


COMPACT_URL = 'http://www.amazon.co.uk/registry/wishlist/31LBH13Q90O5Q/ref=cm_wl_act_vv?_encoding=UTF8&filter=all&sort=date-added&layout=compact&visitor-view=1&reveal=all'
NORMAL_URL = 'http://www.amazon.co.uk/registry/wishlist/31LBH13Q90O5Q?visitor-view=1&reveal=all&filter=all&sort=date-added&layout=standard&x=9&y=13'
GIFTLISTNO = '442551'

br = mechanize.Browser()                # Create a browser
br.open(COMPACT_URL)            # Open the login page
print br.geturl()


datasheet = br.response().read()

#print datasheet

root = lxml.html.fromstring(datasheet)


prodstring = root.cssselect("tbody.itemWrapper span.productTitle")
print prodstring

prodtiny = root.cssselect("tbody.itemWrapper td.tiny")
print prodtiny

#INTEGER CHECK FUNCTION
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

#print RepresentsInt("+123")

#print RepresentsInt("10.0")

arrayprice = []
arraywant = []
arraygot = []
arrayprior = []
arrayname = []
arrayimage = []

for index, item in enumerate(prodtiny):
    varprodstrip = lxml.html.tostring(item)

    varprodstrip = string.replace(varprodstrip, '<td class="tiny"><span class="price"><strong>&#163;', '')
    varprodstrip = string.replace(varprodstrip, '</strong></span></td>', '')

    varprodstrip = string.replace(varprodstrip, '<td align="center" class="tiny">', '')
    varprodstrip = string.replace(varprodstrip, '</td>', '')
    varprodstrip = string.replace(varprodstrip, ' ', '')
    varprodstrip = string.join(string.split(varprodstrip), "")
    
    varprodpriceno = (index+4)%4
    varprodwantno = (index+3)%4
    varprodgotno = (index+2)%4
    varprodpriorno = (index+1)%4

    tinystring = "Tiny String = %s --- " % varprodstrip
    tinystring+= "index = %d --- " % index
    tinystring+= "After Sum Price - %d --- " % varprodpriceno
    tinystring+= "After Sum Want - %d --- " % varprodwantno
    tinystring+= "After Sum Got - %d" % varprodgotno
    tinystring+= "After Sum Prior - %d" % varprodpriorno
    print tinystring

    if varprodpriceno==0:
        print ' - divisible by 4 - price %s'% varprodstrip
        arrayprice.append(varprodstrip)

    if varprodwantno==0:
        print ' - divisible by 4 - want %s'% varprodstrip
        arraywant.append(varprodstrip)

    if varprodgotno==0:
        print ' - divisible by 4 - got %s'% varprodstrip
        arraygot.append(varprodstrip)

    if varprodpriorno==0:
        print ' - divisible by 4 - prior %s'% varprodstrip
        arrayprior.append(varprodstrip)

for index, item in enumerate(prodstring):
    varnamestrip = lxml.html.tostring(item)
    varnamestrip = string.replace(varnamestrip, '=', '')
    varnamestrip = string.replace(varnamestrip, '"', '')
    varnamestrip = string.replace(varnamestrip, '<', '')
    varnamestrip = string.replace(varnamestrip, '>', '')
    varnamestrip = string.replace(varnamestrip, '/', '')

    pat2 = 'word1\s(.*)\sword2'
    test2 = 'word1 will never be a word2'
    repl2 = 'replace'
    
    #span classsmall productTitlestronga
    pat = 'span\s(.*)\srelnofollow'
    test = varnamestrip
    repl = ''
   

    import re
    m = re.search(pat,test)
    
    if m and m.groups() > 0:
        line = test[0:m.start(1)] + repl + test[m.end(1):len(test)]
        #print line
        line = string.replace(line, 'span  relnofollow target_blank', '')
        line = string.replace(line, 'span classswSprite s_extLink spanshop this storespanspanastrongspan', '')
        line = string.join(string.split(line), " ")
        arrayname.append(line)
    else:
        print "the pattern didn't capture any text"


br2 = mechanize.Browser()                # Create a browser
br2.open(NORMAL_URL)            # Open the login page
print br2.geturl()


datasheet2 = br2.response().read()

#print datasheet

root2 = lxml.html.fromstring(datasheet2)


prodimage = root2.cssselect("td.productImage a img")

for index, item in enumerate(prodimage):
    varprodimage = item.attrib.get("src")
    arrayimage.append(varprodimage)

print arrayname
print arrayprice
print arraywant
print arraygot
print arrayprior
print arrayimage


print "There are %d items on your shopping list" % len(prodstring)


scraperwiki.sqlite.execute("drop table if exists swdata")

for index, item in enumerate(arrayname):
        
    varfinalname = arrayname[index]
    varfinalcatno = "n/a"
    varfinalquantity = int(arraywant[index]) - int(arraygot[index])
    varfinalquantitymax = int(arraywant[index])
    varfinalprice = arrayprice[index]
    varfinalimage = arrayimage[index]


    dataArray = { "productName":varfinalname, "catNo":varfinalcatno, "quantity":varfinalquantity, "quantitymax":varfinalquantitymax, "price":varfinalprice, "image":varfinalimage}
    print dataArray
    

    scraperwiki.sqlite.save(unique_keys=["productName"], data=dataArray)
   
print scraperwiki.sqlite.select("* from swdata")