import scraperwiki
import lxml.html

for k in range(1, 343778):
    d = ""

    try:
        html = scraperwiki.scrape("http://soccerdatabase.eu/player/" + str(k))
        root = lxml.html.fromstring(html)
        
        i = 0
        
        for el in root.cssselect("table.tableContent td div"):
            if i != 1 and i != 2:
                if (i == 3 and el.text.find('(') != -1):
                    if el.text[:2].isdigit():
                        d = d + el.text[:2] + ", "
                    else:
                        if el.text[0].isdigit():
                            d = d + el.text[0] + ", "
                else:
                    d = d + el.text.strip() + ", "
            else:
                if len(el.getchildren()) > 0:
                    if el.getchildren()[0].tag == "span":
                        d = d + el.getchildren()[0].getchildren()[0].text.strip() + ", "
                    else:
                        d = d + el.getchildren()[0].text.strip() + ", "
        
            i = i + 1
            if i == 5:
                i = 0
                d = d + '\n'
        print d
    except Exception:
        pass

            



import scraperwiki
import lxml.html

for k in range(1, 343778):
    d = ""

    try:
        html = scraperwiki.scrape("http://soccerdatabase.eu/player/" + str(k))
        root = lxml.html.fromstring(html)
        
        i = 0
        
        for el in root.cssselect("table.tableContent td div"):
            if i != 1 and i != 2:
                if (i == 3 and el.text.find('(') != -1):
                    if el.text[:2].isdigit():
                        d = d + el.text[:2] + ", "
                    else:
                        if el.text[0].isdigit():
                            d = d + el.text[0] + ", "
                else:
                    d = d + el.text.strip() + ", "
            else:
                if len(el.getchildren()) > 0:
                    if el.getchildren()[0].tag == "span":
                        d = d + el.getchildren()[0].getchildren()[0].text.strip() + ", "
                    else:
                        d = d + el.getchildren()[0].text.strip() + ", "
        
            i = i + 1
            if i == 5:
                i = 0
                d = d + '\n'
        print d
    except Exception:
        pass

            



