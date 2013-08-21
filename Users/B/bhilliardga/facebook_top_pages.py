# Blank Python

import mechanize 
import scraperwiki
from BeautifulSoup import BeautifulSoup


#define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Page Name', 'Fans'])

#scrape the fan section
def scrape_fans(soup):
    profiles = soup.find("profileFriendsText",{ "class" : "uiGrid"})  #find the section where the friends are
    links= profiles.findAll("a") #find all the links to friends    
    for cell in cells: #loop through the cells
        #setup the data record
        record={} 
        table_cells=cell.findAll("p") #find all the p items
        if table_cells: #if the item exists store it
            record['Page Name'] = table_cells[0].text
            record['Fans'] = table_cells[1].text[:-5]
            scraperwiki.datastore.save(["Page Name"], record)


def scrape_page(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    #print soup.prettify()
    #link_table=soup.find("div", {"class" : "alphabet_list clearfix"})
    profiles = soup.findall("div", { "class" : "profileFriendsText" })  #find the section where the friends are
    #next_link=soup.findAll("a")
    for profile in profiles:
        next_url=link['href']
        print next_url
        #html1 = scraperwiki.scrape(next_url)
        #soup1 = BeautifulSoup(html1)
        #scrape_fans(soup1)   

def sign_in(url):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    response = br.open(url)
    br._factory.is_html = True
    #print "All forms:", [ form.name  for form in br.forms() ]

    br.select_form(id="login_form")
    print br.form
    

#setup the base url
base_url = 'http://www.facebook.com'
#setup the startup url 



#call the scraping function
sign_in(base_url)
#scrape_page(base_url)
