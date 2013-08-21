import scraperwiki

# testing
# Blank Python

import lxml.html

#parse url
url = "http://en.wikipedia.org/wiki/List_of_Chinese_municipalities_and_prefecture-level_divisions_by_GDP_per_capita"
root = lxml.html.parse(url).getroot()
print root

#some basic manipulations
docstr = lxml.html.tostring(root)
print docstr
docxml = lxml.html.document_fromstring(docstr)
print docxml


scraperwiki.sqlite.execute("drop table if exists swdata")


#tree = lxml.html.parse("http://http://en.wikipedia.org/wiki/List_of_Chinese_municipalities_and_prefecture-#level_divisions_by_GDP_per_capita")



#for a in docxml.xpath("//td[@style='text-align: left;']"):
#    print a.text
#    scraperwiki.sqlite.save(['url'], {'name': a.text, 'url': 'http://en.wikipedia.org%s' % a.attrib['href'] })




# 1. this works
#for el in root.cssselect("div.mw-content-ltr table"):           
#    print el


# 2. this also works
#for el in root.cssselect("div.mw-content-ltr tr"):           
#     tds = el.cssselect("td")       
#     print tds


# 3.  this works to print out string contents of table rows
#for el in root.cssselect("div.mw-content-ltr tr"):           
    #print lxml.html.tostring(el)
    #print el[0].text_content


# 4.  this prints none
#for el in root.cssselect("div.mw-content-ltr tr"):           
#     print el.text

# 5.  this prints text of table cells
#for el in root.cssselect("div.mw-content-ltr td"):           
#     print el.text

# 5b.  this prints text of table cells using higher level in root
#for el in root.cssselect("div.mw-body td"):           
#     print el.text

# 5c. another way of getting text of table cells using xpath this returns a single value
#div = root.xpath( '//div[@class="mw-content-ltr"]' )
#for td in div:
#      print td.xpath('//td[@style="text-align: left;"]')[1].text

# 5d. another way of getting text of table cells using xpath this returns all values
#div = root.xpath( '//div[@class="mw-content-ltr"]' )
#for td in div:
#     for item in td.xpath('//td[@style="text-align: left;"]'):
#          print item.text

# 5e. another way of getting text of table cells using xpath this returns all values
# N.B. use text_content NOT text
#div = root.xpath( '//div[@class="mw-content-ltr"]' )
#for td in div:
#     for item in td.xpath('//td'): 
#        print len(item),item.text_content()


# 5e. another way of getting text of table cells using xpath this returns all values
# N.B. use text_content NOT text
#div = root.xpath( '//div[@class="mw-content-ltr"]' )
#for td in div:
#     for item in td.xpath('//td'): 
#          if len(item)==1:
#               #print item.text_content()
#               data = {
#                    'city' : item.text_content()
#                    }
#               scraperwiki.sqlite.save(unique_keys=['city'], data=data)
#               #scraperwiki.sqlite.save(unique_keys=["Name"],data={"Name":item.text_content()}) 


# 5e. another way of getting text of table cells using xpath this returns all values
# N.B. use text_content NOT text
div = root.xpath( '//div[@class="mw-content-ltr"]' )
for td in div:
     for item in td.xpath('//tr'): 
          print item.text_content()
          #if len(item)==1:
               #print item.text_content()
               #data = {
               #     'city' : item.text_content()
               #     }
               #scraperwiki.sqlite.save(unique_keys=['city'], data=data)
               #scraperwiki.sqlite.save(unique_keys=["Name"],data={"Name":item.text_content()}) 




# 6.  this prints text of table cells
#for el in root.cssselect("div.mw-content-ltr td"):           
#     scraperwiki.sqlite.save(unique_keys=["a"], data={"a":1, "bbb":"Hi there"})
#     if el.text<>"None": 
#         scraperwiki.sqlite.save(unique_keys=["a"], data={"a":el.text, "bbb":el.text})
#     print len(el), el.text


