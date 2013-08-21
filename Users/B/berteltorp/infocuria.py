import scraperwiki
# import requests
import lxml.html
import time
# import re

def scrape_affaires():
    side = 1
    for side in range(1,613):
        #Don't make the server mad. 
        time.sleep(3)
        print 'Scraping page # ' + str(side)
        html = scraperwiki.scrape("http://curia.europa.eu/juris/liste.jsf?pro=&lgrec=en&nat=&oqp=&dates=%2524type%253Dpro%2524mode%253D5Y%2524from%253D2007.09.05%2524to%253D2012.09.05&lg=&language=en&jur=C%2CT%2CF&cit=none%252CC%252CCJ%252CR%252C2008E%252C%252C%252C%252C%252C%252C%252C%252C%252C%252Ctrue%252Cfalse%252Cfalse&td=ALL&pcs=O&avg=&page='+str(side)+'&mat=or&jge=&for=&cid=1098497")
        # print html
        side = side + 1        
        root = lxml.html.fromstring(html)
        newroot = root.get_element_by_id('mainForm:aff')
        for li in newroot.cssselect(".affaire"):
            
            data = {
                'affaire_status' : get_element_or_none(li, '.affaire_status'),
                'affaire_title' : get_element_or_none(li, '.affaire_title'),
                'affaire_counter' : get_element_or_none(li, '.affaire_counter'),
                'decision_link' : get_element_or_none(li, '.decision_links a', 'href')                
            }
            # print data
            scraperwiki.sqlite.save(unique_keys=["decision_link"], data=data)

# A handy function to get text or attributes out of HTML elements
def get_element_or_none(context, css, attribute=None):
    try:
        element = context.cssselect(css)[0]
    except:
        return None
    else:
        if attribute:
            return element.get(attribute)
        else:
            return element.text
scrape_affaires()



