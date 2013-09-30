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
    #it seems that categoria traversals are not possible using the main dbpedia endpoint, but are possible using the live endpoint
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


#Some of these powerplants can have multiple matching categories, especially if they run on two different fuel types
#Some of them also have several coordinates that could be combined in a number of ways if using a flat SPARQL query
#By using "group by" we make sure to keep only one row per power plant
#Note: using coalesce to give precedence to geolat/geolon directly in sparql leads to a strange error
queryString = """PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
                PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dc:<http://purl.org/dc/terms/>
                PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
                PREFIX dbpprop:<http://dbpedia.org/property/>
                SELECT ?plant (sql:group_digest(replace(replace(str(?categoria),"http://dbpedia.org/resource/categoria:",""),'_',' '),", ",255,1) as ?categories) (sql:sample(bif:either(str(?latNs)="S",-1,1)*(?latD+xsd:double(?latM)/60+xsd:double(?latS)/3600)) as ?latDMS) (sql:sample(bif:either(str(?longEw)="W",-1,1)*(?longD+xsd:double(?longM)/60+xsd:double(?longS)/3600)) as ?longDMS) (sql:sample(?geoLat) as ?geoLat) (sql:sample(?geoLong) as ?geoLong) (sql:sample(replace(replace(str(?country),"http://dbpedia.org/resource/",""),"_"," ")) as ?country) (sql:sample(replace(replace(str(?locale),"http://dbpedia.org/resource/",""),"_"," ")) as ?locale) (sql:sample(replace(replace(str(?owner),"http://dbpedia.org/resource/",""),"_"," ")) as ?owner) (sql:sample(replace(replace(str(?primaryFuel),"http://dbpedia.org/resource/",""),"_"," ")) as ?primaryFuel) (sql:sample(replace(replace(str(?secondaryFuel),"http://dbpedia.org/resource/",""),"_"," ")) as ?secondaryFuel) (sql:group_digest(?installedCapacity," - ",255,1) as ?installedCapacity) (sql:sample(?status) as ?status) (sql:sample(?generationUnits) as ?generationUnits) (sql:sample(?averageAnnualGen) as ?averageAnnualGen) (min(?commissionned) as ?commissionned)
                WHERE {
                  { SELECT ?categoria ?y WHERE {
                    ?categoria skos:broader ?y .
                    ?categoria rdfs:label ?categoriaName .
                    FILTER (regex(?categoriaName, "Lebanon", "i") ||
                    regex(?categoriaName, "Lebanon", "i") ||
                    regex(?categoriaName, "CHP plants", "i") ||
                    regex(?categoriaName, "Wave farms", "i") ||
                    regex(?categoriaName, "Wind farms", "i")) .
                  } }
                  OPTION ( TRANSITIVE, T_DISTINCT, t_in(?categoria), t_out(?y), t_step('path_id') as ?path, t_step(?categoria) as ?route, t_step('step_no') AS ?jump, T_DIRECTION 2 )
                  FILTER ( ?y = <http://dbpedia.org/resource/Categoria:Lebanon> ) .
                  ?plant dc:subject ?categoria .
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
#If 10000 results are returned, the the query above needs to be modified to have LIMIT 10000 and then have values of OFFSET defined in increments of 10000import csv
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
    #it seems that categoria traversals are not possible using the main dbpedia endpoint, but are possible using the live endpoint
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


#Some of these powerplants can have multiple matching categories, especially if they run on two different fuel types
#Some of them also have several coordinates that could be combined in a number of ways if using a flat SPARQL query
#By using "group by" we make sure to keep only one row per power plant
#Note: using coalesce to give precedence to geolat/geolon directly in sparql leads to a strange error
queryString = """PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
                PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dc:<http://purl.org/dc/terms/>
                PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
                PREFIX dbpprop:<http://dbpedia.org/property/>
                SELECT ?plant (sql:group_digest(replace(replace(str(?categoria),"http://dbpedia.org/resource/categoria:",""),'_',' '),", ",255,1) as ?categories) (sql:sample(bif:either(str(?latNs)="S",-1,1)*(?latD+xsd:double(?latM)/60+xsd:double(?latS)/3600)) as ?latDMS) (sql:sample(bif:either(str(?longEw)="W",-1,1)*(?longD+xsd:double(?longM)/60+xsd:double(?longS)/3600)) as ?longDMS) (sql:sample(?geoLat) as ?geoLat) (sql:sample(?geoLong) as ?geoLong) (sql:sample(replace(replace(str(?country),"http://dbpedia.org/resource/",""),"_"," ")) as ?country) (sql:sample(replace(replace(str(?locale),"http://dbpedia.org/resource/",""),"_"," ")) as ?locale) (sql:sample(replace(replace(str(?owner),"http://dbpedia.org/resource/",""),"_"," ")) as ?owner) (sql:sample(replace(replace(str(?primaryFuel),"http://dbpedia.org/resource/",""),"_"," ")) as ?primaryFuel) (sql:sample(replace(replace(str(?secondaryFuel),"http://dbpedia.org/resource/",""),"_"," ")) as ?secondaryFuel) (sql:group_digest(?installedCapacity," - ",255,1) as ?installedCapacity) (sql:sample(?status) as ?status) (sql:sample(?generationUnits) as ?generationUnits) (sql:sample(?averageAnnualGen) as ?averageAnnualGen) (min(?commissionned) as ?commissionned)
                WHERE {
                  { SELECT ?categoria ?y WHERE {
                    ?categoria skos:broader ?y .
                    ?categoria rdfs:label ?categoriaName .
                    FILTER (regex(?categoriaName, "Lebanon", "i") ||
                    regex(?categoriaName, "Lebanon", "i") ||
                    regex(?categoriaName, "CHP plants", "i") ||
                    regex(?categoriaName, "Wave farms", "i") ||
                    regex(?categoriaName, "Wind farms", "i")) .
                  } }
                  OPTION ( TRANSITIVE, T_DISTINCT, t_in(?categoria), t_out(?y), t_step('path_id') as ?path, t_step(?categoria) as ?route, t_step('step_no') AS ?jump, T_DIRECTION 2 )
                  FILTER ( ?y = <http://dbpedia.org/resource/Categoria:Lebanon> ) .
                  ?plant dc:subject ?categoria .
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