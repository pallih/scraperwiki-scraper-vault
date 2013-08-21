import scraperwiki
import lxml.html
import math
import multiprocessing 
import time
import sys
from multiprocessing import Process


# Blank Python

propertylisttemp = multiprocessing.Queue()
properties = []
propertylist = []
pool= []

scraperwiki.sqlite.execute("DROP TABLE properties")

scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS properties ('address' varchar(50) NOT NULL,'bedroom' int,'bathroom' int,'carspace' int,'description' varchar(200),'price' varchar(50),'score' varchar(50), Unique('address','price'))")

#scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS properties ('address' varchar(50) NOT NULL,'bedroom' int,'bathroom' int,'carspace' int,'description' varchar(200),'price' varchar(50))")

#class consumer(multiprocessing.Process):
#    def __init__(self):
#        multiprocessing.Process.__init__(self)


#    def run(self):
#        print ' start work'
#        s = True
#       while s:
#           while  propertylisttemp.qsize() > 0:
#                t = propertylisttemp.get()
#                if t == 'None':
#                    s=False
#                    return
#                properties.append(t)
#                #scraperwiki.sqlite.save(unique_keys=[], data={"address":t[0], "bedroom":t[1],"bathroom":t[2],"carspace":t[3],"description":t[4],"price":t[5]},table_name="properties") 
#            time.sleep(2)
#            print ' going to sleep' 

class scraper(multiprocessing.Process):
    def __init__(self, i):
        multiprocessing.Process.__init__(self)
        self.i = i

    def run(self):
        html = scraperwiki.scrape(path+"?page="+str(self.i))
        root = lxml.html.fromstring(html)
        temp = root.xpath("//*[contains(concat(' ', @class, ' '), 's-listing')]")
        for tr in temp:
            property =[]
            address = tr.cssselect("h3>a")
            tempaddress = address[0].text
            tempaddress = tempaddress.replace("/","-")
            tempaddress = tempaddress.replace(" ","-")
            tempaddress = tempaddress.replace(",","-")
            print tempaddress
            try:
                scorehtml = scraperwiki.scrape("http://www.walkscore.com/score/"+ tempaddress)
                scoreroot = lxml.html.fromstring(scorehtml)
                scoretemp = scoreroot.cssselect("span[class='score ']")[0].text
            except:
                scoretemp=""
            #scoretemp=""
            property.append(address[0].text)
            property.append(tr.cssselect("dd[class='bedrooms']")[0].text)
            property.append(tr.cssselect("dd[class='bathrooms']")[0].text)
            property.append(tr.cssselect("dd[class='carspaces']")[0].text)
            try:
                property.append(tr.cssselect("div[class='description']>h5")[0].text)
            except:
                property.append(" ")
            try:
                property.append(tr.cssselect("div[class='description']>h4")[0].text)
            except:
                property.append(" ")
            
            property.append(scoretemp)

            data ={ "address":property[0],
                    "bedroom":property[1],
                    "bathroom":property[2],
                    "carspace":property[3],
                    "description":property[4],
                    "price":property[5],
                    "score":property[6]
                   }
            propertylisttemp.put(data)



#suburbs = ["Coopers-Plains/Holland-Park/Holland-Park-West/Mansfield/Mount-Gravatt/Upper-Mount-Gravatt/Holland-Park/Holland-Park-West"]
#suburbs = ["Coopers-Plains"]

#suburbs = ["Acacia-Ridge","Algester","Annerley","Archerfield","Berrinba","Burbank","Calamvale","Carole-Park","Coopers-Plains","Darra","Doolandella","Drewvale","Durack","Dutton-Park","Eight-Mile-Plains","Ellen-Grove","Fairfield","Forest-Lake","Greenslopes","Heathwood","Holland-Park","Holland-Park-West","Inala","Karawatha","Kuraby","Larapinta","Macgregor","Mackenzie","Mansfield","Moorooka","Mount-Gravatt","Mount-Gravatt-East","Nathan","Oxley","Pallara","Parkinson","Richlands","Robertson","Rochedale","Rocklea","Runcorn","Salisbury","Seventeen-Mile-Rocks","Sinnamon-Park","Stretton","Sumner","Sunnybank","Sunnybank-Hills","Tarragindi","Tennyson","Upper-Mount-Gravatt","Wacol","Willawong","Wishart","Yeerongpilly","Yeronga"]

suburbs = ["Acacia-Ridge/Algester/Annerley/Archerfield/Berrinba/Burbank/Calamvale/Carole-Park/Coopers-Plains/Darra/","Doolandella/Drewvale/Durack/Dutton-Park/Eight-Mile-Plains/Ellen-Grove/Fairfield/Forest-Lake/Greenslopes/Heathwood/","Holland-Park/Holland-Park-West/Inala/Karawatha/Kuraby/Larapinta/Macgregor/","Mackenzie/Mansfield/Moorooka/Mount-Gravatt/","Mount-Gravatt-East/Nathan/Oxley/Pallara/Parkinson/Richlands/Robertson/Rochedale/Rocklea/Runcorn/Salisbury/Seventeen-Mile-Rocks/","Sinnamon-Park/Stretton/Sumner/Sunnybank/Sunnybank-Hills/Tarragindi/Tennyson/Upper-Mount-Gravatt/Wacol/","Willawong/Wishart/Yeerongpilly/Yeronga"]


for sub in suburbs:
    try:
        path = "http://www.domain.com.au/Search/buy/State/QLD/Area/Southside/Region/Brisbane-Region/Suburb/" + sub +"/"
        html = scraperwiki.scrape(path)
        root = lxml.html.fromstring(html)
        totalprop = int(root.cssselect("h1>em")[0].text)
        print sub + " " + str(totalprop)
        for i in range(1,int(math.floor(totalprop/14))+2):
            t = scraper(i)    
            t.start()
            pool.append(t)
    except:
        pass

    for t in pool:
        print "shutdown"
        t.join()
    
    #for p in pool:
    #    p.join(timeout=1)
    #    if not p.is_alive():
    #        break
    #    print '.',
    #    sys.stdout.flush()
    
    while  propertylisttemp.qsize() > 0:
        properties.append( propertylisttemp.get())
    
    
    print len(properties)
    
    scraperwiki.sqlite.save(unique_keys=["address","price"], data=properties, table_name="properties")   
    
    scraperwiki.sqlite.commit() 
