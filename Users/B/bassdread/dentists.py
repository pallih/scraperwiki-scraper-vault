import scraperwiki
import lxml.html

def fetch_html(url):
    try:
        html = scraperwiki.scrape(url)
        return lxml.html.fromstring(html)
    except:
        try:
            html = scraperwiki.scrape(url)
            return lxml.html.fromstring(html)
        except:
            pass
        print "Failed to fetch url: " + url
    return 
    

print "Starting!"

try:
    scraperwiki.sqlite.execute("drop table dentists")
except:
    pass

scraperwiki.sqlite.execute("create table dentists (title string, link string, address string, phonenumber string, lng int, lat int, postcode string)")

def extract(result):
    res = {}
    title = link = address = phonenumber = lng = lat = postcode = ''
    res['title'] = result.find_class('notranslate')[0].xpath('a')[0].text.strip()
    res['link'] = "http://www.nhs.uk" + result.find_class('notranslate')[0].xpath('a')[0].attrib['href']
    res['address'] = result.xpath('div/ul/li')[0].text
    res['phonenumber'] = result.xpath('div/ul/li')[1].text
    res['postcode'] = scraperwiki.geo.extract_gb_postcode(res['address'])
    
    loc = scraperwiki.geo.gb_postcode_to_latlng(res['postcode'])
    if loc:
        res['lng'], res['lat'] = loc[0], loc[1]
    else:
        res['lng'], res['lat'] = "",""

    return res

for page_num in range(1, 788):

    url = "http://www.nhs.uk/Scorecard/Pages/Results.aspx?OrgType=2&Coords=3702%2c5028&TreatmentID=0&PageSize=0&TabId=30&SortType=1&LookupType=1&LocationType=1&SearchTerm=hu17+7hu&DistanceFrom=-1&SortByMetric=0&TrustCode=&TrustName=&DisambiguatedSearchTerm=&LookupTypeWasSwitched=False&MatchedOrganisationPostcode=&MatchedOrganisationCoords=&ServiceIDs=&ScorecardTypeCode=&NoneEnglishCountry=&HasMultipleNames=False&OriginalLookupType=1&ServiceLaunchFrom=&Filters=&TopLevelFilters=&PageCount=788&PageNumber="+ str(page_num)
    #url  = "http://www.nhs.uk/Scorecard/Pages/Results.aspx?OrgType=2&Coords=3702%2c5028&TreatmentID=0&PageSize=0&TabId=30&SortType=1&LookupType=1&LocationType=1&SearchTerm=hu17+7hb&DistanceFrom=-1&SortByMetric=0&TrustCode=&TrustName=&DisambiguatedSearchTerm=&LookupTypeWasSwitched=False&MatchedOrganisationPostcode=&MatchedOrganisationCoords=&ServiceIDs=&ScorecardTypeCode=&NoneEnglishCountry=&HasMultipleNames=False&OriginalLookupType=1&ServiceLaunchFrom=&Filters=&TopLevelFilters=&PageCount=788&PageNumber=421"
    
    root = fetch_html(url)
    if root:
        try:
            for result in root.find_class('organisation-wrapper'):
                details = extract(result)
                scraperwiki.sqlite.execute('insert into dentists values (?, ?, ?, ?, ?, ?, ?)', (
                                details['title'], 
                                details['link'], 
                                details['address'], 
                                details['phonenumber'], 
                                details['lng'], 
                                details['lat'], 
                                details['postcode']))

                scraperwiki.sqlite.commit()
        except:
            print "Failed on: %s - %s --> " % (url, details['title'])
    
import scraperwiki
import lxml.html

def fetch_html(url):
    try:
        html = scraperwiki.scrape(url)
        return lxml.html.fromstring(html)
    except:
        try:
            html = scraperwiki.scrape(url)
            return lxml.html.fromstring(html)
        except:
            pass
        print "Failed to fetch url: " + url
    return 
    

print "Starting!"

try:
    scraperwiki.sqlite.execute("drop table dentists")
except:
    pass

scraperwiki.sqlite.execute("create table dentists (title string, link string, address string, phonenumber string, lng int, lat int, postcode string)")

def extract(result):
    res = {}
    title = link = address = phonenumber = lng = lat = postcode = ''
    res['title'] = result.find_class('notranslate')[0].xpath('a')[0].text.strip()
    res['link'] = "http://www.nhs.uk" + result.find_class('notranslate')[0].xpath('a')[0].attrib['href']
    res['address'] = result.xpath('div/ul/li')[0].text
    res['phonenumber'] = result.xpath('div/ul/li')[1].text
    res['postcode'] = scraperwiki.geo.extract_gb_postcode(res['address'])
    
    loc = scraperwiki.geo.gb_postcode_to_latlng(res['postcode'])
    if loc:
        res['lng'], res['lat'] = loc[0], loc[1]
    else:
        res['lng'], res['lat'] = "",""

    return res

for page_num in range(1, 788):

    url = "http://www.nhs.uk/Scorecard/Pages/Results.aspx?OrgType=2&Coords=3702%2c5028&TreatmentID=0&PageSize=0&TabId=30&SortType=1&LookupType=1&LocationType=1&SearchTerm=hu17+7hu&DistanceFrom=-1&SortByMetric=0&TrustCode=&TrustName=&DisambiguatedSearchTerm=&LookupTypeWasSwitched=False&MatchedOrganisationPostcode=&MatchedOrganisationCoords=&ServiceIDs=&ScorecardTypeCode=&NoneEnglishCountry=&HasMultipleNames=False&OriginalLookupType=1&ServiceLaunchFrom=&Filters=&TopLevelFilters=&PageCount=788&PageNumber="+ str(page_num)
    #url  = "http://www.nhs.uk/Scorecard/Pages/Results.aspx?OrgType=2&Coords=3702%2c5028&TreatmentID=0&PageSize=0&TabId=30&SortType=1&LookupType=1&LocationType=1&SearchTerm=hu17+7hb&DistanceFrom=-1&SortByMetric=0&TrustCode=&TrustName=&DisambiguatedSearchTerm=&LookupTypeWasSwitched=False&MatchedOrganisationPostcode=&MatchedOrganisationCoords=&ServiceIDs=&ScorecardTypeCode=&NoneEnglishCountry=&HasMultipleNames=False&OriginalLookupType=1&ServiceLaunchFrom=&Filters=&TopLevelFilters=&PageCount=788&PageNumber=421"
    
    root = fetch_html(url)
    if root:
        try:
            for result in root.find_class('organisation-wrapper'):
                details = extract(result)
                scraperwiki.sqlite.execute('insert into dentists values (?, ?, ?, ?, ?, ?, ?)', (
                                details['title'], 
                                details['link'], 
                                details['address'], 
                                details['phonenumber'], 
                                details['lng'], 
                                details['lat'], 
                                details['postcode']))

                scraperwiki.sqlite.commit()
        except:
            print "Failed on: %s - %s --> " % (url, details['title'])
    
