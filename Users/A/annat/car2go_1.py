import scraperwiki
import simplejson
import requests
from datetime import datetime

def save_resutls(json,time):
    for i in range(len(json)):

        try: 
            id = json[i]['vin']
        
        except IndexError:
            id = None

        try:
            street = json[i]['address'].split(",")[0]
            plz = json[i]['address'].split(",")[1].split()[0]
            city = json[i]['address'].split(",")[1].split()[1]

        except IndexError:
            street = None
            plz = None
            city = None

        try:
            lng = json[i]['coordinates'][0]
            lat = json[i]['coordinates'][1]

        except IndexError:
            lng = None
            lat = None
    
        try:
            fuelState = json[i]['fuel']

        except IndexError:
            fuelState = None

        try:
            innerCleanliness = json[i]['interior']
    
        except IndexError:
            innerCleanliness = None
    
        licensePlate = None
        

        data = {'id' : id,
                'street' : street,
                'plz' : plz,
                'city' : city,
                'lat' : lat,
                'lng' :lng,
                'time' : time,
                'fuelState' : fuelState,
                'innerCleanliness' : innerCleanliness,
                'licensePlate' : licensePlate,
                'time' : time}
    
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)

def main():
     
    url = "https://www.car2go.com/api/v2.1/vehicles?loc=Berlin&oauth_consumer_key=car2gowebsite&format=json&callback=?"
    json = simplejson.loads(requests.get(url, verify = False).text)
    vehicles = json['placemarks']   
    time = datetime.now()
    save_resutls(vehicles, time)

main()
import scraperwiki
import simplejson
import requests
from datetime import datetime

def save_resutls(json,time):
    for i in range(len(json)):

        try: 
            id = json[i]['vin']
        
        except IndexError:
            id = None

        try:
            street = json[i]['address'].split(",")[0]
            plz = json[i]['address'].split(",")[1].split()[0]
            city = json[i]['address'].split(",")[1].split()[1]

        except IndexError:
            street = None
            plz = None
            city = None

        try:
            lng = json[i]['coordinates'][0]
            lat = json[i]['coordinates'][1]

        except IndexError:
            lng = None
            lat = None
    
        try:
            fuelState = json[i]['fuel']

        except IndexError:
            fuelState = None

        try:
            innerCleanliness = json[i]['interior']
    
        except IndexError:
            innerCleanliness = None
    
        licensePlate = None
        

        data = {'id' : id,
                'street' : street,
                'plz' : plz,
                'city' : city,
                'lat' : lat,
                'lng' :lng,
                'time' : time,
                'fuelState' : fuelState,
                'innerCleanliness' : innerCleanliness,
                'licensePlate' : licensePlate,
                'time' : time}
    
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)

def main():
     
    url = "https://www.car2go.com/api/v2.1/vehicles?loc=Berlin&oauth_consumer_key=car2gowebsite&format=json&callback=?"
    json = simplejson.loads(requests.get(url, verify = False).text)
    vehicles = json['placemarks']   
    time = datetime.now()
    save_resutls(vehicles, time)

main()
