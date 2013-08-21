import scraperwiki
import lxml.html


# Blank Python
x=0
string = ''
for x in xrange(41,43):
    if 'N/A%' in string:
        null= 0
        a= "http://www.lcbo.com/lcbo-ear/lcbo/product/details.do?language=EN&itemNumber="+str(x)
        html = scraperwiki.scrape(a)
        string =''
        
        root = lxml.html.fromstring(html)
        tds = root.cssselect('br')
        print tds.text_content()
        
            
        for tr in tds:
            if (str(lxml.html.tostring(tr)) == '<br>') or (str(lxml.html.tostring(tr)) == '<br>&#13; Made in: &#13;')or (str(lxml.html.tostring(tr)) == '<br>&#13; By: &#13;') or (str(lxml.html.tostring(tr)) == '<br>&#13; &#13; &#13; &#13; N/A% Alcohol/Vol.') or (str(lxml.html.tostring(tr)) == '<br>&#13; &#160;') or ('&#160' in str(lxml.html.tostring(tr))):
                null =0
            else:
                string = string + lxml.html.tostring(tr)
    else:
        print x
        print string
        scraperwiki.sqlite.save(unique_keys=["a"], data={"a":string})  
        a= "http://www.lcbo.com/lcbo-ear/lcbo/product/details.do?language=EN&itemNumber="+str(x)
        html = scraperwiki.scrape(a)
        string =''
        
        root = lxml.html.fromstring(html)
        tds = root.cssselect('br')
        
            
        for tr in tds:
            if (str(lxml.html.tostring(tr)) == '<br>') or (str(lxml.html.tostring(tr)) == '<br>&#13; Made in: &#13;')or (str(lxml.html.tostring(tr)) == '<br>&#13; By: &#13;') or (str(lxml.html.tostring(tr)) == '<br>&#13; &#13; &#13; &#13; N/A% Alcohol/Vol.') or (str(lxml.html.tostring(tr)) == '<br>&#13; &#160;') or ('&#160' in str(lxml.html.tostring(tr))):
                null =0
            else:
                string = string + lxml.html.tostring(tr)


