import yql
import scraperwiki

def run_sparql_query(query, endpoint):
    '''
    # The following string replacement construction may be handy
    query = 'select * from flickr.photos.search where text=@text limit 3';
    y.execute(query, {"text": "panda"})
    '''
    y = yql.Public()
    query='select * from sparql.search where query="'+query+'" and service="'+endpoint+'"'
    env = "http://datatables.org/alltables.env"
    return y.execute(query, env=env)


'''
DEMO of:
- grabbing local authority code from postcode using Ordnance Survey SPARQL endpoint;
- then looking up secondary schools in that area (along with their opening date) using data.gov.uk education datastore

'''

os_query='''
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX admingeo: <http://data.ordnancesurvey.co.uk/ontology/admingeo/>
PREFIX postcode: <http://data.ordnancesurvey.co.uk/ontology/postcode/>

select ?district ?nsdistrict ?wardname ?districtname where {
<http://data.ordnancesurvey.co.uk/id/postcodeunit/MAGIC_POSTCODE> postcode:district ?district; postcode:ward ?ward.
?district skos:prefLabel ?districtname.
?ward skos:prefLabel ?wardname .
?district admingeo:hasCensusCode ?nsdistrict.
}
'''

postcode='MK7 6AA'
os_endpoint='http://api.talis.com/stores/ordnance-survey/services/sparql'
os_query=os_query.replace('MAGIC_POSTCODE',postcode.replace(' ',''))

result=run_sparql_query(os_query, os_endpoint)

for row in result.rows:
    print row['result']['nsdistrict']['value']
    districtcode=row['result']['nsdistrict']['value']
    print postcode,'is in the',row['result']['wardname']['value'],'ward of',row['result']['districtname']['value']
    record={ "id":postcode, "ward":row['result']['wardname']['value'],"district":row['result']['districtname']['value']}
    #scraperwiki.datastore.save(["id"], record) 


    
edu_endpoint='http://services.data.gov.uk/education/sparql'    

#example queries from http://www.simonhume.com/2010/02/10/using-sparql-the-data-gov-uk-school-data/

edu_query='''
prefix sch-ont:  <http://education.data.gov.uk/def/school/>
prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>

SELECT ?name ?reference ?date ?lat ?long WHERE {
?school a sch-ont:School;
sch-ont:establishmentName ?name;
sch-ont:uniqueReferenceNumber ?reference ;
sch-ont:districtAdministrative <http://statistics.data.gov.uk/id/local-authority-district/MAGIC_DISTRICTCODE> ;
sch-ont:openDate ?date ;
sch-ont:phaseOfEducation <http://education.data.gov.uk/def/school/PhaseOfEducation_Primary>;
geo:lat ?lat ;
geo:long ?long .
}
'''

edu_query=edu_query.replace('MAGIC_DISTRICTCODE',districtcode)
result=run_sparql_query(edu_query, edu_endpoint)
for row in result.rows:
    for school in row['result']:
        latlng=(float(school['lat']['value']), float(school['long']['value']))
        print school['name']['value'],school['reference']['value'],school['date']['value'],school['lat']['value'],school['long']['value'],latlng
        record={ "id":school['reference']['value'],"name":school['name']['value'],"openingDate":school['date']['value'],"lat":school['lat']['value'],"lon":school['long']['value']}
        scraperwiki.datastore.save(["id"], record,latlng=latlng) 
import yql
import scraperwiki

def run_sparql_query(query, endpoint):
    '''
    # The following string replacement construction may be handy
    query = 'select * from flickr.photos.search where text=@text limit 3';
    y.execute(query, {"text": "panda"})
    '''
    y = yql.Public()
    query='select * from sparql.search where query="'+query+'" and service="'+endpoint+'"'
    env = "http://datatables.org/alltables.env"
    return y.execute(query, env=env)


'''
DEMO of:
- grabbing local authority code from postcode using Ordnance Survey SPARQL endpoint;
- then looking up secondary schools in that area (along with their opening date) using data.gov.uk education datastore

'''

os_query='''
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX admingeo: <http://data.ordnancesurvey.co.uk/ontology/admingeo/>
PREFIX postcode: <http://data.ordnancesurvey.co.uk/ontology/postcode/>

select ?district ?nsdistrict ?wardname ?districtname where {
<http://data.ordnancesurvey.co.uk/id/postcodeunit/MAGIC_POSTCODE> postcode:district ?district; postcode:ward ?ward.
?district skos:prefLabel ?districtname.
?ward skos:prefLabel ?wardname .
?district admingeo:hasCensusCode ?nsdistrict.
}
'''

postcode='MK7 6AA'
os_endpoint='http://api.talis.com/stores/ordnance-survey/services/sparql'
os_query=os_query.replace('MAGIC_POSTCODE',postcode.replace(' ',''))

result=run_sparql_query(os_query, os_endpoint)

for row in result.rows:
    print row['result']['nsdistrict']['value']
    districtcode=row['result']['nsdistrict']['value']
    print postcode,'is in the',row['result']['wardname']['value'],'ward of',row['result']['districtname']['value']
    record={ "id":postcode, "ward":row['result']['wardname']['value'],"district":row['result']['districtname']['value']}
    #scraperwiki.datastore.save(["id"], record) 


    
edu_endpoint='http://services.data.gov.uk/education/sparql'    

#example queries from http://www.simonhume.com/2010/02/10/using-sparql-the-data-gov-uk-school-data/

edu_query='''
prefix sch-ont:  <http://education.data.gov.uk/def/school/>
prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>

SELECT ?name ?reference ?date ?lat ?long WHERE {
?school a sch-ont:School;
sch-ont:establishmentName ?name;
sch-ont:uniqueReferenceNumber ?reference ;
sch-ont:districtAdministrative <http://statistics.data.gov.uk/id/local-authority-district/MAGIC_DISTRICTCODE> ;
sch-ont:openDate ?date ;
sch-ont:phaseOfEducation <http://education.data.gov.uk/def/school/PhaseOfEducation_Primary>;
geo:lat ?lat ;
geo:long ?long .
}
'''

edu_query=edu_query.replace('MAGIC_DISTRICTCODE',districtcode)
result=run_sparql_query(edu_query, edu_endpoint)
for row in result.rows:
    for school in row['result']:
        latlng=(float(school['lat']['value']), float(school['long']['value']))
        print school['name']['value'],school['reference']['value'],school['date']['value'],school['lat']['value'],school['long']['value'],latlng
        record={ "id":school['reference']['value'],"name":school['name']['value'],"openingDate":school['date']['value'],"lat":school['lat']['value'],"lon":school['long']['value']}
        scraperwiki.datastore.save(["id"], record,latlng=latlng) 
