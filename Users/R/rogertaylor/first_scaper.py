import os
import datetime
import re
import urllib
import lxml.html
import scraperwiki

BASE_URL = "http://www.sportinglife.com"


def GetRaces():
    url = BASE_URL + "/greyhounds/results/04-06-2013"
    
    race_urls = []
    races = []
    races_batch = []
    dogs_batch = []
    
    response = urllib.urlopen(url)
    tree = lxml.html.parse(response)

    for link in tree.xpath("//section[@id='content']/section/ul[2]/li/ul/li[*]/a"):
        race_link = link.attrib.get('href').strip()
        race_urls.append(race_link)
        race_id = race_link.split('/')[6]
        
        record = []
        record = (race_link, race_id)

        races.append(record)

    GetRaceDetails(races, races_batch, dogs_batch)

    SaveRacesDogsDict (races_batch, dogs_batch)


def SaveRacesDogsDict (races_batch, dogs_batch):
    
    print dogs_batch
    print races_batch
    
    scraperwiki.sqlite.save(unique_keys=["race_id"],data=races_batch,table_name="races")
    scraperwiki.sqlite.save(unique_keys=["id"],data=dogs_batch,table_name="race_results")


def GetRaceDetails(races, races_batch, dogs_batch):
    
    for race in races:
       
        url = "%s%s" % (BASE_URL, race[0])
        race_id = race[1]
        
        response = urllib.urlopen(url)
        tree = lxml.html.parse(response)

        class_dist = tree.xpath("//section[@id='content']/section/div/div/h2/span")[0].text.split()
        race_class = class_dist[0].strip()
        race_distance = class_dist[1].strip()
        prizes = tree.xpath("//section[@id='content']/section/div/div/ul/li")[0].text
        prizes = re.sub('(\xc3\x82\xc2\xa3|\xc2\xa3|\xa31|\xc2\xa3|GBP)', 'GBP', prizes)
        r = len(tree.xpath("//section[@id='content']/section/div[2]/div/ul/li"))
        offtime = tree.xpath("//section[@id='content']/section/div[2]/div/ul/li")[r-1].text.strip().replace('Off time: ','')
        race_date = race[0].split('/')[3].strip()
        race_time = tree.xpath("//section[@id='content']/section/div/div/h2")[0].text.strip()
        venue = tree.xpath("//section[@id='content']/nav/h1")[0].text.strip()

        record = {}
        record['race_id'] = race_id
        record['race_url'] = url
        record['race_date'] = race_date
        record['race_time'] = race_time
        record['offtime'] = offtime
        record['venue'] = venue
        record['race_class'] = race_class
        record['race_distance'] = race_distance
        record['prizes'] = prizes
       
        races_batch.append(SetRacesDict(race_id, url, race_date, race_time, offtime, venue, race_class, race_distance, prizes))
        
        #races_batch.append(SetRacesList(race_id, url, race_date, race_time, offtime, venue, race_class, race_distance, prizes))       

        GetRaceDogsDetails(tree,race_id, dogs_batch)
   

def SetRacesDict(race_id, url, race_date, race_time, offtime, venue, race_class, race_distance, prizes):
    record = {}
    record['race_id'] = race_id
    record['race_url'] = url
    record['race_date'] = race_date
    record['race_time'] = race_time
    record['offtime'] = offtime
    record['venue'] = venue
    record['race_class'] = race_class
    record['race_distance'] = race_distance
    record['prizes'] = prizes

    return record



def SetRacesList(race_id, url, race_date, race_time, offtime, venue, race_class, race_distance, prizes):

    return (race_id, url, race_date, race_time, offtime, venue, race_class, race_distance, prizes)


def GetRaceDogsDetails(tree, race_id, batch):
    
    for row in tree.xpath("//section[@id='content']/table/tbody/tr"):
        record = {}   

        position = StripStr(row[0].cssselect("strong")[0].text)
        if position <> 'NR' and len(position)>0 :
            trap = StripStr(row[0].text_content() )
            sex_colour = StripStr(row[2].cssselect("em")[0].text.replace("(",'').replace(")",'')).split('-')
            dog_url = row[2].cssselect("a[href]")[0].attrib['href']
            id = race_id + position
            dog_id = dog_url.split('/')[5]
            distance = StripStr(row[1].text)
            trap = trap[trap.find("(")+1:trap.find(")")]
            dog_url = BASE_URL + dog_url
            dog_name = row[2].cssselect("a[href]")[0].text_content().strip()
            sex = StripStr(sex_colour[0])
            colour = StripStr(sex_colour[1])
            comment = StripStr(row[2].cssselect("small")[0].text)
            trainer = StripStr(row[3].text)
            age = StripStr(row[4].text)
            weight = StripStr(row[5].text)
            bendpos = StripStr(row[6].text)
            runtime = StripStr(row[7].text)
            adj = StripStr(row[8].text)
            sect = StripStr(row[9].text)
            sp = StripStr(row[10].text)


            #print record

            batch.append(SetDogDict(id, dog_id, race_id, position, distance,trap, dog_url,dog_name,sex,colour,comment,trainer,age,weight,bendpos,runtime,adj,sect,sp))
        
            #batch.append(SetDogList(id,  dog_id, race_id, position, distance,trap,  dog_url,dog_name,sex,colour,comment,trainer,age,weight,bendpos,runtime,adj,sect,sp))
            
            #print batch


def SetDogDict(id, dog_id, race_id, position, distance,trap, dog_url,dog_name,sex,colour,comment,trainer,age,weight,bendpos,runtime,adj,sect,sp):
    
    record = {}

    record['id'] = id
    record['dog_id'] = dog_id
    record['race_id'] = race_id
    record['position'] = position
    record['distance'] = distance
    record['trap'] = trap
    record['dog_url'] = dog_url
    record['dog_name'] = dog_name
    record['sex'] = sex
    record['colour'] = colour
    record['comment'] = comment
    record['trainer'] = trainer
    record['age'] = age
    record['weight'] = weight
    record['bendpos'] = bendpos
    record['runtime'] = runtime
    record['adj'] = adj
    record['sect'] = sect
    record['sp'] = sp

    return record


def SetDogList(id, dog_id, race_id, position, distance,trap, dog_url,dog_name,sex,colour,comment,trainer,age,weight,bendpos,runtime,adj,sect,sp):
    
    return (id, dog_id, race_id, position, distance,trap, dog_url,dog_name,sex,colour,comment,trainer,age,weight,bendpos,runtime,adj,sect,sp)


def StripStr (string):
    return string.strip() if string else ''



GetRaces()