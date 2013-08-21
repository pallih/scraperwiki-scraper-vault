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

query='SELECT DISTINCT ?b WHERE { ?a ?b ?c }'

endpoints=[('ordnancesurvey','http://api.talis.com/stores/ordnance-survey/services/sparql'),
           ('transport','http://services.data.gov.uk/transport/sparql'),
           ('education','http://services.data.gov.uk/education/sparql'),
           ('openuniversity','http://data.open.ac.uk/query'),
           ('analytics','http://services.data.gov.uk/analytics/sparql'),
           ('finance','http://services.data.gov.uk/finance/sparql')]
#('ordnancesurvey','http://api.talis.com/stores/ordnance-survey/services/sparql'),
idcount=1
           
for endpointpair in endpoints:
    datastore,endpoint=endpointpair
    if endpoint=='http://services.data.gov.uk/transport/sparql':
        query='SELECT DISTINCT ?b WHERE { ?a ?b ?c } LIMIT 27'
    elif endpoint=='http://api.talis.com/stores/ordnance-survey/services/sparql':
        query='SELECT DISTINCT ?b WHERE { ?a ?b ?c } LIMIT 40'
    results=run_sparql_query(query, endpoint)

    for row in results.rows:
        for item in row['result']:
            idcount+=1
            print datastore,item['b']['value']
            record={"id":idcount,"relation":item['b']['value'],"datastore":datastore}
            scraperwiki.datastore.save(["id"], record)     
