import scraperwiki
import lxml.html

  
url = "http://www.hkjc.com/english/racing/Horse.asp?HorseNo=M113"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
    
    

for main in root.cssselect("table.bigborder tr"):


    try:
        print len(main)
        
        #scraperwiki.sqlite.save(unique_keys=["TEAM"], data={"TEAM":temp1, "AASMHCA":temp2,"AASM":temp3, "ASM":temp4})
    except IndexError:
        print "NULL"
        pass
    
    except TypeError:
        print "NULL"
        pass
