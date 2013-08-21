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
    print url

    scraperwiki.datastore.save(['inSing ID'], data)
    
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again

def scrape_and_look_for_next_link(url):
    while (url) : 
        html = opener.open(url).read()
        soup = BeautifulSoup(html)
        scrape_table(soup, url)
        url= soup.find("li", { "class" : "next" })
        if (url) :
            url = url.a['href']
   

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then
# ---------------------------------------------------------------------------
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8')]
starting_url = 'http://search.insing.com/business/yacht-21/bugis/id-0e400200?businessName=bYSI&refinedCategory=Shopping+%26+Retail+%3E+Fashion+%26+Apparel+%3E+Ladies+Apparel+%26+Accessories&businessPage=137&resultIndex=6&shuffling_cipher=6&ogType=company&address=50+Orchard+Road+%2302-15%2F16+Wheelock+Place++&TRUNCATE_REVIEWS=true'
    
scrape_and_look_for_next_link(starting_url)


 
