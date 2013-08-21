import scraperwiki
import urlparse
import lxml.html

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    country = root.cssselect( "div#content h1" )
    if country:
        record = {}
        record[ "Country" ] = country[ 0 ].text
        infos = root.cssselect("div.sprawk-nofuzzy.qpCountryFloatBox")  # selects all <tr> blocks within <table class="data">
        if infos:
            info = infos[ 0 ]

            # cameral type
            cameralType = info.cssselect( "p b" )
            record[ "Type" ] = cameralType[ 0 ].text
    
            uls = info.cssselect( "ul" )
    
            lis = uls[ 0 ].cssselect( "li" )
            lowerExist = lis[ 0 ].cssselect( "span" )[ 0 ].text_content()
            record[ "Lower" ] = lowerExist
    
            if len( lis ) > 2:
                upperExist = lis[ 1 ].cssselect( "span" )[ 0 ].text_content()
                record[ "Upper" ] = upperExist
    
                subLevel = lis[ 2 ].cssselect( "span" )[ 0 ].text_content()
                record[ "SubNationalLevel" ] = subLevel
            else:
                record[ "Upper" ] = "-"
                subLevel = lis[ 1 ].cssselect( "span" )[ 0 ].text_content()
                record[ "SubNationalLevel" ] = subLevel
                
    
            voluntaryQuatas = uls[ 1 ].cssselect( "li span" )[ 0 ].text_content()
            record[ "VoluntaryQuatas" ] = voluntaryQuatas

            scraperwiki.datastore.save(["Country"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape(url):
    html = scraperwiki.scrape(url)
    if html:
        root = lxml.html.fromstring(html)
        scrape_table( root )

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.quotaproject.org/uid/countryview.cfm'

html = scraperwiki.scrape( base_url )
if html:
    root = lxml.html.fromstring(html)
    countries = root.cssselect( "select.sprawk-sorted option" )
    i = 0
    for country in countries:
        countryValue = country.attrib[ "value" ]
        if countryValue == "-1":
            continue
        scrape( base_url + "?country=" + countryValue )
        i += 1
        print str( i ) + "/" + str( len( countries ) )
