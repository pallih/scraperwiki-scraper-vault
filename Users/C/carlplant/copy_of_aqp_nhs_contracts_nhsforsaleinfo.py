import scraperwiki
import urlparse
import lxml.html
import re
from BeautifulSoup import BeautifulSoup

try:
    scraperwiki.sqlite.execute("""
        create table aqpnhs
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)
except:
    print "Table probably already exists."


record = {}

def scrape_sme(root2):
    
    rows2 = root2.cssselect("table.ms-formtable tr td")[1]         #some pages have different categories depending on if it includes "suitable  
    record['ref_number'] = rows2.text_content()                        # for SME" is shown
    rows3 = root2.cssselect("table.ms-formtable tr td")[3]
    record['title'] = rows3.text_content()
    rows4 = root2.cssselect("table.ms-formtable tr td")[5]
    record['leadCommiss'] = rows4.text_content()
    rows5 = root2.cssselect("table.ms-formtable tr td")[25]
    record['StartDate'] = rows5.text_content()
#rows7 = root2.cssselect("table.ms-formtable tr td")[9]
#record['detail4'] = rows7.text_content() 
    scraperwiki.sqlite.save(unique_keys=[],data=record, table_name='aqpnhs')
def scrape_cost(root2):
    rows2a = root2.cssselect("table.ms-formtable tr td")[3]         #some pages have different categories depending on if it includes "likely 
    record['ref_number'] = rows2a.text_content()                        #contract value is shown
    rows3a = root2.cssselect("table.ms-formtable tr td")[1]
    record['title'] = rows3a.text_content()
    rows4a = root2.cssselect("table.ms-formtable tr td")[23]
    record['ConValMin'] = rows4a.text_content()
    rows5a = root2.cssselect("table.ms-formtable tr td")[5]
    record['leadCommiss'] = rows5a.text_content()
    rows6a = root2.cssselect("table.ms-formtable tr td")[25]
    record['ConValMax'] = rows6a.text_content() 
    rows7a = root2.cssselect("table.ms-formtable tr td")[27]
    record['StartDate'] = rows7a.text_content() 
    scraperwiki.sqlite.save(unique_keys=[],data=record, table_name='aqpnhs')


#this def scrapes the inidividual pages
def scrape_links(Links):
    
    page = scraperwiki.scrape(Links)
    root2 = lxml.html.fromstring(page)
    soup2 = BeautifulSoup(page)
    #print soup2  
    refNumber = re.search('name="SPBookmark_SuitableForSME"',page)
    tariff = re.search('name="SPBookmark_AWPTariff"',page)
    #print refNumber
    if refNumber:
        scrape_sme(root2)
        print "sme"
    elif tariff:
        scrape_sme(root2)
        print "tariff"
    else:
        scrape_cost(root2)
        print "contract val"
    
    

# scrape_table function: gets passed the search result pages to scrape to get the individual page urls
def scrape_table(root):
    rows = root.cssselect("div.srch-results p")  # selects all <div> blocks within <table class="srch-results">
    for row in rows:
        
        table_cells = row.cssselect("p.ms-navheader a")
        if table_cells: 
            Links = table_cells[0].attrib['href']
            
            scrape_links(Links)
            
            #print Links
            


     
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again

def scrape_and_look_for_next_link(url):      
    html = scraperwiki.scrape(url)
    #print html
    root = lxml.html.fromstring(html)
    soup = BeautifulSoup(html)                        #using BeautifulSoup to find next page links
    scrape_table(root)                                     #before carrying on scrape the hrefs using the scrape_table function
    #print soup
    
    items = soup.findAll('a',title="Next page")           # findAll "next page" links        
    if items:                                             # if there is a next page link continue
        
        next_link = root.cssselect("div.srch-Page.srch-Page-bg a")
    #print next_link
        if next_link:
            next_link2 = next_link[2].attrib['href']
            #print next_link2
            split_link = re.split("\)+",next_link2)
            split_link2 = re.split("\=+",split_link[0])
            split_link3 = re.split("\'+",split_link2[2])
            #print split_link3[0]
        #print split_link2
        #if split_link ==11:
            next_url = nextlink_url+split_link3[0]
            if next_url:
                print next_url
                scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
nextlink_url = 'https://www.supply2health.nhs.uk/results.aspx?k=Status"live"&start1=41'
base_url = 'https://www.supply2health.nhs.uk/Results.aspx?k=Status%3A%22Live%22'
starting_url = urlparse.urljoin(base_url, 'results.aspx?k=Status"live"')
scrape_and_look_for_next_link(base_url)
