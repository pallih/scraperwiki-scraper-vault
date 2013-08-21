# Scraper to retrieve drilling licence permits from the NPD website.
# Note: The website has multiple pages, this only gets the first page of the search results.

# Imports
import scraperwiki
import lxml.html

# Get the target site
targetSite = "http://www.npd.no/en/news/Drilling-permits/"

print "NPD Scraper"

# Scrape it
html = scraperwiki.scrape(targetSite)
root = lxml.html.fromstring(html)

# Loop through the sections that contain the data (divs of "row" class)
for div in root.cssselect("div.row"):
    # Split into an array
    content = div.text_content().split("\n")
    # Strip whitespace from the lines, ignore any lines that are blank 
    content = [ln.strip() for ln in content if ln.strip() != ""]
    # Find the start point of the well name
    wellidx = content[0].find('for well ') + 9
    # Extract the well name
    well = content[0][wellidx:content[0].find(' in production licence')]
    # Extract the licence name
    licence = content[0][content[0].find('licence ') + 8:]
    # Reformat the date to universal/sqllite date format
    date = content[1]
    date = date.split('.')
    date = date[2] + '-' + date[1] + '-' + date[0]
    
    # Build the data array
    data = {
        'key' : content[1] + '#' + well, # Create a key
        'title' : content[0],
        'date' : date,
        'well' : well,
        'licence' : licence
    }

    # Insert the date into the database
    scraperwiki.sqlite.save(unique_keys=['key'], data=data)