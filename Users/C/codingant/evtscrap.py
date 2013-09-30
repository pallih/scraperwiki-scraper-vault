import scraperwiki
import lxml.html 

html = scraperwiki.scrape("http://www.morongocasinoresort.com/entertainment")
root = lxml.html.fromstring(html)
scraperwiki.sqlite.execute("delete from swdata")

node=root.cssselect("div#myEvents")


root=lxml.html.fromstring(lxml.html.tostring(node[0]))

title=root.cssselect("strong")

dumpcontent=root.cssselect("br")
content=[]

for i in dumpcontent:
    if i.tail != None:
        content.append(i.tail)
conten=[]
cont=0
while (cont < len(content)):
    conten.append(content[cont]+" "+content[cont+1])
    cont = cont + 2
    
img=[]        
dump=root.cssselect("div.eventsBox")
for i in dump:
    nod=lxml.html.fromstring(lxml.html.tostring(i))
    imgLink=nod.cssselect("img")
    for el in imgLink:
        img.append( el.attrib['src'])

count = 0
while (count < len(title)):
    data = {
          'sno' : count,  
          'title' : title[count].text,
          'content' : conten[count],
          'imgLink': img[count],
        }
    scraperwiki.sqlite.save(unique_keys=["sno"], data=data)    
    count = count + 1


import scraperwiki
import lxml.html 

html = scraperwiki.scrape("http://www.morongocasinoresort.com/entertainment")
root = lxml.html.fromstring(html)
scraperwiki.sqlite.execute("delete from swdata")

node=root.cssselect("div#myEvents")


root=lxml.html.fromstring(lxml.html.tostring(node[0]))

title=root.cssselect("strong")

dumpcontent=root.cssselect("br")
content=[]

for i in dumpcontent:
    if i.tail != None:
        content.append(i.tail)
conten=[]
cont=0
while (cont < len(content)):
    conten.append(content[cont]+" "+content[cont+1])
    cont = cont + 2
    
img=[]        
dump=root.cssselect("div.eventsBox")
for i in dump:
    nod=lxml.html.fromstring(lxml.html.tostring(i))
    imgLink=nod.cssselect("img")
    for el in imgLink:
        img.append( el.attrib['src'])

count = 0
while (count < len(title)):
    data = {
          'sno' : count,  
          'title' : title[count].text,
          'content' : conten[count],
          'imgLink': img[count],
        }
    scraperwiki.sqlite.save(unique_keys=["sno"], data=data)    
    count = count + 1