# 7. extracts first elements
#for el in root:          
    #print el.tag
    #for el2 in el:
        #print "--", el2.tag, el2.attrib


# 8. extracts second elements
#for el in root:          
    #print el.tag
    #for el2 in el:
        #print "--", el2.tag, el2.attrib
        #for el3 in el2:
            #print "---", el3.tag, el3.attrib
            #for el4 in el3:
                #print "----", el4.tag, el4.attrib
                #for el5 in el4:
                    #print "-----", el5.tag, el5.attrib
                    #for el6 in el5:
                        #print "------", el6.tag, el6.attrib
                        #for el7 in el6:
                            #print "-------", el7.tag, el7.attrib
                            #for el8 in el7:
                                #print "--------", el8.tag, el8.attrib
                                #for el9 in el8:
                                    #print "---------", el9.tag, el9.attrib
      

#9. in development stage
#code snippet
#view-source:https://scraperwiki.com/editor/raw/test_328
#import scraperwiki
#html = scraperwiki.scrape("http://en.wikipedia.org/wiki/List_of_Chinese_municipalities_and_prefecture-#level_divisions_by_GDP_per_capita")
#print html

#import lxml.html
#root = lxml.html.fromstring(html)
#print root
#for tr in root.cssselect("div[align='left'] tr"):
#    print tr
#    tds = tr.cssselect("td")
#    print tds.text
#    if len(tds)==12:
#        data = {
#            'country' : tds[0].text_content(),
#            'years_in_school' : int(tds[4].text_content())
#        }
#        scraperwiki.sqlite.save(unique_keys=['country'], data=data)
####################################################################




# all paragraphs with class="kkk"
#paras = root.cssselect("table.sortable wikitable jquery-tablesorter")

#print paras
#for p in paras:
#    print (p.tag, p.attrib.get("id"), p.text)

# For more, click on Quick help and select lxml cheat sheet



#root = lxml.html.fromstring(html)


#for tr in root.cssselect("div[align='right'] tr"):
#    tds = tr.cssselect("td")
#    if len(td) > 0:
#        data = {
#            'Municipality/Division' : td[0].text_content()
#        }
#        print data








#print root.cssselect("body")


# all paragraphs with class="kkk"
paras = root.cssselect("toc")

#print paras
#for p in paras:
#    print (p.tag, p.attrib.get("id"), p.text)

# For more, click on Quick help and select lxml cheat sheet



#html = scraperwiki.scrape("http://en.wikipedia.org/wiki/List_of_Chinese_municipalities_and_prefecture-level_divisions_by_GDP_per_capita")
           
#root = lxml.html.fromstring(html)
#for tr in root.cssselect("div[align='left'] tr"):
#    tds = tr.cssselect("td")
#    if len(tds)==12:
#        data = {
#            'Municipality/Division' : tds[0].text_content(),
#            'years_in_school' : int(tds[4].text_content())
#        }
#        print data


#code snippet
#view-source:https://scraperwiki.com/editor/raw/test_328
#import scraperwiki
#html = #scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
#print html

#import lxml.html
#root = lxml.html.fromstring(html)
#for tr in root.cssselect("div[align='left'] tr"):
#    tds = tr.cssselect("td")
#    if len(tds)==12:
#        data = {
#            'country' : tds[0].text_content(),
#            'years_in_school' : int(tds[4].text_content())
#        }
#        scraperwiki.sqlite.save(unique_keys=['country'], data=data)
####################################################################



#tree = lxml.html.parse("http://http://en.wikipedia.org/wiki/List_of_Chinese_municipalities_and_prefecture-level_divisions_by_GDP_per_capita")

#for a in tree.xpath('//html/head'):
#    scraperwiki.sqlite.save(['url'], {'name': a.text, 'url': 'http://en.wikipedia.org%s' % a.attrib['href'] })

