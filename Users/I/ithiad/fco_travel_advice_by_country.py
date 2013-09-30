import scraperwiki
import lxml.html
import string

letters = string.uppercase

# Now run through all the letters
for letter in letters:
    # Get the listing page for the current letter
    html = lxml.html.parse('http://www.fco.gov.uk/en/travel-and-living-abroad/travel-advice-by-country/?l=' + letter).getroot()
    
    # a.EmbassyLink is the secret CSS incantation for links with the class EmbassyLink
    # This results in a list of a tags
    embassies = html.cssselect('a.EmbassyLink')

    # For each a tag, pull out the link text and link url and stick them in the ScraperWiki datastore
    for embassy in embassies:
        record = {
            "country" : embassy.text,
            "travel-advice" : 'http://www.fco.gov.uk' + embassy.get('href')
        }
        scraperwiki.sqlite.save(["country"], record, verbose=0)


import scraperwiki
import lxml.html
import string

letters = string.uppercase

# Now run through all the letters
for letter in letters:
    # Get the listing page for the current letter
    html = lxml.html.parse('http://www.fco.gov.uk/en/travel-and-living-abroad/travel-advice-by-country/?l=' + letter).getroot()
    
    # a.EmbassyLink is the secret CSS incantation for links with the class EmbassyLink
    # This results in a list of a tags
    embassies = html.cssselect('a.EmbassyLink')

    # For each a tag, pull out the link text and link url and stick them in the ScraperWiki datastore
    for embassy in embassies:
        record = {
            "country" : embassy.text,
            "travel-advice" : 'http://www.fco.gov.uk' + embassy.get('href')
        }
        scraperwiki.sqlite.save(["country"], record, verbose=0)


