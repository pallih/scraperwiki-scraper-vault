##############sunrise calculation from http://michelanders.blogspot.nl/2010/12/calulating-sunrise-and-sunset-in-python.html
## I would import it, but I can't therefore I have to define this as a function first.

from math import cos,sin,acos,asin,tan  
from math import degrees as deg, radians as rad  
import datetime

def timefromdecimalday(day):  
      """
      returns a datetime.time object.
       
      day is a decimal day between 0.0 and 1.0, e.g. noon = 0.5
      """  
      hours  = 24.0*day  
      h      = int(hours)  
      minutes= (hours-h)*60  
      m      = int(minutes)  
      seconds= (minutes-m)*60  
      s      = int(seconds)  
      return datetime.time(hour=h,minute=m,second=s)    
        
def calcSunTimes(onDate):  
      """
      Perform the actual calculations for sunrise, sunset and
      a number of related quantities.
      
      onDate is a datetime object

      The results are returned as a dict
      {sunrise, sunset, solarnoon}
      """  
      timezone = 1 # in hours, east is positive  #+1for european summertime. TODO: find a more elegant solution for this.
      longitude= 4.257188     # in decimal degrees, east is positive  #default coordinates for Scheveningen, NL
      latitude = 52.10155      # in decimal degrees, north is positive  
      
      time  = 0.5 # percentage past midnight, i.e. noon  is 0.5  
      daysDelta = onDate-datetime.datetime(1900,1,1,0,0)
      day   = daysDelta.days     # daynumber 1=1/1/1900  
       
      Jday     =day+2415018.5+time-timezone/24 # Julian day  
      Jcent    =(Jday-2451545)/36525    # Julian century  
      
      Manom    = 357.52911+Jcent*(35999.05029-0.0001537*Jcent)  
      Mlong    = 280.46646+Jcent*(36000.76983+Jcent*0.0003032)%360  
      Eccent   = 0.016708634-Jcent*(0.000042037+0.0001537*Jcent)  
      Mobliq   = 23+(26+((21.448-Jcent*(46.815+Jcent*(0.00059-Jcent*0.001813))))/60)/60  
      obliq    = Mobliq+0.00256*cos(rad(125.04-1934.136*Jcent))  
      vary     = tan(rad(obliq/2))*tan(rad(obliq/2))  
      Seqcent  = sin(rad(Manom))*(1.914602-Jcent*(0.004817+0.000014*Jcent))+sin(rad(2*Manom))*(0.019993-0.000101*Jcent)+sin(rad(3*Manom))*0.000289  
      Struelong= Mlong+Seqcent  
      Sapplong = Struelong-0.00569-0.00478*sin(rad(125.04-1934.136*Jcent))  
      declination = deg(asin(sin(rad(obliq))*sin(rad(Sapplong))))  
        
      eqtime   = 4*deg(vary*sin(2*rad(Mlong))-2*Eccent*sin(rad(Manom))+4*Eccent*vary*sin(rad(Manom))*cos(2*rad(Mlong))-0.5*vary*vary*sin(4*rad(Mlong))-1.25*Eccent*Eccent*sin(2*rad(Manom)))  
      
      hourangle= deg(acos(cos(rad(90.833))/(cos(rad(latitude))*cos(rad(declination)))-tan(rad(latitude))*tan(rad(declination))))  
      
      solarnoon =(720-4*longitude-eqtime+timezone*60)/1440  
      sunrise = solarnoon-hourangle*4/1440  
      sunset = solarnoon+hourangle*4/1440  
      
      print timefromdecimalday(sunrise)
      print timefromdecimalday(sunset)


      return {
        'solarnoon': timefromdecimalday(solarnoon),
        'sunrise': timefromdecimalday(sunrise),
        'sunset': timefromdecimalday(sunset)
      }
            

####################done calculating sunrise and sunset

#now for the real scraping

import scraperwiki
import dateutil.parser
import lxml.html

htmlWaves = scraperwiki.scrape("http://www.mumm.ac.be/NL/Models/Operational/Waves/table.php?station=hoekvanholland")
htmlWind = scraperwiki.scrape("http://www.mumm.ac.be/NL/Models/Operational/Wind/table.php?station=hoekvanholland")

     
rootWaves = lxml.html.fromstring(htmlWaves)
rootWind = lxml.html.fromstring(htmlWind)

