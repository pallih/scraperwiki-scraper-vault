import scraperwiki
import lxml.html
import numpy           

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
                byState[state]=[]
            byState[state].append(int(cloudy_days))
            #data = {
            #    'city_state' : city_state,
            #    'state' : state,
            #    'cloudy_days' : int(cloudy_days)
            #}
            #print data

for state in byState.keys():
    #print state, numpy.average(byState[state]),byState[state] 
    byState[state] = round(numpy.average(byState[state]))
    data = {'state' : state, 'cloudy_days':byState[state]}
    scraperwiki.sqlite.save(unique_keys=['state'], data=data)import scraperwiki
import lxml.html
import numpy           

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
                byState[state]=[]
            byState[state].append(int(cloudy_days))
            #data = {
            #    'city_state' : city_state,
            #    'state' : state,
            #    'cloudy_days' : int(cloudy_days)
            #}
            #print data

for state in byState.keys():
    #print state, numpy.average(byState[state]),byState[state] 
    byState[state] = round(numpy.average(byState[state]))
    data = {'state' : state, 'cloudy_days':byState[state]}
    scraperwiki.sqlite.save(unique_keys=['state'], data=data)