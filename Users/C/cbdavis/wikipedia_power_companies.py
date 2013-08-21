import csv
from lxml import etree
import re
import scraperwiki
from StringIO import StringIO
from urllib import urlencode

#code inspired by https://scraperwiki.com/scrapers/dbpedia-us-hospitals/edit/
#code build using yql library doesn't seem to work, get a SSLHandshakeError when using code based on https://scraperwiki.com/scrapers/ouseful-two-step-linked-data-test/edit/

#this gets the url that is used to run the sparql query and return results in csv
def csv_url(sparql):
    params = {
        'default-graph-uri': 'http://dbpedia.org',
        'query': sparql,
        'format': 'text/csv',
    }

    return 'http://live.dbpedia.org/sparql?%s' % urlencode(params)
    #it seems that category traversals are not possible using the main dbpedia endpoint, but are possible using the live endpoint
    #return 'http://dbpedia.org/sparql?%s' % urlencode(params)

#run the sparql query and get the results in csv
def parse_csv(url):
    print('creating data object')
    data = StringIO()
    print('about to run query')
    data.write(scraperwiki.scrape(url))
    print('just got the data')
    data.seek(0)

    data_csv = csv.DictReader(data)

    print('about to iterate over the data')
    for row in data_csv:
        rowResult = dict()
        #show what's in here
        for key in row.keys():
            if(row[key]): #only add if string is not empty
                rowResult[key] = row[key]

        print(rowResult)            

        scraperwiki.sqlite.save(unique_keys=['company'], data=rowResult)
    
queryString = """PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
                PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dc:<http://purl.org/dc/terms/>
                PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
                PREFIX dbpprop:<http://dbpedia.org/property/>
                SELECT ?company ?parent 
                        (sql:group_digest(replace(replace(str(?category),"http://dbpedia.org/resource/Category:",""),'_',' '),", ",255,1) 
                            as ?categories)
                WHERE {
                  { SELECT ?category ?y WHERE {
                    ?category skos:broader ?y .
                    ?category rdfs:label ?categoryName .
                    FILTER (regex(?categoryName, "Power companies of", "i")) .
                  } }
                  OPTION ( TRANSITIVE, T_DISTINCT, t_in(?category), t_out(?y), t_step('path_id') as ?path, t_step(?category) as ?route, t_step('step_no') AS ?jump, T_DIRECTION 2 )
                  FILTER ( ?y = <http://dbpedia.org/resource/Category:Power_companies_by_country> ) .
                  ?company dc:subject ?category .
                  OPTIONAL{?company dbpprop:parent ?parent} .
                }"""

parse_csv(csv_url(queryString))
