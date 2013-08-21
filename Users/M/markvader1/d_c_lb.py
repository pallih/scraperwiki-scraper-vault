import scraperwiki
import lxml.html
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):

    scraperwiki.sqlite.save('data_columns', ['Crag Name','Map Reference','Crag Code','link',])
    
    table = soup.find("table", {"class": "bodytext"})
    
    rows = table.findAll("tr")
    for row in rows:
        record = {}

        table_td = row.findAll("td")
    
        if len(table_td) == 4:
            record['Crag Name'] = table_td[0].text
#            record['Map Reference'] = table_td[1].text
            record['Author'] = table_td[2].text
#            record['link'] = table_td[3].string #HOW DO I STRIP HREF LINK FROM WITHIN THIS TD VALUE
            record['link'] = table_td[3].tag["href"] #HOW DO I STRIP HREF LINK FROM WITHIN THIS TD VALUE


#    rows=table.findAll("a")
#    for row in rows:
#        record = {}
#
#        table_td = row.findAll("a")
#    
#        if len(table_td) == 4:
#            record['link'] = table_td[3].get('href') #HOW DO I STRIP HREF LINK FROM WITHIN THIS TD VALUE


#        table_td = row.findAll("a")
#           print row['href']

# Various attempts I have tried to export the href link
#            record['link'] = table_td[3].attrib['href']
#            record['link'] = table_td[3][0].attrib['href']
#            record['link'] = table_td[3][1].attrib['href']

#            link = 'http://www.pete-smith.co.uk/dynamic/guidebook/' + table_td[3]
#            record['link'] = link

#            record['link'] = table_td[3].href.text


#            print record,
#            print "-" * 10
          
            scraperwiki.sqlite.save(["Crag Name"], record)

#Define the website
website = "http://www.pete-smith.co.uk/dynamic/guidebook/add_a_crag.php"
#Put the all code in html variable
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)

#TO DO
#
#Correct link extraced from table
#Combine href in table with http://www.pete-smith.co.uk/dynamic/guidebook/ to create full link 
#Strip various data from additional linked lines
#
# Any help appreciated
#
#