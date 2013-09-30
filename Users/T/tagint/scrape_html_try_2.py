import scraperwiki

# testing
# Blank Python

import lxml.html

#parse url

scraperwiki.sqlite.execute("drop table if exists swdata")

letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
#letters = ['A']

years = ['2009','2010','2011','2012']

months = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
          'august', 'september', 'october', 'november', 'december']

recno = 0


for letter in letters:
    print letter
    #recno = recno + 1
    print recno

    baseurl = "http://uk.advfn.com/exchanges/LSE/"
    url = baseurl + letter 
    print url

    root = lxml.html.parse(url).getroot()
    #print root

    #some basic manipulations
    docstr = lxml.html.tostring(root)
    #print docstr
    docxml = lxml.html.document_fromstring(docstr)
    #print docxml


    
    #div = root.xpath( '//div[@id="A"]' )
    sxpath = "//div[@id=" + '"' + letter + '"' + "]"
    print sxpath
    div = root.xpath(sxpath)


    colnum = 0
    for row in div:
        for cell in row.xpath('//td'):
            colnum = colnum + 1
            if colnum == 1:
                company = cell.text_content()
            else:
                recno = recno + 1
                ticker = cell.text_content()
                colnum = 0
                try:
                    if cell.attrib['class'] == "String Column2 ColumnLast":
                        #print colnum,company,ticker,cell.attrib['class']
                        scraperwiki.sqlite.save(unique_keys=['recno'],data={"recno":recno,"company":company,"ticker":ticker})
                except:
                    pass
                #scraperwiki.sqlite.save(unique_keys=['recno'],data={"recno":recno,"company":company,"ticker":ticker})
            


import scraperwiki

# testing
# Blank Python

import lxml.html

#parse url

scraperwiki.sqlite.execute("drop table if exists swdata")

letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
#letters = ['A']

years = ['2009','2010','2011','2012']

months = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
          'august', 'september', 'october', 'november', 'december']

recno = 0


for letter in letters:
    print letter
    #recno = recno + 1
    print recno

    baseurl = "http://uk.advfn.com/exchanges/LSE/"
    url = baseurl + letter 
    print url

    root = lxml.html.parse(url).getroot()
    #print root

    #some basic manipulations
    docstr = lxml.html.tostring(root)
    #print docstr
    docxml = lxml.html.document_fromstring(docstr)
    #print docxml


    
    #div = root.xpath( '//div[@id="A"]' )
    sxpath = "//div[@id=" + '"' + letter + '"' + "]"
    print sxpath
    div = root.xpath(sxpath)


    colnum = 0
    for row in div:
        for cell in row.xpath('//td'):
            colnum = colnum + 1
            if colnum == 1:
                company = cell.text_content()
            else:
                recno = recno + 1
                ticker = cell.text_content()
                colnum = 0
                try:
                    if cell.attrib['class'] == "String Column2 ColumnLast":
                        #print colnum,company,ticker,cell.attrib['class']
                        scraperwiki.sqlite.save(unique_keys=['recno'],data={"recno":recno,"company":company,"ticker":ticker})
                except:
                    pass
                #scraperwiki.sqlite.save(unique_keys=['recno'],data={"recno":recno,"company":company,"ticker":ticker})
            