rowsWaves = rootWaves.cssselect('''table[width="100%"][border="0"][cellspacing="0"][cellpadding="2"] tr''')
rowsWind = rootWind.cssselect('''table[width="100%"][border="0"][cellspacing="0"][cellpadding="3"] tr''')

data = {}
windDateTime = 0
i = 4 #the index of the starting row on the wind table
j = 0 #to check if we have past the tides scraping point

for trw in rowsWaves[3:]: #parse trough all rows in the waves table, starting at 3
    tdsw = trw.cssselect("td") #get a list of waves cell contents

    if len(tdsw)==5:
        #get the wave data
        dataWaves = {
            'datetime' : dateutil.parser.parse(tdsw[0].text_content()+" "+tdsw[1].text_content()),
            'time' : tdsw[1].text_content(), #just out of laziness
            'waveheight' : float(tdsw[2].text_content()),
            'pctswell' : int(tdsw[3].text_content())
        }

        #get the wind data from the same datestamp
        while windDateTime != dataWaves['datetime']: #skip forward until we find the same datestamp in the wind table
            tds = rowsWind[i].cssselect("td")
            if len(tds)==8:
                windDateTime = dateutil.parser.parse(tds[0].text_content()+" "+tds[1].text_content())
            i += 1
        else: #we apparently found the same datestamp
            dataWind = {
                'Bft' : int(tds[4].text_content()),
                'Wind_Direction_Deg' : int(tds[5].text_content())
            }

        #done. Save the data
        prevData = data #store for interpolation
        data = dict(dataWaves.items() + dataWind.items())

        #print data #for debugging
        scraperwiki.sqlite.save(unique_keys=['datetime'], data=data)

        #so far so good. If our only interest was waves and wind, we'd be done here.
        #and we could start the next iteration in the loop
        #the next code is for interpolating and adding tides


        #When time is 03:00 get sunrise and sundown times, and scrape tides
        # I have to wait until 03:00 so I can interpolate from the 00:00 timestamp.
        if dataWaves['time'] == "03:00" and prevData:
            dateTime = dataWaves['datetime']

            #build url string
            dateStr = str(dateTime.day)+"-"+str(dateTime.month)+"-"+str(dateTime.year)
            URLfirsthalf = "http://live.getij.nl/export.cfm?format=txt&from="
            URLdates = dateStr+"&to="+dateStr
            URLsecondhalf = "&uitvoer=1&interval=30&location=SCHEVNGN&Timezone=MET_DST&refPlane=NAP&graphRefPlane=NAP&bottom=0&keel=0"
            tidesURL = URLfirsthalf+URLdates+URLsecondhalf

            #get tide data
            txtTideLines = scraperwiki.scrape(tidesURL).split("\n")
            j = 14 #line 14 is the first line to contain actual data

            #get sunrise and sunsit times as a dict. Input is the current day.
            sunTimes = calcSunTimes(dataWaves['datetime'])
        
        if j:
            #if j, we have retrieved a tide table.
            for k in range(6): #6 half hours in 3h
                #Let's read line j of the tides file and focus on the tide in cm.
                #the tide in cm is stored in character 18:22
                #print txtTideLines[j][18:24]
                tide = int(txtTideLines[j][18:24])
                timeInterpolated = prevData['datetime']+datetime.timedelta(0,0,0,0,30*k) #store the time for this k-loop
                j += 1 #keep track of the index trough the tides table
            
                #also check wether the sun is shining. :)
                if timeInterpolated.time() > sunTimes['sunrise'] and timeInterpolated.time() < sunTimes['sunset']:
                    dayLight=1
                else:
                    dayLight=0
            
                #interpolate wave and wind data
                #and add tide and dayLight
                dataCombined = {
                    'Bft':int(prevData['Bft']+(data['Bft']-prevData['Bft'])/6.0*k),
                    'datetime': timeInterpolated, #increment in half hours
                    'waveheight': prevData['waveheight']+(data['waveheight']-prevData['waveheight'])/6*k,
                    'pctswell': prevData['pctswell']+int((data['pctswell']-prevData['pctswell'])/6*k),
                    'Wind_Direction_Deg': prevData['Wind_Direction_Deg']+int((data['Wind_Direction_Deg']-prevData['Wind_Direction_Deg'])/6*k),
                    'tide':tide,
                    'dayLight':dayLight
                }

                #print dataCombined['datetime']
                #print data['datetime']
                #print prevData['datetime']+datetime.timedelta(0,0,0,0,30*k)

                scraperwiki.sqlite.save(unique_keys=['datetime'], data=dataCombined)





