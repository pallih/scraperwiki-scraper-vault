import scraperwiki
import lxml.html

  
url = "http://www.raymondcheong.com/rankings/index.html"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
    
    

for main in root.cssselect("table#rankings tr"):


    try:
        temp1 = main[1].text
        temp2 = main[3].text
        temp3 = main[7].text
        temp4 = main[7].text
        temp1 = temp1.partition(' ')[0]
        temp2 = temp2.partition(' ')[0]
        temp3 = temp3.partition(' ')[0]
        temp4 = temp4.partition(' ')[0]
        
        scraperwiki.sqlite.save(unique_keys=["TEAM"], data={"TEAM":temp1, "AASMHCA":temp2,"AASM":temp3, "ASM":temp4})
    except IndexError:
        pass
    
    except TypeError:
        pass
