# TODO 
# figure out how to reorder columns in the sqlite database
# clean out unnecessary columns
# process coordinate information into a usuable form


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
    
#TODO the modifications made by Nono to the scraper below can be used to help clean up this query.
#https://scraperwiki.com/scrapers/wikipedia_power_plants/edit/

queryString = """PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
                PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dc:<http://purl.org/dc/terms/>
                PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
                PREFIX dbpprop:<http://dbpedia.org/property/>
                SELECT 
                    replace(replace(str(?plant),"http://dbpedia.org/resource/",""),"_"," ") as ?plant
                    replace(str(?plant),"http://dbpedia.org/resource/","http://en.wikipedia.org/wiki/") as ?wikipediaPage
                    sql:sample(bif:either(str(?latNs)="S",-1,1)*(?latD+xsd:double(?latM)/60+xsd:double(?latS)/3600)) as ?latDMS
                    sql:sample(bif:either(str(?longEw)="W",-1,1)*(?longD+xsd:double(?longM)/60+xsd:double(?longS)/3600)) as ?longDMS
                    (sql:sample(?geoLat) as ?geoLat)
                    (sql:sample(?geoLong) as ?geoLong)
                    sql:sample(replace(replace(str(?country),"http://dbpedia.org/resource/",""),"_"," ")) as ?country
                    sql:group_digest(replace(replace(str(?owner),"http://dbpedia.org/resource/",""),"_"," "), ", ",255,1) as ?owner
                    sql:sample(replace(replace(str(?city),"http://dbpedia.org/resource/",""),"_"," ")) as ?city
                    sql:group_digest(replace(replace(str(?mainContractor),"http://dbpedia.org/resource/",""),"_"," "), ", ",255,1) 
                       as ?mainContractor
                    sql:group_digest(replace(replace(str(?operator),"http://dbpedia.org/resource/",""),"_"," "), ", ",255,1) as ?operator
                    sql:sample(replace(replace(str(?province),"http://dbpedia.org/resource/",""),"_"," ")) as ?province
                    sql:group_digest(?capacityBblDay, " - ",255,1) as ?capacityBblDay
                    sql:group_digest(?oilRefiningCenter, " - ",255,1) as ?oilRefiningCenter
                    sql:group_digest(?founded, ", ",255,1) as ?founded
                    sql:group_digest(?refUnits, " - ",255,1) as ?refUnits
                    sql:group_digest(?oilTank, " - ",255,1) as ?oilTank
                    sql:group_digest(?capacity, " - ",255,1) as ?capacity
                    sql:group_digest(?closure, ", ",255,1) as ?closure
                    sql:group_digest(?employees, " - ",255,1) as ?employees WHERE {
                { SELECT ?category ?y WHERE { 
                  ?category skos:broader ?y . 
                  ?category rdfs:label ?categoryName . 
                  FILTER (regex(?categoryName, 'Oil refineries in ')) .
                } }
                OPTION ( TRANSITIVE, T_DISTINCT, t_in(?category), t_out(?y), t_step('path_id') as ?path, t_step(?category) as ?route, t_step('step_no') AS ?jump, T_DIRECTION 2 )
                FILTER ( ?y = <http://dbpedia.org/resource/Category:Oil_refineries_by_country> ) . 
                ?plant dc:subject ?category .
                OPTIONAL{?plant <http://dbpedia.org/property/capacityBbl/d> ?capacityBblDay }. 
                OPTIONAL{?plant dbpprop:oilRefiningCenter ?oilRefiningCenter}.
                OPTIONAL{?plant dbpprop:founded ?founded}.
                OPTIONAL{?plant dbpprop:refUnits ?refUnits}.
                OPTIONAL{?plant dbpprop:oilTank ?oilTank}.
                OPTIONAL{?plant dbpprop:capacity ?capacity}.
                OPTIONAL{?plant dbpprop:closure ?closure}.
                OPTIONAL{?plant dbpprop:mainContractor ?mainContractor}.
                OPTIONAL{?plant dbpprop:employees ?employees}.
                OPTIONAL{?plant dbpprop:operator ?operator}.
                OPTIONAL{?plant dbpprop:province ?province}.
                OPTIONAL{?plant dbpprop:owner ?owner}.
                OPTIONAL{?plant dbpprop:city ?city}.
                OPTIONAL{?plant dbpprop:country ?country}.
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
                } group by ?plant"""


