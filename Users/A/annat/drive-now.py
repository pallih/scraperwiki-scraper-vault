import scraperwiki
import simplejson
import requests
from datetime import datetime

def save_resutls(json, selected_city, time):

    for i in range(len(json)):

        try: 
            city = unicode(json[i]['address'].split(",")[1].split()[1])
        
            if selected_city == city:
                try: 
                    id = json[i]['int']
        
                except IndexError:
                    id = None
        
                try:
                    street = json[i]['address'].split(",")[0]
                    plz =  json[i]['address'].split(",")[1].split()[0]   
            
                except IndexError: 
                    street = None
                    plz = None
                    
                try:
                    lat = json[i]['position']['latitude']
                    lng = json[i]['position']['longitude']
            
                except IndexError:    
                    lat = None
                    lng = None                        
                 

                try:
                    fuelState = json[i]['fuelState']

                except:
                    fuelState = None

                try:
                    innerCleanliness = json[i]['innerCleanliness']

                except:
                    innerCleanliness = None 

                try:
                    licensePlate = json[i]["licensePlate"]
                
                except:
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

        except IndexError: 
            city = None
            
def main():
    
    
    selected_city = "Berlin"
    url = "https://de.drive-now.com/php/metropolis/json.vehicle_filter"
    json = simplejson.loads(requests.get(url, verify = False).text)
    vehicles = json['rec']['vehicles']['vehicles']
    time = datetime.now()    
    
    save_resutls(vehicles, selected_city, time)

main()
