import scraperwiki
import lxml.html

# Blank Python
html = scraperwiki.scrape("http://www.loc.gov/marc/relators/relaterm.html")
root = lxml.html.fromstring(html)

authorizedList = root.find_class("authorized")
codeList = root.find_class('relator-code')
codeDict = dict()


for i in range(len(authorizedList)):
    codeDict = {
        'type' : authorizedList[i].text_content().lower(), 
        'code' : codeList[i].text_content().replace('[','').replace(']','')
    }
    scraperwiki.sqlite.save(unique_keys=['code'], data=codeDict)






