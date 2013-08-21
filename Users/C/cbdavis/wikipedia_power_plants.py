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
            
        scraperwiki.sqlite.save(unique_keys=['plant'], data=rowResult)
    


#click on "clear data" and this will recreate the table with columns in the right order, there's no other way to re-order them
scraperwiki.sqlite.execute("create table if not exists swdata (plant text, categories text, latitude real, longitude real, country text, locale text, owner text, primaryFuel text, secondaryFuel text, installedCapacity text, status text, generationUnits text, averageAnnualGen text, commissionned text, geoLat real, geoLong real, latDMS real, longDMS real)")


#Below is an absolutely epic sparql query.  
#For anyone reading this who wants to understand how it works, 
#refer to the "Traversing Ontologies and (Sub)Classes; all subclasses of Person down the hierarchy" 
#section of http://webr3.org/blog/linked-data/virtuoso-6-sparqlgeo-and-linked-data/
#for a much more simple example


#Some of these powerplants can have multiple matching categories, especially if they run on two different fuel types
#Some of them also have several coordinates that could be combined in a number of ways if using a flat SPARQL query
#By using "group by" we make sure to keep only one row per power plant
#Note: using coalesce to give precedence to geolat/geolon directly in sparql leads to a strange error

#In running a test over a minimal query based on the one used on the wikipedia_oil_refineries scraper, it seems that "group by" 
#isn't enough to ensure only one row per power plant, but the use of sql:sample and sql:group_digest does the trick.  
#It doesn't seem clear if this is causing fewer records to be retrieved since the database uses a primary key based on the plant name.  

#According to this scraper's history, it looks like fewer results are being returned.
#Run succeeded: - ran 6 times, most recently for 335 seconds (1 scraped pages, 2654 records) 07:41, 25 October 2012
#Run succeeded: - ran 2 times, most recently for 973 seconds (1 scraped pages, 3116 records) 22:35, 18 October 2012

#Looking at the scraper's history it looks like the record number dropped while there were no more edits to the scraper's code
#"run_ended": "2012-10-20T21:17:22", "run_started": "2012-10-20T21:09:56", "records_produced": 3136
#"run_ended": "2012-10-21T21:27:36", "run_started": "2012-10-21T21:25:04", "records_produced": 2649
#So, something might have happened on DBPedia's side. And indeed there are now 6 more categories with encoding issue on colon...

