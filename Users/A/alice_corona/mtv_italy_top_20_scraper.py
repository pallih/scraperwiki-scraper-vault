import scraperwiki
import scraperwiki
import scraperwiki
import requests
import lxml.html
html = requests.get('http://classifiche.mtv.it/classifica/hitlist-italia-classifica-singoli/hitlist-italia-singoli-7-gennaio-2012').text
root = lxml.html.fromstring(html)
for item in root.cssselect("span.today") :
    date = item.text_content()
    date2 = date.replace(' ', '-')
    html2 = requests.get('http://classifiche.mtv.it/classifica/hitlist-italia-classifica-singoli/hitlist-italia-singoli' + date2).text
    print date2
    
#root2 = lxml.html.fromstring(html2)
#    for item in root2.cssselect("a.cpChartEntryImage"):
#        song = item.text_content() 
#        print song
    #for item in root2.cssselect("span.pos"):
            #position = item.text_content()
    #for box in root2.cssselect("a"):
            #print date, position
#html3 = requests.get('http://classifiche.mtv.it/classifica/hitlist-italia-classifica-singoli/hitlist-italia-singoli' + date2 + '/pagina-2').text
    #root3 = lxml.html.fromstring(html3)#for item in root3.cssselect("span.pos"):
       #position = item.text_content()
        #print date, position
#for item in root3.cssselect("span.pos"):
    #position2 = item.text_content()
    #for name in root2.cssselect("a"):
#        print date, name.text_content(), 
# Blank Python

import scraperwiki
import scraperwiki
import scraperwiki
import requests
import lxml.html
html = requests.get('http://classifiche.mtv.it/classifica/hitlist-italia-classifica-singoli/hitlist-italia-singoli-7-gennaio-2012').text
root = lxml.html.fromstring(html)
for item in root.cssselect("span.today") :
    date = item.text_content()
    date2 = date.replace(' ', '-')
    html2 = requests.get('http://classifiche.mtv.it/classifica/hitlist-italia-classifica-singoli/hitlist-italia-singoli' + date2).text
    print date2
    
#root2 = lxml.html.fromstring(html2)
#    for item in root2.cssselect("a.cpChartEntryImage"):
#        song = item.text_content() 
#        print song
    #for item in root2.cssselect("span.pos"):
            #position = item.text_content()
    #for box in root2.cssselect("a"):
            #print date, position
#html3 = requests.get('http://classifiche.mtv.it/classifica/hitlist-italia-classifica-singoli/hitlist-italia-singoli' + date2 + '/pagina-2').text
    #root3 = lxml.html.fromstring(html3)#for item in root3.cssselect("span.pos"):
       #position = item.text_content()
        #print date, position
#for item in root3.cssselect("span.pos"):
    #position2 = item.text_content()
    #for name in root2.cssselect("a"):
#        print date, name.text_content(), 
# Blank Python

