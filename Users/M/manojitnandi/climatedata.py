# -*- coding: utf-8 -*- 
import scraperwiki
from bs4 import BeautifulSoup
import time

def main():
    url = 'http://www.usclimatedata.com/'
    soup = BeautifulSoup(scraperwiki.scrape(url))
    results = soup.find('div', attrs = {'id':"main"})
    results = results.find('table')
    rows = results.findAll('td')
    for row in rows:
        state = row.text
        link = row.find('a').get('href')
        getCities(url,link,state)

def getCities(url,link,state):
    newUrl = url+link
    soup = BeautifulSoup(scraperwiki.scrape(newUrl))
    time.sleep(3)
    results = soup.find('div', attrs = {'id':'main'})
    results = results.find('table')
    rows = results.findAll('td')
    for row in rows:
        city_name = row.text
        city_link = row.find('a').get('href')
        getClimateInfo(url,city_link,city_name,state)

def getClimateInfo(url,link,city_name,state):
    climateUrl = url+link
    soup = BeautifulSoup(scraperwiki.scrape(climateUrl))
    time.sleep(2)
    results = soup.find('div', attrs = {'id':'main'})
    results = results.findAll('table')
    for table in results:
        trs = table.findAll('tr')
        if len(trs) == 4:
           #print trs
           header = getHeaders(trs[0])
           precipitation = getPrecipitation(trs[1:])
           if len(header) > 0:
               header = header[1:]
               keys = precipitation.keys()
               for i in range(len(header)):
                   month = header[i]
                   input = {"State":state,"City":city_name,"Month":month}
                   for key in keys:
                       values = precipitation[key]
                       value = values[i]
                       input[translateKeys(key.encode('ascii','ignore'))] = float(value)
                   scraperwiki.sqlite.save(unique_keys=['City',"State","Month"],data = input)
                         
          

def translateKeys(key):
    if key == "Average high in F":
        return "Average_High"
    elif key == "Average low in F":
        return "Average_Low"
    else:
        return "Average_Precipitation"

def getHeaders(tr):
    ths = tr.findAll('th')
    holder = []
    for th in ths:
        holder.append(th.text)
    return holder
    

def getPrecipitation(trs):
    information = {}
    for tr in trs:
        tds = tr.findAll('td')
        feature = tds[0].text
        tds = tds[1:]
        tds = [td.text for td in tds] 
        information[feature] = tds
    return information
        
    

main()
    


