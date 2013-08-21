import scraperwiki
import lxml.html


html = scraperwiki.scrape("http://sueddeutsche.de")
root = lxml.html.fromstring(html)

for el in root.cssselect("div.teaser a strong"):
    aufm = None
    exclusiv = None

    sub= el.text #subtitel
    
    if sub is not None:
        head= el.getnext() #em headline

#aufmacher suchen
        auf= el.getparent()
        auf= auf.getnext()
        if auf is not None:
            print auf.tag      
            
            if auf.text is not None:
                kind = auf[0] #child of aufmacher
                exclusiv = kind.tail #tail of exclusiv
                aufm = auf.text #aufmacher text
            


    data = {
    'headline' : head.text,
    'sub' : sub,
    'exclusivmeinung' : exclusiv,
    'aufmacher' : aufm
   
    }
    print data 
    scraperwiki.sqlite.save(unique_keys=['headline'], data=data) 
