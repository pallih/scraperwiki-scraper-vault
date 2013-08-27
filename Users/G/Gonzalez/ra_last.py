import scraperwiki           
import lxml.html





#Function to get all links

def scrape_and_look_for_next_link(url,start,stop):
    counter = 0
    for start in range(start +1 , stop +1 ):
            next_url = url + "#selected=" + str(start)
            print next_url
            apt = {}
            html = scraperwiki.scrape(next_url)
            root = lxml.html.fromstring(html)
            #counter = 0
            for row in root.cssselect("li.btn-vermas a"):
                link = row.attrib.get('href')
                #print link               
                apt['url'] = str("www.metroscubicos.com") +  str(link)
                counter += 1
                apt['counter'] = counter
                #print apt['url'], '-----------------'
                unique_keys=['counter']    
                scraperwiki.sqlite.save(unique_keys, apt)

url = "http://www.metroscubicos.com/resultados/distrito-federal/en-renta?propertyType=Departamento&sid=1369407545"
scrape_and_look_for_next_link(url,0,2)import scraperwiki           
import lxml.html





#Function to get all links

def scrape_and_look_for_next_link(url,start,stop):
    counter = 0
    for start in range(start +1 , stop +1 ):
            next_url = url + "#selected=" + str(start)
            print next_url
            apt = {}
            html = scraperwiki.scrape(next_url)
            root = lxml.html.fromstring(html)
            #counter = 0
            for row in root.cssselect("li.btn-vermas a"):
                link = row.attrib.get('href')
                #print link               
                apt['url'] = str("www.metroscubicos.com") +  str(link)
                counter += 1
                apt['counter'] = counter
                #print apt['url'], '-----------------'
                unique_keys=['counter']    
                scraperwiki.sqlite.save(unique_keys, apt)

url = "http://www.metroscubicos.com/resultados/distrito-federal/en-renta?propertyType=Departamento&sid=1369407545"
scrape_and_look_for_next_link(url,0,2)import scraperwiki           
import lxml.html





#Function to get all links

def scrape_and_look_for_next_link(url,start,stop):
    counter = 0
    for start in range(start +1 , stop +1 ):
            next_url = url + "#selected=" + str(start)
            print next_url
            apt = {}
            html = scraperwiki.scrape(next_url)
            root = lxml.html.fromstring(html)
            #counter = 0
            for row in root.cssselect("li.btn-vermas a"):
                link = row.attrib.get('href')
                #print link               
                apt['url'] = str("www.metroscubicos.com") +  str(link)
                counter += 1
                apt['counter'] = counter
                #print apt['url'], '-----------------'
                unique_keys=['counter']    
                scraperwiki.sqlite.save(unique_keys, apt)

url = "http://www.metroscubicos.com/resultados/distrito-federal/en-renta?propertyType=Departamento&sid=1369407545"
scrape_and_look_for_next_link(url,0,2)