#The query has been improved to include use of type:PowerStation, this helps getting power plants for which category suffers from the encoding glitch
#By now only infobox:Power_Station is mapped, but the same could ne done with Infobox:Dam at least where there is an installed capacity
#It seems that even power plants only listed in tables could be mapped and thus available in DBPedia as entries
#(see http://mappings.dbpedia.org/index.php/How_to_edit_DBpedia_Mappings#How_to_map_a_Wikipedia_Table)
queryString = """PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
                PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dc:<http://purl.org/dc/terms/>
                PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
                PREFIX dbpprop:<http://dbpedia.org/property/>
                PREFIX dbp-owl:<http://dbpedia.org/ontology/>
                SELECT ?plant 
                        (sql:group_digest(replace(replace(str(?category),"http://dbpedia.org/resource/Category:",""),'_',' '),", ",255,1) 
                            as ?categories)
                        (sql:sample(bif:either(str(?latNs)="S",-1,1)*(?latD+xsd:double(?latM)/60+xsd:double(?latS)/3600)) as ?latDMS)
                        (sql:sample(bif:either(str(?longEw)="W",-1,1)*(?longD+xsd:double(?longM)/60+xsd:double(?longS)/3600)) as ?longDMS)
                        (sql:sample(?geoLat) as ?geoLat)
                        (sql:sample(?geoLong) as ?geoLong)
                        (sql:sample(replace(replace(str(?country),"http://dbpedia.org/resource/",""),"_"," ")) as ?country)
                        (sql:sample(replace(replace(str(?locale),"http://dbpedia.org/resource/",""),"_"," ")) as ?locale)
                        (sql:sample(replace(replace(str(?owner),"http://dbpedia.org/resource/",""),"_"," ")) as ?owner)
                        (sql:sample(replace(replace(str(?primaryFuel),"http://dbpedia.org/resource/",""),"_"," ")) as ?primaryFuel)
                        (sql:sample(replace(replace(str(?secondaryFuel),"http://dbpedia.org/resource/",""),"_"," ")) as ?secondaryFuel)
                        (sql:group_digest(?installedCapacity," - ",255,1) as ?installedCapacity)
                        (sql:sample(?status) as ?status)
                        (sql:sample(?generationUnits) as ?generationUnits)
                        (sql:sample(?averageAnnualGen) as ?averageAnnualGen)
                        (min(?commissionned) as ?commissionned)
                WHERE {
                  {{ SELECT ?category ?y WHERE {
                    ?category skos:broader ?y .
                    ?category rdfs:label ?categoryName .
                    FILTER (regex(?categoryName, "power station", "i") ||
                    regex(?categoryName, "power plant", "i") ||
                    regex(?categoryName, "CHP plants", "i") ||
                    regex(?categoryName, "Wave farms", "i") ||
                    regex(?categoryName, "Wind farms", "i")) .
                  } }
                  OPTION ( TRANSITIVE, T_DISTINCT, t_in(?category), t_out(?y), t_step('path_id') as ?path, t_step(?category) as ?route, t_step('step_no') AS ?jump, T_DIRECTION 2 )
                  FILTER ( ?y = <http://dbpedia.org/resource/Category:Power_stations_by_country> )
                  ?plant dc:subject ?category . 
                  } UNION  { { SELECT ?plant WHERE { ?plant rdf:type dbp-owl:PowerStation  }  } }
                  OPTIONAL{?plant dbpprop:latD ?latD} .
                  OPTIONAL{?plant dbpprop:latM ?latM} .
                  OPTIONAL{?plant dbpprop:latS ?latS} .
                  OPTIONAL{?plant dbpprop:latNs ?latNs} .
                  OPTIONAL{?plant dbpprop:longEw ?longEw} .
                  OPTIONAL{?plant dbpprop:longD ?longD} .
                  OPTIONAL{?plant dbpprop:longM ?longM} .
                  OPTIONAL{?plant dbpprop:longS ?longS} .
                  OPTIONAL{?plant geo:lat ?geoLat} .
                  OPTIONAL{?plant geo:long ?geoLong} .
                  OPTIONAL{?plant dbpprop:country ?country} .
                  OPTIONAL{?plant dbpprop:locale ?locale} .
                  OPTIONAL{?plant dbpprop:owner ?owner} .
                  OPTIONAL{?plant dbpprop:primaryFuel ?primaryFuel} .
                  OPTIONAL{?plant dbpprop:secondaryFuel ?secondaryFuel} .
                  OPTIONAL{?plant dbpprop:installedCapacity ?installedCapacity} .
                  OPTIONAL{?plant dbpprop:status ?status} .
                  OPTIONAL{?plant dbpprop:generationUnits ?generationUnits} .
                  OPTIONAL{?plant dbpprop:averageAnnualGen ?averageAnnualGen} .
                  OPTIONAL{?plant dbpprop:status ?status} .
                  OPTIONAL{?plant dbpprop:commissionned ?commissionned} .
                  OPTIONAL{?plant dbpprop:decommissionned ?decommissionned} .
                  OPTIONAL{?plant dbpprop:technology ?technology} .
                  OPTIONAL{?plant dbpprop:coolingWater ?coolingWater} .
                } group by ?plant"""


#queryString = "select * where {?x ?y ?z} limit 10"
parse_csv(csv_url(queryString))
#If 10000 results are returned, the the query above needs to be modified to have LIMIT 10000 and then have values of OFFSET defined in increments of 10000