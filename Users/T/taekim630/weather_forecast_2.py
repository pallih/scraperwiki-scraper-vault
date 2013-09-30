#Kevin Kim
#self; no group
#5.6.13 
#Scraper Wiki Script in-class exercise

import scraperwiki       
 
#This scraper pulls weather information including highest and lowest temperatures in each date.  
import lxml.html

#This part assigns specific web site that we are going to pull out information to scrape
html = scraperwiki.scrape("http://www.weather.com/weather/tenday/Washington+DC+USDC0001:1:US")
root = lxml.html.fromstring(html)


#This part loops through all divs, particular with "wx-daypart" class which contains all weather information that I need
for row in root.cssselect("div[class='wx-daypart']"):
    
    #Date includes day and date
    date = row.cssselect("h3")

    #high indcates higest temperature in Fahrenheit on each day
    high = row.cssselect("p[class='wx-temp']")    

    #low indcates lowest temperature in Fahrenheit on each day
    low = row.cssselect("p[class='wx-temp-alt']")

    #rain indicates chance of rain in percent on each day
    rain = row.cssselect("dd")    
    
    #This part saves data in list format
    data = {  
        'date' : date[0].text_content(),
        'high' : high[0].text_content(), 
        'low' : low[0].text_content(),
        'rain' : rain[0].text_content()
    }
    #This part prints out data
    print data
    
    #This part assigns unique keys and saves data into database
    scraperwiki.sqlite.save(unique_keys=['date'], data=data)#Kevin Kim
#self; no group
#5.6.13 
#Scraper Wiki Script in-class exercise

import scraperwiki       
 
#This scraper pulls weather information including highest and lowest temperatures in each date.  
import lxml.html

#This part assigns specific web site that we are going to pull out information to scrape
html = scraperwiki.scrape("http://www.weather.com/weather/tenday/Washington+DC+USDC0001:1:US")
root = lxml.html.fromstring(html)


#This part loops through all divs, particular with "wx-daypart" class which contains all weather information that I need
for row in root.cssselect("div[class='wx-daypart']"):
    
    #Date includes day and date
    date = row.cssselect("h3")

    #high indcates higest temperature in Fahrenheit on each day
    high = row.cssselect("p[class='wx-temp']")    

    #low indcates lowest temperature in Fahrenheit on each day
    low = row.cssselect("p[class='wx-temp-alt']")

    #rain indicates chance of rain in percent on each day
    rain = row.cssselect("dd")    
    
    #This part saves data in list format
    data = {  
        'date' : date[0].text_content(),
        'high' : high[0].text_content(), 
        'low' : low[0].text_content(),
        'rain' : rain[0].text_content()
    }
    #This part prints out data
    print data
    
    #This part assigns unique keys and saves data into database
    scraperwiki.sqlite.save(unique_keys=['date'], data=data)