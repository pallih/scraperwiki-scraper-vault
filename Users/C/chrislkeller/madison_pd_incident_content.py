import scraperwiki           
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2

def extract(soup, incident):

    incident_prefix = 'http://www.cityofmadison.com/incidentReports/'

    crimes = soup.find('table', {'id': 'list'})
    rows = crimes.findAll('tr')[1:]
    for row in rows:
        col = row.findAll('td')
        date = col[0].text
        incident = col[1].text
        incident_link = col[1].a['href']
        case_number = col[2].text
        address = col[3].text

        # generate URL to incident report
        incident_content = incident_prefix + incident_link

        # check the incident report URL
        

        # open the incident report URL
        # and return the contents
        mech = Browser()
        urlContent = incident_content
        pageContent = mech.open(urlContent)
        htmlContent = pageContent.read()
        soupContent = BeautifulSoup(htmlContent)


        # hits incident detail table and returns the contents
        table = soupContent.find('table', {'id': 'incidentdetail'})

        # finds the tbody that contains the data
        body = table.find('tbody')

        # find all of the rows
        rows = body.findAll('tr')

        # determine the number of rows
        numberOfRows = len(rows)

        for row in rows:
            label = row.find('th').text
            narrative = row.find('td').text

            print label
            print narrative


mech = Browser()
url = 'http://www.cityofmadison.com/incidentReports/incidentList.cfm?a=71&page=1'
page = mech.open(url)
html = page.read()
soup = BeautifulSoup(html)
extract (soup, 1)
