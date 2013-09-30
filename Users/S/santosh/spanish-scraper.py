import scraperwiki
import string
import scraperwiki
#import json #for json decoding
from lxml import etree     
from cStringIO import StringIO
import urllib
i=0
searchList=["hospitales", "laboratorio", "medicina+natural", "ortodoncia", "ecografia", "clinicas+y+hospitales", "centros+de+salud"]
for eachitem in searchList:
    for i in range(1,20):
        strAddr = "http://www.paginasamarillas.com.pe/s/"+eachitem+"/"+str(i)+"/50"
        html = urllib.urlopen(strAddr)
        html = html.read()
        parser = etree.HTMLParser()
        tree   = etree.parse(StringIO(html), parser)
        print tree
        mainContent = tree.xpath("//div[@class='resultados']")[0]
        
        print mainContent
        
        contentHTML= (etree.tostring(mainContent, pretty_print=True))
        
        print contentHTML
        
        tree   = etree.parse(StringIO(contentHTML), parser)
        hospitals = tree.xpath("//div[@class='texto-bus-pago']")
        print hospitals
        
        mylist=[]
        for eachHospitals in hospitals:
            dictionary = {}
            contentHTML= (etree.tostring(eachHospitals, pretty_print=True))
            tree   = etree.parse(StringIO(contentHTML), parser)
            dictionary['name']=tree.xpath("//h2/a/text()")[0].strip()
            dictionary['link']=tree.xpath("//h2/a/@href")[0].strip()
            mylist.append(dictionary)
        
        for dictionary in mylist:
            url="http://www.paginasamarillas.com.pe/"+dictionary['link']
            html = urllib.urlopen(url)
            html = html.read()
            infoList = []
            parser = etree.HTMLParser()
            tree   = etree.parse(StringIO(html), parser)
            maininfo = tree.xpath("//div[@class='uno']")
            
            for eachinfo in maininfo:
                contentHTML= (etree.tostring(eachinfo, pretty_print=True))
                tree   = etree.parse(StringIO(contentHTML), parser)
                cond=tree.xpath("//p[@class='mas-datos']/text()")[0].strip()
                while cond!="Direcciones y Teléfonos:":
                    info=tree.xpath("//p[@class='detalle']/descendant-or-self::*/text()")[0].strip()
            infoList.append(info)
            dictionary["i"]=str(i)       
            dictionary['info'] =  ':'.join(infoList)
            print dictionary
            scraperwiki.sqlite.save(unique_keys=["i"], data=dictionary)
            i=i+1import scraperwiki
import string
import scraperwiki
#import json #for json decoding
from lxml import etree     
from cStringIO import StringIO
import urllib
i=0
searchList=["hospitales", "laboratorio", "medicina+natural", "ortodoncia", "ecografia", "clinicas+y+hospitales", "centros+de+salud"]
for eachitem in searchList:
    for i in range(1,20):
        strAddr = "http://www.paginasamarillas.com.pe/s/"+eachitem+"/"+str(i)+"/50"
        html = urllib.urlopen(strAddr)
        html = html.read()
        parser = etree.HTMLParser()
        tree   = etree.parse(StringIO(html), parser)
        print tree
        mainContent = tree.xpath("//div[@class='resultados']")[0]
        
        print mainContent
        
        contentHTML= (etree.tostring(mainContent, pretty_print=True))
        
        print contentHTML
        
        tree   = etree.parse(StringIO(contentHTML), parser)
        hospitals = tree.xpath("//div[@class='texto-bus-pago']")
        print hospitals
        
        mylist=[]
        for eachHospitals in hospitals:
            dictionary = {}
            contentHTML= (etree.tostring(eachHospitals, pretty_print=True))
            tree   = etree.parse(StringIO(contentHTML), parser)
            dictionary['name']=tree.xpath("//h2/a/text()")[0].strip()
            dictionary['link']=tree.xpath("//h2/a/@href")[0].strip()
            mylist.append(dictionary)
        
        for dictionary in mylist:
            url="http://www.paginasamarillas.com.pe/"+dictionary['link']
            html = urllib.urlopen(url)
            html = html.read()
            infoList = []
            parser = etree.HTMLParser()
            tree   = etree.parse(StringIO(html), parser)
            maininfo = tree.xpath("//div[@class='uno']")
            
            for eachinfo in maininfo:
                contentHTML= (etree.tostring(eachinfo, pretty_print=True))
                tree   = etree.parse(StringIO(contentHTML), parser)
                cond=tree.xpath("//p[@class='mas-datos']/text()")[0].strip()
                while cond!="Direcciones y Teléfonos:":
                    info=tree.xpath("//p[@class='detalle']/descendant-or-self::*/text()")[0].strip()
            infoList.append(info)
            dictionary["i"]=str(i)       
            dictionary['info'] =  ':'.join(infoList)
            print dictionary
            scraperwiki.sqlite.save(unique_keys=["i"], data=dictionary)
            i=i+1