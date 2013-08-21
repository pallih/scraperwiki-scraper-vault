import scraperwiki

from cartodb import CartoDBOAuth, CartoDBException
#import json

user =  'newsbeastlabs@gmail.com'
password =  'TheDowntownHorseRocketFiasco555maps'
CONSUMER_KEY='aCUzZCTPpB6JChlkOvObHVZSgE1JcK3vcWAsGHXU'
CONSUMER_SECRET='yXfiMNeUlhJEaKnvTnF5z5GVVVmZ9NNLWFkM9FEv'
cartodb_domain = 'newsbeastlabs'
cl = CartoDBOAuth(CONSUMER_KEY, CONSUMER_SECRET, user, password, cartodb_domain)
