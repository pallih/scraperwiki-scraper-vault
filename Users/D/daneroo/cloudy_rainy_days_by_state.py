import scraperwiki
import lxml.html
import numpy 
import math         

html = scraperwiki.scrape("http://www.weathertoday.net/weatherfacts/cloudy.php")
#print html
root = lxml.html.fromstring(html)
byState={}
for tr in root.cssselect("div[align='center'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==2:
        cloudy_days = tds[1].text_content()
        city_state = tds[0].text_content()
        split = city_state.split(',')
        state='None'
        if len(split)>1:
            state = split[-1]
        state=state.strip(' ,.').replace('.','') # leading,traling, and acronym-dot
        if cloudy_days.isdigit():
            if not state in byState:
                byState[state]={'rainy':[],'cloudy':[]}
            byState[state]['cloudy'].append(int(cloudy_days))


html = scraperwiki.scrape("http://www.weathertoday.net/weatherfacts/precip_01.php")
#print html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='center'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==2:
        rainy_days = tds[1].text_content()
        city_state = tds[0].text_content()
        split = city_state.split(',')
        state='None'
        if len(split)>1:
            state = split[-1]
        state=state.strip(' ,.').replace('.','') # leading,traling, and acronym-dot
        if rainy_days.isdigit():
            if not state in byState:
                byState[state]={'rainy':[],'cloudy':[]}
            byState[state]['rainy'].append(int(rainy_days))

for state in byState.keys():
    #print 'rainy',state, numpy.average(byState[state]['rainy']),byState[state]['rainy'] 
    #print 'cloudy',state, numpy.average(byState[state]['cloudy']),byState[state]['cloudy']
    byState[state]['rainy'] = round(numpy.average(byState[state]['rainy']))
    byState[state]['cloudy'] = round(numpy.average(byState[state]['cloudy']))
    data = {'state' : state, 'cloudy_days':byState[state]['cloudy'], 'rainy_days':byState[state]['rainy']}
    if not math.isnan(byState[state]['cloudy']) and not math.isnan(byState[state]['rainy']):
        scraperwiki.sqlite.save(unique_keys=['state'], data=data)