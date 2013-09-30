###############################################################################
# Obtain egms meta data for local authority websites
# Very early stages!
# Next is to restrict to just egms.subject.service 
# then run for all LA websites for a service page that will be used by them all - if one exists
###############################################################################

import scraperwiki
lgsl = "58"    # 58 = Council Tax
lgil = "08"    # 08 = Information
agency = "35"  # 35 = Brent
url = "http://local.direct.gov.uk/LDGRedirect/index.jsp?LGSL="+lgsl+"&LGIL="+lgil+"&AgencyId="+agency+"&Type=Single"
print url
html = scraperwiki.scrape(url)


# -----------------------------------------------------------------------------
# Get the meta lines
# -----------------------------------------------------------------------------

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html) # turn HTML into a BeautifulSoup object
tds = soup.findAll('meta') # get all the <meta> tags - 
print tds


#for td in tds:

    #print td # the full HTML tag
    #print td.text # just the text inside the HTML tag

# -----------------------------------------------------------------------------
# Save the data in the ScraperWiki datastore.
# -----------------------------------------------------------------------------

for td in tds:
     record = { "td" : td.text } # column name and value
     scraperwiki.datastore.save(["td"], record) # save the records one by one
    
# -----------------------------------------------------------------------------

###############################################################################
# Obtain egms meta data for local authority websites
# Very early stages!
# Next is to restrict to just egms.subject.service 
# then run for all LA websites for a service page that will be used by them all - if one exists
###############################################################################

import scraperwiki
lgsl = "58"    # 58 = Council Tax
lgil = "08"    # 08 = Information
agency = "35"  # 35 = Brent
url = "http://local.direct.gov.uk/LDGRedirect/index.jsp?LGSL="+lgsl+"&LGIL="+lgil+"&AgencyId="+agency+"&Type=Single"
print url
html = scraperwiki.scrape(url)


# -----------------------------------------------------------------------------
# Get the meta lines
# -----------------------------------------------------------------------------

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html) # turn HTML into a BeautifulSoup object
tds = soup.findAll('meta') # get all the <meta> tags - 
print tds


#for td in tds:

    #print td # the full HTML tag
    #print td.text # just the text inside the HTML tag

# -----------------------------------------------------------------------------
# Save the data in the ScraperWiki datastore.
# -----------------------------------------------------------------------------

for td in tds:
     record = { "td" : td.text } # column name and value
     scraperwiki.datastore.save(["td"], record) # save the records one by one
    
# -----------------------------------------------------------------------------

