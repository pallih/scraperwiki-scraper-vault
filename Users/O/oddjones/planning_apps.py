import string
import scraperwiki
import mechanize
import re

from BeautifulSoup import BeautifulSoup


def CleanCrapFromLink(clen):
    clen = re.sub("&#xD;|&#xA;|&#x9;|\t", "", clen)
    clen = re.sub(" ", "%20", clen)
    clen = re.sub("&amp;", "&", clen)
    return clen

def scrape_table(soup):
    #find table class="reports"
    data_table = soup.find("table", { "summary" : "Results of the Online Registers Search" })
    br2=mechanize.Browser()
    if data_table:
        #find each table row <tr>
        rows = data_table.findAll("tr")
        #for each row, loop through this
        for row in rows:
            #create a record to hold the data
            record = {}
            #find each cell <td>
            table_cells = row.findAll("td")
            #if there is a cell, record the contents in our dataset, the first cell [0] in 'Name' and so on
            if table_cells: 
                record['id'] = table_cells[0].a.string
                record['address'] = table_cells[1].string
                record['proposal'] = table_cells[2].string
                record['date_recd'] = table_cells[3].string
                record['date_decisn'] = table_cells[4].string
                record['decision'] = table_cells[5].string
                # Print out the data we've gathered
                detail = table_cells[0].a.get('href')
                detail = (detail.split())
                record['detail-link'] = detail[3]
                detail="http://northgate.liverpool.gov.uk/PlanningExplorer17/Generic/StdDetails.aspx?PT=Planning%20Applications%20On-Line&TYPE=PL/PlanningPK.xml&PARAM0="+detail[3]+"/PlanningExplorer17/SiteFiles/Skins/Liverpool_WIP/xslt/PL/PLDetails.xslt&FT=Planning%20Application%20Details&DAURI=PLANNING&XMLSIDE=/PlanningExplorer17/SiteFiles/Skins/Liverpool_WIP/Menus/PL.xml"
                br2.open(detail)
                detailSoup = BeautifulSoup(br2.response().read()) 
                hascoords = detailSoup.find(text=re.compile('^Eas'))
                if hascoords:
                    coords = hascoords.split()
                    #go get lat/lng for easting/northing
                    br2.open('http://www.uk-postcodes.com/eastingnorthing.php?easting='+coords[1]+'&northing='+coords[3])
                    latlng = BeautifulSoup(br2.response().read())
                    ll=latlng.find(text=re.compile('^{'))
                    ll = ll.split('"')
                    record['latitude'] =  ll[3]
                    record['longitude']= ll[7]

                # Save the record to the datastore - 'id' is our unique key - 
                scraperwiki.sqlite.save(['id'], record)



#set the URL containing the form we need to open with mechanize
starting_url = 'http://northgate.liverpool.gov.uk/PlanningExplorer17/RecentDecisionsSearch.aspx' #Get decisions from last 7 days
#start using mechanize to simulate a browser ('br')
br = mechanize.Browser()
br.set_debug_responses(True)
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#open the URL previously defined as 'starting_url'
br.open(starting_url)
br.select_form(name="M3Form")
br["vrDays"]=["7"]
#submit the form and put the contents into 'response'
response = br.submit(name="csbtnSearch")
soup = BeautifulSoup(response.read())
#need to do a loop through the "Next" buttons here
page = 1
scrape_table(soup)
while soup.find("a", { "title" : "Goto Page "+ str(page+1) }):
    if page>1:
        for link in br.links(text_regex="next"):
            l2f=str(link.absolute_url)
            l2f=l2f.replace("%09", "")
            l2f=l2f.replace("%0A", "")
            l2f=l2f.replace("%0D", "")
        response = br.open(l2f)
        #create soup object by reading the contents of response and passing it through BeautifulSoup
        soup = BeautifulSoup(br.response().read())
        scrape_table(soup)
    page = page +1

