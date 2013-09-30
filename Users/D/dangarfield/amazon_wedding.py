from __future__ import division
import sys, time, os
import mechanize
import lxml.html
import scraperwiki

NORMAL_URL = 'http://www.amazon.co.uk/gp/registry/registry.html?ie=UTF8&type=wedding&id=2KKY3PRYK2Y06'
GIFTLISTNO = '442551'

br = mechanize.Browser()                # Create a browser
br.open(NORMAL_URL)            # Open the login page
print br.geturl()


datasheet = br.response().read()

#print datasheet

root = lxml.html.fromstring(datasheet)

arrayprice = []
arraywant = []
arraygot = []
arrayprior = []
arrayname = []
arrayimage = []

prodimage = root.cssselect("tbody.itemWrapper img")

for index, item in enumerate(prodimage):
    varimagealt = item.attrib.get("alt")
    varimagesrc = item.attrib.get("src")
    if varimagealt == "Product Image":
        arrayimage.append(varimagesrc)



prodname = root.cssselect("tbody.itemWrapper span.regItemTitle strong a")

for index, item in enumerate(prodname):
    varnamestrip = lxml.html.tostring(item)
   # print varnamestrip
    varnamestrip = varnamestrip.replace('=', '')
    varnamestrip = varnamestrip.replace('"', '')
    varnamestrip = varnamestrip.replace('</a>', '')
    varnamestrip = varnamestrip.replace('>', ' endtrigger ')
    varnamestrip = varnamestrip.replace('/', '')
    varnamestrip = varnamestrip.replace('<', '')
    varnamestrip = varnamestrip.replace('a href', 'starttrigger ')

  #  print varnamestrip
    
    #span classsmall productTitlestronga
    pat = 'starttrigger\s(.*)\sendtrigger'
    test = varnamestrip
    repl = ''
   

    import re
    m = re.search(pat,test)
    
    if m and m.groups() > 0:
        line = test[:m.start(1)] + repl + test[m.end(1):]
 #       print line
        line = " ".join(line.split())
        line = line.replace('starttrigger endtrigger ', '')
        
 #       print line
        arrayname.append(line)
    else:
        print "the pattern didn't capture any text"


spantiny = root.cssselect("tbody.itemWrapper td span.tiny")
for index, item in enumerate(spantiny):
    varprodstrip = lxml.html.tostring(item)
    print varprodstrip
    varprodstrip = varprodstrip.replace('<spanclass="tiny">', '')
    varprodstrip = varprodstrip.replace('<span class="tiny">', '')
    varprodstrip = varprodstrip.replace('</span>', '')
    varprodstrip = varprodstrip.replace(' ', '')
    varprodstrip = "".join(varprodstrip.split())

    varprodwantno = (index+1)%2
    varprodgotno = (index)%2


    tinystring = "Tiny String = %s --- " % varprodstrip
    tinystring+= "index = %d --- " % index
    tinystring+= "After Sum Want - %d --- " % varprodwantno
    tinystring+= "After Sum Got - %d" % varprodgotno
    #print tinystring


    if varprodwantno==0:
        #print ' - divisible by 4 - want %s'% varprodstrip
        arraywant.append(varprodstrip)

    if varprodgotno==0:
        #print ' - divisible by 4 - got %s'% varprodstrip
        if not index == 0:
            arraygot.append(varprodstrip)



prodprice = root.cssselect("tbody.itemWrapper td span.regPrice strong")
for index, item in enumerate(prodprice):
    varpricestrip = lxml.html.tostring(item)
    varpricestrip = " ".join(varpricestrip.split())
    varpricestrip = varpricestrip.replace('<strong><span style="color:#000000">Price:</span> &#163;', '')
    varpricestrip = varpricestrip.replace('<br></strong>', '')
    varpricestrip = varpricestrip.replace('<', '')
    varpricestrip = varpricestrip.replace('>', '')
    varpricestrip = varpricestrip.replace('/', '')
    arrayprice.append(varpricestrip )

print arrayimage
print arrayname
print arraywant
print arraygot
print arrayprice



print "There are %d items on your shopping list" % len(arrayname)


scraperwiki.sqlite.execute("drop table if exists swdata")

for index, item in enumerate(arrayname):
        
    varfinalname = arrayname[index]
    varfinalcatno = "n/a"
    varfinalquantity = int(arraywant[index]) - int(arraygot[index])
    varfinalquantitymax = arraywant[index]
    varfinalprice = arrayprice[index]
    varfinalimage = arrayimage[index]


    dataArray = { "productName":varfinalname, "catNo":varfinalcatno, "quantity":varfinalquantity, "quantitymax":varfinalquantitymax, "price":varfinalprice, "image":varfinalimage}
    print dataArray
    

    scraperwiki.sqlite.save(unique_keys=["productName"], data=dataArray)
   
