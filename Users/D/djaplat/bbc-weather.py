import scraperwiki
import re
from lxml import etree
from pyquery import PyQuery as pq

from mechanize import Browser
from BeautifulSoup import BeautifulSoup

mech = Browser()
url = "http://www.bbc.co.uk/weather/2988507"
page = mech.open(url)

html = page.read()
soup = BeautifulSoup(html)
daily_window = soup.find('div', {'class' : 'daily-window'})


d = pq(html)
class_daily = d('ul.daily')

lis = class_daily.find('li')
for li in lis:
    day = pq(li).find('.abbrev').text()
    icon = pq(li).find('span img').attr('alt')
    print icon



# de div met class tabbed-forecast met de weersvooruitzichten
tabbedforecast = soup.find("ul", { "class" : "daily"})

# de li's bevatten de weersvoorspellingen per dag
lis = tabbedforecast.findAll("li")

lst = []

for li in lis:
    day = li.a.h3.span.contents[0].text + li.a.h3.span.contents[1].text

    icon = li.a.contents[3]['class']
    icon = re.split("weather-type-", icon)
    icon = icon[3]

    description = li.a.contents[3].img['alt']
    
    try:
        li.a.find("span", {"class":"max-temp"}).find("span", {"class":"units-value temperature-value temperature-value-unit-c"}).text
    except AttributeError:
        try:
            li.a.find("span", {"class":"min-temp"}).find("span", {"class":"units-value temperature-value temperature-value-unit-c"}).text
        except AttributeError:
            max_temp = ""
        else:
            max_temp = li.a.find("span", {"class":"min-temp"}).find("span", {"class":"units-value temperature-value temperature-value-unit-c"}).text
            max_temp = re.split("(\xb0C)", max_temp)
            max_temp = max_temp[0]
    else:
        max_temp = li.a.find("span", {"class":"max-temp"}).find("span", {"class":"units-value temperature-value temperature-value-unit-c"}).text
        max_temp = re.split("(\xb0C)", max_temp)
        max_temp = max_temp[0]

    windspeed = li.a.find("span", {"class":"units-value windspeed-value windspeed-value-unit-kph"}).text
    winddirection = li.a.find("span", {"class":"description blq-hide"}).text
    humidity = "na"
    pressure = "na"
    visibility = "na"

    lst.append({'day':day, 
                'icon':icon, 
                'description':description, 
                'max_temp':max_temp, 
                'min_temp':max_temp, 
                'winddirection':winddirection, 
                'windspeed':windspeed, 
                'humidity':humidity, 
                'pressure':pressure, 
                'visibility':visibility})

print lst

import scraperwiki
import re
from lxml import etree
from pyquery import PyQuery as pq

from mechanize import Browser
from BeautifulSoup import BeautifulSoup

mech = Browser()
url = "http://www.bbc.co.uk/weather/2988507"
page = mech.open(url)

html = page.read()
soup = BeautifulSoup(html)
daily_window = soup.find('div', {'class' : 'daily-window'})


d = pq(html)
class_daily = d('ul.daily')

lis = class_daily.find('li')
for li in lis:
    day = pq(li).find('.abbrev').text()
    icon = pq(li).find('span img').attr('alt')
    print icon



# de div met class tabbed-forecast met de weersvooruitzichten
tabbedforecast = soup.find("ul", { "class" : "daily"})

# de li's bevatten de weersvoorspellingen per dag
lis = tabbedforecast.findAll("li")

lst = []

for li in lis:
    day = li.a.h3.span.contents[0].text + li.a.h3.span.contents[1].text

    icon = li.a.contents[3]['class']
    icon = re.split("weather-type-", icon)
    icon = icon[3]

    description = li.a.contents[3].img['alt']
    
    try:
        li.a.find("span", {"class":"max-temp"}).find("span", {"class":"units-value temperature-value temperature-value-unit-c"}).text
    except AttributeError:
        try:
            li.a.find("span", {"class":"min-temp"}).find("span", {"class":"units-value temperature-value temperature-value-unit-c"}).text
        except AttributeError:
            max_temp = ""
        else:
            max_temp = li.a.find("span", {"class":"min-temp"}).find("span", {"class":"units-value temperature-value temperature-value-unit-c"}).text
            max_temp = re.split("(\xb0C)", max_temp)
            max_temp = max_temp[0]
    else:
        max_temp = li.a.find("span", {"class":"max-temp"}).find("span", {"class":"units-value temperature-value temperature-value-unit-c"}).text
        max_temp = re.split("(\xb0C)", max_temp)
        max_temp = max_temp[0]

    windspeed = li.a.find("span", {"class":"units-value windspeed-value windspeed-value-unit-kph"}).text
    winddirection = li.a.find("span", {"class":"description blq-hide"}).text
    humidity = "na"
    pressure = "na"
    visibility = "na"

    lst.append({'day':day, 
                'icon':icon, 
                'description':description, 
                'max_temp':max_temp, 
                'min_temp':max_temp, 
                'winddirection':winddirection, 
                'windspeed':windspeed, 
                'humidity':humidity, 
                'pressure':pressure, 
                'visibility':visibility})

print lst

