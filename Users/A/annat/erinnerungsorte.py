# -- coding: utf-8 --
import scraperwiki
import requests
import lxml.html
from lxml.cssselect import CSSSelector
import time
import re

def scrape_site(root_link, select, j):
        
    text =  root_link.cssselect("div#content_left")[0].text_content()
    
   
    try:
        reg = re.search(r"(?<=point).*?(?=)\)", text).group(0)
    
        coordinates = re.search(r'\((.*)\)', reg).group(1)
    
        lat = coordinates.split(",")[0]   
        lng = coordinates.split(",")[1]   

    except:
        lat = None
        lng = None

    contact =  root_link.cssselect("br")
    contact_list = []

    for item in contact:
        if item.tail != None:
            
            contact_list.append(item.tail)

    intro_text = contact_list[0]

   
    length = len(contact_list)-1
    street = None
    plz = None
    tel = None
    city = None

    try:

        for i in range(length,0,-1):

            if contact_list[i].find('Tel') != -1:
                tel = contact_list[i]
                street = contact_list[i-3]
                plz = contact_list[i-2].split()[0]
                city = contact_list[i-2].split()[1]

    except (RuntimeError, TypeError, NameError):
            tel = None
            street = None
            plz= None
            city = None

    
    name = select("h1.red").text_content()
    
    webpage_list =  root_link.cssselect("a")
    webpage = None
    try:
        for i in range(len(webpage_list)):
            if webpage_list[i].text_content().find('http://') != -1:
    
                webpage = webpage_list[i].text_content()

    except IndexError:
        webpage = None

    try:
        image_url = "http://www.bpb.de" +  select("img.thumbnail-border-article").get('src')
    except IndexError:
        image_url = None
      
    data = {
            'image_url' : image_url,
            'name' : name,
            'lat' : lat,
            'lng' : lng,
            'intro_text' : intro_text,
            'street' : street,
            'plz' : plz,
            'city' : city,
            'tel' : tel,
            'webpage' : webpage
            }

    scraperwiki.sqlite.save(unique_keys=['name'], data=data)

def main():
    
    for i in range(20):

        p = str(i)
        url ="http://www.bpb.de/geschichte/nationalsozialismus/erinnerungsorte/?gstdb_sent=1&gstdb_volltext=&gstdb_gedenkstaettentyp=-1&gstdb_bundesland=-1&gstdb_plz=&gstdb_umkreis=&paginator="+p+"#paginator"
        
        html = requests.get(url, verify = False).text
        root = lxml.html.fromstring(html)

        hit_list =  root.cssselect("div#ajaxtrefferliste a")

        for j in range(3,len(hit_list)):
             
            select = lambda expr: root_link.cssselect(expr)[0]
      
            link ="http://www.bpb.de" + hit_list[j].attrib['href']  
            html_link = requests.get(link, verify = False).text
            root_link = lxml.html.fromstring(html_link)

            if select("h1.red").text_content() != "Datenbank Erinnerungsorte":
                scrape_site(root_link, select, j)

        time.sleep(7)
            
       

main()
# -- coding: utf-8 --
import scraperwiki
import requests
import lxml.html
from lxml.cssselect import CSSSelector
import time
import re

def scrape_site(root_link, select, j):
        
    text =  root_link.cssselect("div#content_left")[0].text_content()
    
   
    try:
        reg = re.search(r"(?<=point).*?(?=)\)", text).group(0)
    
        coordinates = re.search(r'\((.*)\)', reg).group(1)
    
        lat = coordinates.split(",")[0]   
        lng = coordinates.split(",")[1]   

    except:
        lat = None
        lng = None

    contact =  root_link.cssselect("br")
    contact_list = []

    for item in contact:
        if item.tail != None:
            
            contact_list.append(item.tail)

    intro_text = contact_list[0]

   
    length = len(contact_list)-1
    street = None
    plz = None
    tel = None
    city = None

    try:

        for i in range(length,0,-1):

            if contact_list[i].find('Tel') != -1:
                tel = contact_list[i]
                street = contact_list[i-3]
                plz = contact_list[i-2].split()[0]
                city = contact_list[i-2].split()[1]

    except (RuntimeError, TypeError, NameError):
            tel = None
            street = None
            plz= None
            city = None

    
    name = select("h1.red").text_content()
    
    webpage_list =  root_link.cssselect("a")
    webpage = None
    try:
        for i in range(len(webpage_list)):
            if webpage_list[i].text_content().find('http://') != -1:
    
                webpage = webpage_list[i].text_content()

    except IndexError:
        webpage = None

    try:
        image_url = "http://www.bpb.de" +  select("img.thumbnail-border-article").get('src')
    except IndexError:
        image_url = None
      
    data = {
            'image_url' : image_url,
            'name' : name,
            'lat' : lat,
            'lng' : lng,
            'intro_text' : intro_text,
            'street' : street,
            'plz' : plz,
            'city' : city,
            'tel' : tel,
            'webpage' : webpage
            }

    scraperwiki.sqlite.save(unique_keys=['name'], data=data)

def main():
    
    for i in range(20):

        p = str(i)
        url ="http://www.bpb.de/geschichte/nationalsozialismus/erinnerungsorte/?gstdb_sent=1&gstdb_volltext=&gstdb_gedenkstaettentyp=-1&gstdb_bundesland=-1&gstdb_plz=&gstdb_umkreis=&paginator="+p+"#paginator"
        
        html = requests.get(url, verify = False).text
        root = lxml.html.fromstring(html)

        hit_list =  root.cssselect("div#ajaxtrefferliste a")

        for j in range(3,len(hit_list)):
             
            select = lambda expr: root_link.cssselect(expr)[0]
      
            link ="http://www.bpb.de" + hit_list[j].attrib['href']  
            html_link = requests.get(link, verify = False).text
            root_link = lxml.html.fromstring(html_link)

            if select("h1.red").text_content() != "Datenbank Erinnerungsorte":
                scrape_site(root_link, select, j)

        time.sleep(7)
            
       

main()
