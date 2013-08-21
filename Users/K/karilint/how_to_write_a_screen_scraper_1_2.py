###############################################################################
# Mammalian Species from American Society of Mammalogists web page
# http://www.science.smith.edu/msi/msiaccounts.html
###############################################################################

# -----------------------------------------------------------------------------
# Scraped by: Kari Lintulaakso
# Date:17.09.2012
# 
# This is a test scraper I made from the mammals listed on the American Society of Mammalogists web page
# 
# -----------------------------------------------------------------------------


import scraperwiki
import lxml.html
url = "http://www.science.smith.edu/msi/msiaccounts.html"
base_url = "http://www.science.smith.edu/msi/"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

lis = root.cssselect('li') # get all the <li> tags
for li in lis:
    species_url = ''
    binomal = ''
    vernacular = ''
#    print lxml.html.tostring(li) # the full HTML tag
    links = li.cssselect('a')  # selects all <a> links in <div class="Result">
    if links:
        vernacular = links[0].text.encode('utf-8').replace("(","").strip()    
        species_url = links[0].attrib['href']
#        print links[0].text.encode('utf-8').replace("(","").strip()
#        print links[0].attrib['href']
    else:
#        print li[0].text.encode('utf-8').replace("(","")    
        vernacular = li.text.encode('utf-8').replace("(","").strip()
        species_url = 'No link'
#        print li.text.encode('utf-8').replace("(","").strip()
#        print 'No link'
    
#    print str(li.text).encode('utf-8').replace("(","")
#    print li.text                # just the text inside the HTML tag
#    print li.tail                #Any trailing text from just after the close tag.
    i = li.cssselect('i')
    if i:
        binomal = i[0].text
#        print i[0].text    
    else:
        em = li.cssselect('em')
        if em:
            binomal = em[0].text
#            print em[0].text    
        else:
            binomal = 'No latin name'
#            print'No latin name'        

    # Set up our data record - we'll need it later
    record = {}
    record['Binomal'] = binomal.strip()
    record['Vernacular'] = vernacular.strip()
    if species_url.strip() == 'No link':
        record['URL'] = species_url.strip()
    else:
        record['URL'] = base_url.strip() + species_url.strip()

    # Print out the data we've gathered
    print record, '------------'
    # Finally, save the record to the datastore - 'Binomal' is our unique key
    scraperwiki.sqlite.save(['Binomal'], record)

