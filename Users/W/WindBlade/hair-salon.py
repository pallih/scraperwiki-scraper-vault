###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next'
# links from page to page: use functions, so you can call the same code
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################
import urllib2
import scraperwiki
import base64

from BeautifulSoup import BeautifulSoup

#print  base64.decodestring('eWlsb25nc2FsZXNAc2luZ25ldC5jb20uc2c=')
#abc = "<span>Tel: <script type='text/javascript'>/* <![CDATA[ */document.write(DecodeBase64(\'NjczNTg3MjU=\'));/* ]]> */</script></span>"
#low = abc.find("e64('")
#high = abc.rfind("'))")
#print abc[low+5:high]
#print base64.decodestring(abc[low+5:high])

         
         
         

# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup, url):
    
    name = soup.find("div", {"class": "hd"}).h1.renderContents().strip()
    address = soup.find("p", { "class" : "address"}).renderContents().strip()
    tel = ""
    fax = ""
    hours = ""
    cat = ""
    email = ""
    website = ""
    special = ""
    nearestMRT = ""
    neighbourhood  = ""
    desc = ""
    
    id1 = url.find('id-')
    id = url[id1+3:id1+11]

    phones = soup.find("p", { "class" : "phones"})
    if phones:
        p = phones.find(text="Tel: ")
        if p:
            telRaw  = p.parent.renderContents()
            low = telRaw.find("e64('")
            high = telRaw.rfind("'))")
            tel = base64.decodestring(telRaw[low+5:high])
            
        p = phones.find(text="Fax: ")
        if p:
            telRaw  = p.parent.renderContents()
            low = telRaw.find("e64('")
            high = telRaw.rfind("'))")
            fax= base64.decodestring(telRaw[low+5:high])
        
    
    details = soup.find("div", { "class" : "details"})
   
    d = details.find(text="Opening Hours")
    if d:
        hours = d.parent.findNextSibling("dd").renderContents().strip()
                  
    d = details.find(text="Category")              
    if d:
        cat = d.parent.findNextSibling("dd").text.strip()
                  
                  
    d = details.find(text="Email")
    if d:
        email= d.parent.findNextSibling("dd").renderContents().strip()
        if email.find("e64('"):
            low = email.find("e64('")
            high = email.rfind("'))")
            email= base64.decodestring(email[low+5:high])
            
                  
    d =  details.find(text="Website")
    if d:
        website = d.parent.findNextSibling("dd").a.renderContents().strip()
                  
    d = (details.find(text="Specialties"))              
    if d:
        special = d.parent.findNextSibling("dd").renderContents().strip()
                  
    d = (details.find(text="Neighbourhood"))              
    if d:
        neighbourhood = d.parent.findNextSibling("dd").renderContents().strip()
                  
                  
    d = (details.find(text="Nearest MRT"))
    if d:               
        nearestMRT= d.parent.findNextSibling("dd").renderContents().strip()
    
     
    d = (details.find("dd", { "class" : "description"}))
    if d:
        desc = d.renderContents().strip()
        
    data = {}
    data['Name'] = name
    data['Address'] = address
    data['Tel'] = tel
    data['Fax'] = fax
    data['Operating Hours'] = hours
    data['Category'] = cat
    data['Email'] = email
    data['Website'] = website
    data['Specialties'] = special
    data['inSing ID'] = id
    data['Neighbourhood'] = neighbourhood
    data['Nearest MRT'] = nearestMRT
    data['Description'] = desc
    print data

    scraperwiki.datastore.save(['inSing ID'], data)
    
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again

def scrape_and_look_for_next_link(url):
    html = opener.open(url).read()
# print html
    soup = BeautifulSoup(html)
    scrape_table(soup, url)
    next_link = soup.find("li", { "class" : "next" })
    if next_link:        
        scrape_and_look_for_next_link(next_link.a['href'])

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then
# ---------------------------------------------------------------------------
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8')]
#starting_url = 'http://search.insing.com/business/fresver-beauty/scotts-road-newton/id-f0a00100?title=Beauty+%26+Spa+%3E+Beauty+Salons+%3E+Facials&refinedCategory=Beauty+%26+Spa+%3E+Beauty+Salons+%3E+Facials&taxonomyNode=Beauty+%26+Spa+%3E+Beauty+Salons+%3E+Facials&shuffling_cipher=4&businessPage=6&resultIndex=1'
#starting_url = 'http://search.insing.com/business/yi-long-envelope-manufacturer/geylang-stadium-old-airport/id-efcc0000?title=Arts+%26+Entertainment+%3E+Art+Galleries&refinedCategory=Arts+%26+Entertainment+%3E+Art+Galleries&taxonomyNode=Arts+%26+Entertainment+%3E+Art+Galleries&shuffling_cipher=12&businessPage=1&resultIndex=1'
starting_url = 'http://search.insing.com/business/phyto-hair-spa-by-revamp/orchard-river-valley/id-ba0c0000?title=Beauty+%26+Spa+%3E+Hair+Salons+%26+Barbers&refinedCategory=Beauty+%26+Spa+%3E+Hair+Salons+%26+Barbers&taxonomyNode=Beauty+%26+Spa+%3E+Hair+Salons+%26+Barbers&shuffling_cipher=14&businessPage=1&resultIndex=1'
    
scrape_and_look_for_next_link(starting_url)



