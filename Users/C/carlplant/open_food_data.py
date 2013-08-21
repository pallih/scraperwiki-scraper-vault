import scraperwiki
import urlparse
import lxml.html
import datetime
now = datetime.datetime.now()
import re
from BeautifulSoup import BeautifulSoup

def scrape_main_links(main_link):
    html3 = scraperwiki.scrape(main_link)
    root3 = lxml.html.fromstring(html3)
    names = root3.cssselect("div#mid") 
    for name in names:
        food = name.cssselect("h2")
        if food:
            food_type = food[0].text
            rows2 = root3.cssselect("table tr")  # selects all <tr> blocks within <table>
    
    soup = BeautifulSoup(html3)
    serving = soup.find('option', selected="selected")
    print serving
    if serving:
        portion = serving.text

    foods = root3.cssselect("div#nutrition-box table")
    for row3 in foods:
        food_cells = row3.cssselect(" tr td.calorie-row1")
       
        if food_cells:  
            calories = food_cells[0].text_content()
        food_cells2 = row3.cssselect("td table tr td.col2.right")
        if food_cells2:  
            total_fats = food_cells2[0].text_content()
                    
            scraperwiki.sqlite.save(unique_keys=[], data={'Calories' : calories, 'Food':food_type, 'portion':portion, 'Total fats':total_fats})


def scrape_table(next_url):
    html2 = scraperwiki.scrape(next_url)
            #print html2
    root2 = lxml.html.fromstring(html2)
    rows = root2.cssselect("div.category-box-big ul li")  
    #print rows
    for row2 in rows:
        table_cells = row2.cssselect("a")
        if table_cells:
            #link = table_cells[0].attrib.get('href')
            main_link = urlparse.urljoin(base_url, table_cells[0].attrib.get('href'))
            scrape_main_links(main_link)
            
            #print main_link

def scrape_and_look_for_next_link(base_url):
    html = scraperwiki.scrape(base_url)
    #print html
    root = lxml.html.fromstring(html)
    #scrape_table(root)
    next_link = root.cssselect("div.category-box")
    for row in next_link:
        cells = row.cssselect("a")
        if cells:
            next_url = urlparse.urljoin(base_url, cells[0].attrib.get('href'))
            scrape_table(next_url)
            #print next_url
            
            
        #scrape_and_look_for_next_link(next_url)


base_url = 'http://openfooddata.com'
scrape_and_look_for_next_link(base_url)
