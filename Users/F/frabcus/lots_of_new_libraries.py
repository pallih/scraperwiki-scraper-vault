from cartodb import CartoDBAPIKey, CartoDBException

API_KEY ='YOUR_CARTODB_API_KEY'
cartodb_domain = 'jatorre'
cl = CartoDBAPIKey(API_KEY, cartodb_domain)
try:
    print cl.sql('select * from mytable')
except CartoDBException as e:
    print ("some error ocurred", e)from cartodb import CartoDBAPIKey, CartoDBException

API_KEY ='YOUR_CARTODB_API_KEY'
cartodb_domain = 'jatorre'
cl = CartoDBAPIKey(API_KEY, cartodb_domain)
try:
    print cl.sql('select * from mytable')
except CartoDBException as e:
    print ("some error ocurred", e)