print scraperwiki.sqlite.select("* from swdata")from __future__ import division
import sys, time, os
import mechanize
import lxml.html
import scraperwiki

NORMAL_URL = 'http://www.amazon.co.uk/gp/registry/registry.html?ie=UTF8&type=wedding&id=2KKY3PRYK2Y06'
GIFTLISTNO = '442551'

br = mechanize.Browser()                # Create a browser
br.open(NORMAL_URL)            # Open the login page
print br.geturl()


datasheet = br.response().read()

#print datasheet

root = lxml.html.fromstring(datasheet)

arrayprice = []
arraywant = []
arraygot = []
arrayprior = []
arrayname = []
arrayimage = []

prodimage = root.cssselect("tbody.itemWrapper img")

for index, item in enumerate(prodimage):
    varimagealt = item.attrib.get("alt")
    varimagesrc = item.attrib.get("src")
    if varimagealt == "Product Image":
        arrayimage.append(varimagesrc)



prodname = root.cssselect("tbody.itemWrapper span.regItemTitle strong a")

for index, item in enumerate(prodname):
    varnamestrip = lxml.html.tostring(item)
   # print varnamestrip
    varnamestrip = varnamestrip.replace('=', '')
    varnamestrip = varnamestrip.replace('"', '')
    varnamestrip = varnamestrip.replace('</a>', '')
    varnamestrip = varnamestrip.replace('>', ' endtrigger ')
    varnamestrip = varnamestrip.replace('/', '')
    varnamestrip = varnamestrip.replace('<', '')
    varnamestrip = varnamestrip.replace('a href', 'starttrigger ')

  #  print varnamestrip
    
    #span classsmall productTitlestronga
    pat = 'starttrigger\s(.*)\sendtrigger'
    test = varnamestrip
    repl = ''
   

    import re
    m = re.search(pat,test)
    
    if m and m.groups() > 0:
        line = test[:m.start(1)] + repl + test[m.end(1):]
 #       print line
        line = " ".join(line.split())
        line = line.replace('starttrigger endtrigger ', '')
        
 #       print line
        arrayname.append(line)
    else:
        print "the pattern didn't capture any text"


spantiny = root.cssselect("tbody.itemWrapper td span.tiny")
for index, item in enumerate(spantiny):
    varprodstrip = lxml.html.tostring(item)
    print varprodstrip
    varprodstrip = varprodstrip.replace('<spanclass="tiny">', '')
    varprodstrip = varprodstrip.replace('<span class="tiny">', '')
    varprodstrip = varprodstrip.replace('</span>', '')
    varprodstrip = varprodstrip.replace(' ', '')
    varprodstrip = "".join(varprodstrip.split())

    varprodwantno = (index+1)%2
    varprodgotno = (index)%2


    tinystring = "Tiny String = %s --- " % varprodstrip
    tinystring+= "index = %d --- " % index
    tinystring+= "After Sum Want - %d --- " % varprodwantno
    tinystring+= "After Sum Got - %d" % varprodgotno
    #print tinystring


    if varprodwantno==0:
        #print ' - divisible by 4 - want %s'% varprodstrip
        arraywant.append(varprodstrip)

    if varprodgotno==0:
        #print ' - divisible by 4 - got %s'% varprodstrip
        if not index == 0:
            arraygot.append(varprodstrip)



prodprice = root.cssselect("tbody.itemWrapper td span.regPrice strong")
for index, item in enumerate(prodprice):
    varpricestrip = lxml.html.tostring(item)
    varpricestrip = " ".join(varpricestrip.split())
    varpricestrip = varpricestrip.replace('<strong><span style="color:#000000">Price:</span> &#163;', '')
    varpricestrip = varpricestrip.replace('<br></strong>', '')
    varpricestrip = varpricestrip.replace('<', '')
    varpricestrip = varpricestrip.replace('>', '')
    varpricestrip = varpricestrip.replace('/', '')
    arrayprice.append(varpricestrip )

print arrayimage
print arrayname
print arraywant
print arraygot
print arrayprice



print "There are %d items on your shopping list" % len(arrayname)


scraperwiki.sqlite.execute("drop table if exists swdata")

for index, item in enumerate(arrayname):
        
    varfinalname = arrayname[index]
    varfinalcatno = "n/a"
    varfinalquantity = int(arraywant[index]) - int(arraygot[index])
    varfinalquantitymax = arraywant[index]
    varfinalprice = arrayprice[index]
    varfinalimage = arrayimage[index]


    dataArray = { "productName":varfinalname, "catNo":varfinalcatno, "quantity":varfinalquantity, "quantitymax":varfinalquantitymax, "price":varfinalprice, "image":varfinalimage}
    print dataArray
    

    scraperwiki.sqlite.save(unique_keys=["productName"], data=dataArray)
   
print scraperwiki.sqlite.select("* from swdata")