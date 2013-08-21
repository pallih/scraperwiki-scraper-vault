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

        #calculate the latitude and longitude, these appear in several forms

        rowResult["latitude"] = ""
        rowResult["longitude"] = ""
                
        #values for geoLat and geoLong are preferred
        if ("geoLat" in rowResult) and ("geoLong" in rowResult) :
            rowResult["latitude"] = float(rowResult["geoLat"])
            rowResult["longitude"] = float(rowResult["geoLong"])
        elif ("latDMS" in rowResult) and ("longDMS" in rowResult) :
            #otherwise use values for latDMS and longDMS
            rowResult["latitude"] = float(rowResult["latDMS"])
            rowResult["longitude"] = float(rowResult["longDMS"])
            
        scraperwiki.sqlite.save(unique_keys=['field'], data=rowResult)
    


#click on "clear data" and this will recreate the table with columns in the right order, there's no other way to re-order them
scraperwiki.sqlite.execute("create table if not exists swdata (field text, categories text, latitude real, longitude real, country text, geoLat real, geoLong real, latDMS real, longDMS real)")


#Below is an absolutely epic sparql query.  
#For anyone reading this who wants to understand how it works, 
#refer to the "Traversing Ontologies and (Sub)Classes; all subclasses of Person down the hierarchy" 
#section of http://webr3.org/blog/linked-data/virtuoso-6-sparqlgeo-and-linked-data/
#for a much more simple example


queryString = """PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
                PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dc:<http://purl.org/dc/terms/>
                PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
                PREFIX dbpprop:<http://dbpedia.org/property/>
                SELECT ?field 
                        (sql:group_digest(replace(replace(str(?category),"http://dbpedia.org/resource/Category:",""),'_',' '),", ",255,1) 
                            as ?categories)
                        (sql:sample(bif:either(str(?latNs)="S",-1,1)*(?latD+xsd:double(?latM)/60+xsd:double(?latS)/3600)) as ?latDMS)
                        (sql:sample(bif:either(str(?longEw)="W",-1,1)*(?longD+xsd:double(?longM)/60+xsd:double(?longS)/3600)) as ?longDMS)
                        (sql:sample(?geoLat) as ?geoLat)
                        (sql:sample(?geoLong) as ?geoLong)
                WHERE {
                  { SELECT ?category ?y WHERE {
                    ?category skos:broader ?y .
                    ?category rdfs:label ?categoryName .
                    FILTER (regex(?categoryName, "Oil fields", "i")) .
                  } }
                  OPTION ( TRANSITIVE, T_DISTINCT, t_in(?category), t_out(?y), t_step('path_id') as ?path, t_step(?category) as ?route, t_step('step_no') AS ?jump, T_DIRECTION 2 )
                  FILTER ( ?y = <http://dbpedia.org/resource/Category:Oil_fields_by_country> ) .
                  ?field dc:subject ?category .
                  OPTIONAL{?field dbpprop:latD ?latD} .
                  OPTIONAL{?field dbpprop:latM ?latM} .
                  OPTIONAL{?field dbpprop:latS ?latS} .
                  OPTIONAL{?field dbpprop:latNs ?latNs} .
                  OPTIONAL{?field dbpprop:longEw ?longEw} .
                  OPTIONAL{?field dbpprop:longD ?longD} .
                  OPTIONAL{?field dbpprop:longM ?longM} .
                  OPTIONAL{?field dbpprop:longS ?longS} .
                  OPTIONAL{?field geo:lat ?geoLat} .
                  OPTIONAL{?field geo:long ?geoLong} .
                  OPTIONAL{?field dbpprop:country ?country} .
                } group by ?field"""



parse_csv(csv_url(queryString))