#queryString = "select * where {?x ?y ?z} limit 10"
parse_csv(csv_url(queryString))# TODO 
# figure out how to reorder columns in the sqlite database
# clean out unnecessary columns
# process coordinate information into a usuable form


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
    
#TODO the modifications made by Nono to the scraper below can be used to help clean up this query.
#https://scraperwiki.com/scrapers/wikipedia_power_plants/edit/

queryString = """PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
                PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dc:<http://purl.org/dc/terms/>
                PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
                PREFIX dbpprop:<http://dbpedia.org/property/>
                SELECT 
                    replace(replace(str(?plant),"http://dbpedia.org/resource/",""),"_"," ") as ?plant
                    replace(str(?plant),"http://dbpedia.org/resource/","http://en.wikipedia.org/wiki/") as ?wikipediaPage
                    sql:sample(bif:either(str(?latNs)="S",-1,1)*(?latD+xsd:double(?latM)/60+xsd:double(?latS)/3600)) as ?latDMS
                    sql:sample(bif:either(str(?longEw)="W",-1,1)*(?longD+xsd:double(?longM)/60+xsd:double(?longS)/3600)) as ?longDMS
                    (sql:sample(?geoLat) as ?geoLat)
                    (sql:sample(?geoLong) as ?geoLong)
                    sql:sample(replace(replace(str(?country),"http://dbpedia.org/resource/",""),"_"," ")) as ?country
                    sql:group_digest(replace(replace(str(?owner),"http://dbpedia.org/resource/",""),"_"," "), ", ",255,1) as ?owner
                    sql:sample(replace(replace(str(?city),"http://dbpedia.org/resource/",""),"_"," ")) as ?city
                    sql:group_digest(replace(replace(str(?mainContractor),"http://dbpedia.org/resource/",""),"_"," "), ", ",255,1) 
                       as ?mainContractor
                    sql:group_digest(replace(replace(str(?operator),"http://dbpedia.org/resource/",""),"_"," "), ", ",255,1) as ?operator
                    sql:sample(replace(replace(str(?province),"http://dbpedia.org/resource/",""),"_"," ")) as ?province
                    sql:group_digest(?capacityBblDay, " - ",255,1) as ?capacityBblDay
                    sql:group_digest(?oilRefiningCenter, " - ",255,1) as ?oilRefiningCenter
                    sql:group_digest(?founded, ", ",255,1) as ?founded
                    sql:group_digest(?refUnits, " - ",255,1) as ?refUnits
                    sql:group_digest(?oilTank, " - ",255,1) as ?oilTank
                    sql:group_digest(?capacity, " - ",255,1) as ?capacity
                    sql:group_digest(?closure, ", ",255,1) as ?closure
                    sql:group_digest(?employees, " - ",255,1) as ?employees WHERE {
                { SELECT ?category ?y WHERE { 
                  ?category skos:broader ?y . 
                  ?category rdfs:label ?categoryName . 
                  FILTER (regex(?categoryName, 'Oil refineries in ')) .
                } }
                OPTION ( TRANSITIVE, T_DISTINCT, t_in(?category), t_out(?y), t_step('path_id') as ?path, t_step(?category) as ?route, t_step('step_no') AS ?jump, T_DIRECTION 2 )
                FILTER ( ?y = <http://dbpedia.org/resource/Category:Oil_refineries_by_country> ) . 
                ?plant dc:subject ?category .
                OPTIONAL{?plant <http://dbpedia.org/property/capacityBbl/d> ?capacityBblDay }. 
                OPTIONAL{?plant dbpprop:oilRefiningCenter ?oilRefiningCenter}.
                OPTIONAL{?plant dbpprop:founded ?founded}.
                OPTIONAL{?plant dbpprop:refUnits ?refUnits}.
                OPTIONAL{?plant dbpprop:oilTank ?oilTank}.
                OPTIONAL{?plant dbpprop:capacity ?capacity}.
                OPTIONAL{?plant dbpprop:closure ?closure}.
                OPTIONAL{?plant dbpprop:mainContractor ?mainContractor}.
                OPTIONAL{?plant dbpprop:employees ?employees}.
                OPTIONAL{?plant dbpprop:operator ?operator}.
                OPTIONAL{?plant dbpprop:province ?province}.
                OPTIONAL{?plant dbpprop:owner ?owner}.
                OPTIONAL{?plant dbpprop:city ?city}.
                OPTIONAL{?plant dbpprop:country ?country}.
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
                } group by ?plant"""


#queryString = "select * where {?x ?y ?z} limit 10"
parse_csv(csv_url(queryString))