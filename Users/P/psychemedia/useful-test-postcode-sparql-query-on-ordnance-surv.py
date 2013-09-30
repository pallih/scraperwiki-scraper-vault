###############################################################################
# Basic scraper
# YQL SPARQL Query on Ordnance Survey SPARQL Enpoint
###############################################################################

import yql
import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrapeFrom(soup,txt,el,attr=''):
    start=soup.find(text=txt)
    return start.findAllNext(el,attr)
    
def get_Library_postcode(url):
    # retrieve a page
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    tags=scrapeFrom(soup,'Post Code:','td','')
    print 'Extracted postcode:',tags[1].text
    return tags[1].text.replace(' ','')
    
url='http://www.access.sconul.ac.uk/members/institution_html?ins_id=3&contacts=1'
postcode=get_Library_postcode(url)
    
    
os_endpoint='http://api.talis.com/stores/ordnance-survey/services/sparql'

os_query='''
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX postcode: <http://data.ordnancesurvey.co.uk/ontology/postcode/>

select ?district ?wardname ?districtname where {
<http://data.ordnancesurvey.co.uk/id/postcodeunit/MAGIC_POSTCODE> postcode:district ?district; postcode:ward ?ward.
?district skos:prefLabel ?districtname.
?ward skos:prefLabel ?wardname
}
'''

#postcode="MK7 6AA"

    
os_query=os_query.replace('MAGIC_POSTCODE',postcode.replace(' ',''))


def run_sparql_query(query, endpoint):
    y = yql.Public()
    query='select * from sparql.search where query="'+query+'" and service="'+endpoint+'"'
    env = "http://datatables.org/alltables.env"
    return y.execute(query, env=env)

result=run_sparql_query(os_query, os_endpoint)

for row in result.rows:
    print postcode,'is in the',row['result']['wardname']['value'],'ward of',row['result']['districtname']['value']
    record={ "id":postcode, "ward":row['result']['wardname']['value'],"district":row['result']['districtname']['value']}
    scraperwiki.datastore.save(["id"], record) 
###############################################################################
# Basic scraper
# YQL SPARQL Query on Ordnance Survey SPARQL Enpoint
###############################################################################

import yql
import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrapeFrom(soup,txt,el,attr=''):
    start=soup.find(text=txt)
    return start.findAllNext(el,attr)
    
def get_Library_postcode(url):
    # retrieve a page
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    tags=scrapeFrom(soup,'Post Code:','td','')
    print 'Extracted postcode:',tags[1].text
    return tags[1].text.replace(' ','')
    
url='http://www.access.sconul.ac.uk/members/institution_html?ins_id=3&contacts=1'
postcode=get_Library_postcode(url)
    
    
os_endpoint='http://api.talis.com/stores/ordnance-survey/services/sparql'

os_query='''
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX postcode: <http://data.ordnancesurvey.co.uk/ontology/postcode/>

select ?district ?wardname ?districtname where {
<http://data.ordnancesurvey.co.uk/id/postcodeunit/MAGIC_POSTCODE> postcode:district ?district; postcode:ward ?ward.
?district skos:prefLabel ?districtname.
?ward skos:prefLabel ?wardname
}
'''

#postcode="MK7 6AA"

    
os_query=os_query.replace('MAGIC_POSTCODE',postcode.replace(' ',''))


def run_sparql_query(query, endpoint):
    y = yql.Public()
    query='select * from sparql.search where query="'+query+'" and service="'+endpoint+'"'
    env = "http://datatables.org/alltables.env"
    return y.execute(query, env=env)

result=run_sparql_query(os_query, os_endpoint)

for row in result.rows:
    print postcode,'is in the',row['result']['wardname']['value'],'ward of',row['result']['districtname']['value']
    record={ "id":postcode, "ward":row['result']['wardname']['value'],"district":row['result']['districtname']['value']}
    scraperwiki.datastore.save(["id"], record) 
