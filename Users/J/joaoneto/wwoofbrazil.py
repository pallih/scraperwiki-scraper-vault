import scraperwiki

# Blank Python

def extractInfo(infoName, pContent, span):
    if span.text_content() == infoName + ': ':
        findstr = '<span class="style3">' + infoName + ': </span>'
        start = pContent.find(findstr)
        end = content.find('<br>', start)
        return pContent[start + len(findstr):end].lstrip()
    elif span.text_content() == infoName + ':':
        findstr = '<span class="style3">' + infoName + ':</span>'
        start = pContent.find(findstr)
        end = content.find('<br>', start)
        return pContent[start + len(findstr):end].lstrip()
        

html = scraperwiki.scrape("http://www.wwoofbrazil.com/pre_host_farm.htm")

import lxml.html
root = lxml.html.fromstring(html)
for p in root.cssselect("p.style2"):

    content = lxml.html.tostring(p)
    spans = p.cssselect("span.style3")
    
    if len(spans) > 0:
        data = {'id': p.cssselect("strong")[0].text_content()}
        saveData = False
        for span in spans:
            for infoName in {'City', 'State', 'Type of property', 'Crops', 'We speak', 'Description', 'Accomodation', 'Food', 'We are', 'When to come', 'Additional comments', 'Children'}:
                info = extractInfo(infoName, content, span)
                if info != None:
                    saveData = True
                    data[infoName] = info
        if saveData:
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)

