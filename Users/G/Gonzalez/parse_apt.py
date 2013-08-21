import scraperwiki           
import lxml.html
import random
import sys, traceback
import uuid
reload(sys)
sys.setdefaultencoding("latin-1")


###Define function to parse urls
def parse_apt(url):
    try:
        #The function receives a list with urls
        record={}
        cargen=[]
        counter = 0
        #Generate a unique id for each apt
        #print len(url)
        random.seed(10)
        #record['key']=str(n).zfill(4)    
        for i in url:
            print '-------------------------------'
            print "Parsing url # ", i
            print i 
            html = scraperwiki.scrape(i)
            root = lxml.html.fromstring(html)
            ammenities =[]
            caracteristics = []
            vals_caracteristics =[]
            record['key']=uuid.uuid4().hex #Rehuse the past key
            record['url'] = i
            for el in root.cssselect("p.h2"):
                record['price'] = el.text_content().strip()
                #print el.text_content().strip()
            for el in root.cssselect("div.meta h2"):
                record['cmt'] = el.text_content().strip()
                #print el.text_content().strip()
            for el in root.cssselect("div.meta"):
                record['desc'] = el.text_content().strip()
                #print el.text_content().strip()
            for el in root.cssselect("div.grid_16.alpha.omega.mtl li"):
                ammenities.append(el.text_content().encode(encoding='latin1').strip())
            record['amenities'] = ammenities
                #print el.text_content().strip()
            for el in root.cssselect("div.caracteristicas.grid_10.alpha.pan.mtl dt"):
                caracteristics.append(el.text_content().strip().encode("hex"))        
    
                #print el.text_content().strip()
            for el in root.cssselect("div.caracteristicas.grid_10.alpha.pan.mtl dd"):
                vals_caracteristics.append(el.text_content().strip())
                #print el.text_content().strip()
            for el in root.get_element_by_id("image_wrap"):
                print el.attrib.get('src')
                record['img']= el.attrib.get('src')   
                
            ####Make dictionary for characteristics
            chars = {k: v for k, v in zip(caracteristics, vals_caracteristics)}
            
            ###Join both dictionaries
            final_record = dict(record.items() + chars.items())
            #print final_record.keys()    
            
            #Save data
    
            unique_keys = ['key']
            
            scraperwiki.sqlite.save(unique_keys, final_record)

    except:
        pass
        tb = sys.exc_info()[2]
        print "Line %i" % tb.tb_lineno
        print e.message
        


#####Get urls for apts

def make_url(min,max):
    try:
        path = "http://propiedades.zonaprop.com.mx/renta-departamentos-distrito-federal/ncZ52_opZtipo-operacion-alquiler_lnZ58767_pnZ"
        #random.seed(10)
        #clave = sorted(random.sample(xrange(1,5000), 2000))
        ###Loop and make the next urls
        list_of_urls = []
        for i in range(min,max+1):        
            menu_url = str(path) + str(i)
            print '---------------------- Main page address------------------------'
            print menu_url
            print '--------------------------------------------------------------'
            #Scrape each url for apt urls
            doc = scraperwiki.scrape(menu_url)
            root_menu = lxml.html.fromstring(doc)
            counter = []
            base={}
            #Search for links in main pages
            for z in root_menu.cssselect("div.middle a"):
                #counter.append(z)
                #base['id']= str(i).rjust(3, '0') + str(len(counter)).rjust(3, '0')                        
                base['apt_url'] = z.attrib.get('href')
                if z.attrib.get('href'):
                    if z.attrib.get('href') != '#':
                        print 'Adding to url list: '
                        print z.attrib.get('href')
                        list_of_urls.append(z.attrib.get('href'))
        #print " Parsing a total of " + str(len(list_of_urls)) + " urls"
        print len(list_of_urls)
        parse_apt(list_of_urls)
    
        #for j in range(1,len(list_of_urls)):
            #print "This is url " + str(j) + " out of " +str(len(list_of_urls))
            #print list_of_urls[j]    
        #unique_keys = ['key']
                
        #scraperwiki.sqlite.save(unique_keys, final_record)
    except:
        pass


               

make_url(2,24)