import scraperwiki
import lxml.html

url = 'http://www.nhs.uk/ServiceDirectories/Pages/AcuteTrustListing.aspx'
#typical destination is http://www.nhs.uk/Services/Trusts/Overview/DefaultView.aspx?id=818
#link is relative: a href="/Services/hospitals/Overview/DefaultView.aspx?id=606"
#within <h3> <a>
#need to convert to this:http://www.nhs.uk/Services/Trusts/HospitalsAndClinics/DefaultView.aspx?id=818
baseurl = 'http://www.nhs.uk'

def scrapedetails(hospitalsurl):
    html = scraperwiki.scrape(hospitalsurl)
    print html
    root = lxml.html.fromstring(html)
    headings = root.cssselect('h3')
    for heading in headings:
        print heading.text_content

def scrapelinks(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    links = root.cssselect('ul.trust-list li a')
    print links
    for link in links:
        print link.attrib.get('href')
        if link.attrib.get('href') is not "#":
            print "NOT HASH"
            print link.attrib.get('href').split("?")[1]
            hospitalsurl = "http://www.nhs.uk/Services/Trusts/HospitalsAndClinics/DefaultView.aspx?"+link.attrib.get('href').split("?")[1]
            print hospitalsurl
            scrapedetails(hospitalsurl)


scrapelinks(url)

