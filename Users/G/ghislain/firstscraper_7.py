import scraperwiki
import lxml.html
import urlparse
import re

urlb = 'http://eventmedia.eurecom.fr/'
url2012= ['http://eventmedia.eurecom.fr/', 'http://papos.space.noa.gr/fend_static/', 'http://www.dublinked.ie/sandbox/SemanticWebChall/index.php', 'http://www.streamreasoning.org/demos/london2012', 'http://www.superstreamcollider.org/', 'http://m.railgb.org.uk/', 'http://sswap.info/','http://kebap.ke.informatik.tu-darmstadt.de:8080/LODATC/query/index','http://activehiring.labs.exalead.com/', 'https://sites.google.com/site/semanticsmartaleck/', 'http://www.semanticwebservices.org/enalgae/', 'http://swget.inf.unibz.it/blazeds/swget/swget.html ', 'http://kebap.ke.informatik.tu-darmstadt.de:8080/semantic-browser/query/index', 'http://139.91.183.72/x-ens/', 'http://lsm.deri.ie/', 'http://larkc.cefriel.it/lbsma/bottari/', 'http://wit.istc.cnr.it/aemoo/', 'http://boowa.com/', 'http://our.kisti.re.kr/login/login_nor.jsp', 'http://mbw.molgen.mpg.de/wiki/Maps', 'http://robodb.fruitcakesites.nl/' ]
data = {}
scripts = [ ]
content = " "
for url in url2012:
     
     try:
         #for element in root.cssselect("script"):
            #scripts.append(element.attrib['src'])
           # print scripts
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        title = root.cssselect("title")
          
               
     except: 
        continue
     titre = title[0].text_content()

     if len(titre) < 1:
        continue
     #try:
         #for desc in root.cssselect("meta"):
             #print desc[0].text_content()
             #content = desc[0].text_content()
             #if len(content) < 1:
                #description = "null"
     #except:
         #continue

     

     
     

     data = {'href' : url,
             'titre' : titre 
             }   
     

     scraperwiki.sqlite.save(unique_keys=['href'], data=data)

#htmlb = scraperwiki.scrape(urlb)
#rootb = lxml.html.fromstring(htmlb)
#scripts = [ ]
#for element in rootb.cssselect("script"):
    #print element.attrib['src']
    #scripts.append(element.attrib['src'])
    #print scripts
    #print lxml.html.tostring(element)
    
    
   import scraperwiki
import lxml.html
import urlparse
import re

urlb = 'http://eventmedia.eurecom.fr/'
url2012= ['http://eventmedia.eurecom.fr/', 'http://papos.space.noa.gr/fend_static/', 'http://www.dublinked.ie/sandbox/SemanticWebChall/index.php', 'http://www.streamreasoning.org/demos/london2012', 'http://www.superstreamcollider.org/', 'http://m.railgb.org.uk/', 'http://sswap.info/','http://kebap.ke.informatik.tu-darmstadt.de:8080/LODATC/query/index','http://activehiring.labs.exalead.com/', 'https://sites.google.com/site/semanticsmartaleck/', 'http://www.semanticwebservices.org/enalgae/', 'http://swget.inf.unibz.it/blazeds/swget/swget.html ', 'http://kebap.ke.informatik.tu-darmstadt.de:8080/semantic-browser/query/index', 'http://139.91.183.72/x-ens/', 'http://lsm.deri.ie/', 'http://larkc.cefriel.it/lbsma/bottari/', 'http://wit.istc.cnr.it/aemoo/', 'http://boowa.com/', 'http://our.kisti.re.kr/login/login_nor.jsp', 'http://mbw.molgen.mpg.de/wiki/Maps', 'http://robodb.fruitcakesites.nl/' ]
data = {}
scripts = [ ]
content = " "
for url in url2012:
     
     try:
         #for element in root.cssselect("script"):
            #scripts.append(element.attrib['src'])
           # print scripts
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        title = root.cssselect("title")
          
               
     except: 
        continue
     titre = title[0].text_content()

     if len(titre) < 1:
        continue
     #try:
         #for desc in root.cssselect("meta"):
             #print desc[0].text_content()
             #content = desc[0].text_content()
             #if len(content) < 1:
                #description = "null"
     #except:
         #continue

     

     
     

     data = {'href' : url,
             'titre' : titre 
             }   
     

     scraperwiki.sqlite.save(unique_keys=['href'], data=data)

#htmlb = scraperwiki.scrape(urlb)
#rootb = lxml.html.fromstring(htmlb)
#scripts = [ ]
#for element in rootb.cssselect("script"):
    #print element.attrib['src']
    #scripts.append(element.attrib['src'])
    #print scripts
    #print lxml.html.tostring(element)
    
    
   