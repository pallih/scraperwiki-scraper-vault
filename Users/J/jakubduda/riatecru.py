# Riatec.ru

import scraperwiki 
html = scraperwiki.scrape("http://www.cdu.ru/en/") 

import lxml.html 
root = lxml.html.fromstring(html) 

for bl in root.cssselect("div.informerBlock"):
    for el in bl:
        className = el.attrib['class']
        if className == "informerTitle":
            title=el.text
        elif className == "informerData":
            data=el.text
        else:
            for subel in el:
                if subel.attrib['class'] == "infoName viewGraph":
                    item=subel[0].text
                if subel.attrib['class'] == "infoNum":
                    number=subel.text
                elif subel.attrib['class'] == "infoChange":
                    print title,data[:10],data[11:],item,number,subel.text
                    outdata={'title':title,'date':data[:10],'unit':data[11:],'item':item,'level':number,'change':subel.text}
                    scraperwiki.sqlite.save(unique_keys=['title','date','item'], data=outdata)

# Riatec.ru

import scraperwiki 
html = scraperwiki.scrape("http://www.cdu.ru/en/") 

import lxml.html 
root = lxml.html.fromstring(html) 

for bl in root.cssselect("div.informerBlock"):
    for el in bl:
        className = el.attrib['class']
        if className == "informerTitle":
            title=el.text
        elif className == "informerData":
            data=el.text
        else:
            for subel in el:
                if subel.attrib['class'] == "infoName viewGraph":
                    item=subel[0].text
                if subel.attrib['class'] == "infoNum":
                    number=subel.text
                elif subel.attrib['class'] == "infoChange":
                    print title,data[:10],data[11:],item,number,subel.text
                    outdata={'title':title,'date':data[:10],'unit':data[11:],'item':item,'level':number,'change':subel.text}
                    scraperwiki.sqlite.save(unique_keys=['title','date','item'], data=outdata)

