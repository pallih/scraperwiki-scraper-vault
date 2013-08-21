#Scrape of NHS Choice to look at numbers of
#people recommending GP practices
#and whether the practice has extended appointment times.
#The service directory url has the ID code which we will use later to scrape performance measures.

import scraperwiki
import urlparse
import lxml.html
url = 'http://www.nhs.uk'

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("div.organisation-wrapper div")  # selects  <divs> blocks within <"div.organisation-wrapper">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("div.organisation-header h2 a")
        if table_cells: 
            record['Dr Name'] = table_cells[0].text
        if table_cells: 
            record['Link'] = table_cells[0].attrib['href']             #print record, '------------'
        table_cells2 = row.cssselect("div.organisation.clear ul.address.clear.notranslate li")
        if table_cells2: 
            record['Address'] = table_cells2[0].text 
        table_cells3 = row.cssselect("div.organisation.clear div.metric.stripe p")
        if table_cells3: 
            record['Score'] = table_cells3[0].text_content()
            print record, '------------'
            scraperwiki.sqlite.save(unique_keys=[], data={'Dr Name' : table_cells[0].text, 'Address': table_cells2[0].text, 'Phone': table_cells2[1].text, 'Rec Score': table_cells3[4].text_content(), 'Ext Apps': table_cells3[5].text_content(), 'Link' : url+table_cells[0].attrib['href']})
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("li.next a")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.nhs.uk/Scorecard/Pages/'
starting_url = urlparse.urljoin(base_url, 'Results.aspx?OrgType=1&Coords=2822%2c4042&TreatmentID=0&PageNumber=1&PageSize=0&TabId=30&SortType=1&LookupType=1&LocationType=1&SearchTerm=B29+6JG&DistanceFrom=-1&SortByMetric=0&TrustCode=&TrustName=&DisambiguatedSearchTerm=&LookupTypeWasSwitched=False&MatchedOrganisationPostcode=&MatchedOrganisationCoords=&ServiceIDs=&ScorecardTypeCode=&NoneEnglishCountry=&HasMultipleNames=False&OriginalLookupType=1&ServiceLaunchFrom=&Filters=&TopLevelFilters=')
scrape_and_look_for_next_link(starting_url)
