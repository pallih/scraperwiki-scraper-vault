# Imports
import scraperwiki
import lxml.html
from datetime import datetime, date, time

# Get the target site
targetSite = "http://epetitions.direct.gov.uk/petitions/"
ePetitionId = "33116" # "Withdraw Addison Lee's license"
targetSite = targetSite + ePetitionId

def main():
    dt = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print dt
    print ePetitionId
    html = scraperwiki.scrape(targetSite)
    root = lxml.html.fromstring(html)
    title = root.cssselect("div.content h1")[0].text
    print title
    count = root.cssselect("dd.signature_count")[0].text
    print count
    saveScrapeData(dt, ePetitionId, title, count)

def saveScrapeData(dt, ePetitionId, title, count):
    # Build the data array
    data = {
        'scrape_time' : dt, # Create a key
        'petition_id' : ePetitionId,
        'petition_title' : title,
        'sign_count' : count
    }

    # Insert the date into the database
    scraperwiki.sqlite.save(unique_keys=['scrape_time'], data=data)

main()# Imports
import scraperwiki
import lxml.html
from datetime import datetime, date, time

# Get the target site
targetSite = "http://epetitions.direct.gov.uk/petitions/"
ePetitionId = "33116" # "Withdraw Addison Lee's license"
targetSite = targetSite + ePetitionId

def main():
    dt = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print dt
    print ePetitionId
    html = scraperwiki.scrape(targetSite)
    root = lxml.html.fromstring(html)
    title = root.cssselect("div.content h1")[0].text
    print title
    count = root.cssselect("dd.signature_count")[0].text
    print count
    saveScrapeData(dt, ePetitionId, title, count)

def saveScrapeData(dt, ePetitionId, title, count):
    # Build the data array
    data = {
        'scrape_time' : dt, # Create a key
        'petition_id' : ePetitionId,
        'petition_title' : title,
        'sign_count' : count
    }

    # Insert the date into the database
    scraperwiki.sqlite.save(unique_keys=['scrape_time'], data=data)

main()