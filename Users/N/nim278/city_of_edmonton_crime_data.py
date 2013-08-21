import scraperwiki
import httplib2, json, csv
import datetime

#to rebuild
#    scraperwiki.sqlite.execute("drop table `swdata`")         
#    scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`CommunityID` integer, `CommunityName` text, `Lat` real, `Lon` real, `OccurrenceTypeGroup` text, `Description` text, `Date` text)")
#    scraperwiki.sqlite.commit()

#first load
#startDate = '2012,01,26'
#endDate = '2012,04,25'
#normal load
startDate = (datetime.date.today() + datetime.timedelta(days=-5)).strftime('%Y,%m,%d')
endDate = (datetime.date.today() + datetime.timedelta(days=-1)).strftime('%Y,%m,%d')

http = httplib2.Http()
urlCom = 'http://crimemapping.edmontonpolice.ca/DataProvider.asmx/getCommunityInfo'
urlOcc = 'http://crimemapping.edmontonpolice.ca/DataProvider.asmx/getOccurrenceInfo'

for n in range(1,500):
    #first let's get the community info
    params = u'{communityID:'+str(n)+'}'    
    try:
        response, content = http.request(urlCom, 'POST', params, headers={'Content-type': 'application/json'})
    except:
        response, content = http.request(urlCom, 'POST', params, headers={'Content-type': 'application/json'})        
    
    #try to get the community name, if it doesn't exist, we don't bother querying the data
    try:
        strCommunityName = json.loads(content)['CommunityName']
    except:
        continue

    #then we get the details
    params = u'{neighbourhoodID:'+str(n)+',crimeTypes:"Assault;Sexual Assaults;Break and Enter;Theft From Vehicle;Homicide;Theft Of Vehicle;Robbery;Theft Over $5000",strStartDate:"'+startDate+'",strEndDate:"'+endDate+'"}'
    try:
        response, content = http.request(urlOcc, 'POST', params, headers={'Content-type': 'application/json'})
    except:
        response, content = http.request(urlOcc, 'POST', params, headers={'Content-type': 'application/json'})
    data = json.loads(content)

    for item in data:
        for occ in item['Occurrences']:
            scraperwiki.sqlite.save(unique_keys=["CommunityID","Lat","Lon","Description","Date"],
                data={"CommunityID":n,
                    "CommunityName":strCommunityName,
                    "Lat":occ['Location']['Lat'],
                    "Lon":occ['Location']['Lon'],
                    "OccurrenceTypeGroup":occ['OccurrenceTypeGroup'],
                    "Description":occ['Description'][:-15],
                    "Date":datetime.datetime.strptime(occ['Description'][-12:-1], '%b %d %Y').strftime('%Y-%m-%d')
                })