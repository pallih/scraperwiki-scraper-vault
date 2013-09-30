# -*- coding: utf-8 -*-
import requests
import scraperwiki
import lxml.html
from datetime import date, datetime
import dateutil
from dateutil.parser import parser
import cgi,os,sys
from dateutil.relativedelta import relativedelta
from icalendar import Calendar, Event
import pytz
import unicodedata
import urllib
from unidecode import unidecode
from json import loads

qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

def shorten(url):
    login =  'pallih'
    apiKey = 'R_4f6dfa301e932acc5fb7d2d26fcc0217'
    r = requests.get("http://api.bit.ly/v3/shorten?longUrl=%s&login=%s&apiKey=%s&format=json" % (url,login,apiKey))
    response = r.text
    j = loads(response)
    if j['status_code'] == 200:
        return j['data']['url']
    else:
        return url

if not qsenv:
    print '''
    <!DOCTYPE html>
<html>
  <head>
    <title>Leikjaskrá KSÍ í iCalendar</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <style type="text/css">
    body {
    background-color: #333;
    margin-left: 30px;
    }
    body,td,th {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 18px;
    color: #F0C;
    }
    a:link, a:visited {
    color: #FFF;
    }
    h2 {
    font-size: 22px;
    color: #FFF;
    }
        h1 {
    font-size: 28px;
    color: #FFF;
    }
 
    </style>
    </head>
    <body>
    <h1>Leikjalisti KSÍ yfir í iCalendar snið</h1>
    <h2>Í boði <a href="http://gogn.in">gogn.in</a></h2>
    Veldu það mót sem þú vilt fá á iCalendar sniði:<br /><br />

<form id="motalisti" name="motalisti" method="get" action="https://views.scraperwiki.com/run/ksi-mot2ical/" accept-charset="utf-8">
  <label for="mot">Mót:  </label><select name='mot' id='mot'><option value=''>Veldu mót</option>
'''
    html = requests.get('http://www.ksi.is/mot/motalisti/').text
    root = lxml.html.fromstring(html)
    table = root.xpath('//table[@id="mot-tafla"]/tr')
    for t in table[1:]:
        if t[2].text_content() == '':
            print '<option value="'+ (t[1][0].attrib['href'].replace('urslit-stada/?MotNumer=','')).strip() + '|'+ t[1].text_content().strip()+'">' + t[1].text_content().strip()+'</option>'
    print'''
    </select>

    <input type="submit" value="Sýna">

    </form>

    </body>
    '''
    exit()

if 'mot' in qsenv:
    
    
    print '''
    <!DOCTYPE html>
<html>
  <head>
    <title>Leikjaskrá KSÍ --> ical</title>
    <meta charset="UTF-8">
    <style type="text/css">
    body {
    background-color: #333;
    margin-left: 30px;
    }
    body,td,th {
    font-family: Arial, Helvetica, sans-serif;
    #font-size: 18px;
    color: #F0C;
    }
    a:link, a:visited {
    color: #FFF;
    }
    h2 {
    font-size: 22px;
    color: #FFF;
    }
    h1 {
    font-size: 28px;
    color: #FFF;
    }
 
    </style>
    </head>
    <body>
    <h1>Leikjalisti KSÍ yfir í iCalendar snið</h1>
    <h2>Í boði <a href="http://gogn.in">gogn.in</a></h2>
    '''
    icalurl= shorten('https://views.scraperwiki.com/run/ksi-mot2ical/?motnumer='+qsenv['mot'].encode('iso-8859-1').partition('|')[0])
    icalurl_encoded = str(urllib.quote_plus(icalurl))
    motanafn =  qsenv['mot'].encode('iso-8859-1').partition('|')[2]
    print 'Þú valdir: <h2>' + motanafn + '</h2>'
    print '<br /><br />'
    print 'Hér er slóð á iCal skrána fyrir þetta mót:<br /><br /> <a href="'+str(icalurl)+'">'+str(icalurl)+'</a>'
    print '<br /><br />'
    print 'Þú getur notað slóðina til að búa til dagatal í Google Calendar (smellir á örina við Other calendars, vinstra megin, og velur "Add by url"), í iCal forritinu á OS X (velur Calendar og svo Subscribe) eða Outlook.'
    print '<br /><br />Hér er sýnishorn: <br /><br />'
    print "<iframe id='cv_if5' src='http://cdn.instantcal.com/cvir.html?id=cv_nav6&id=cv_nav7&cname="+motanafn+"&time24=1&id=cv_nav8&gtype=cv_monthgrid&gtype=cv_daygrid&gtype=cv_listSummary&file="+icalurl_encoded+"&file="+icalurl_encoded+"&file="+icalurl_encoded+"&theme=ff00cc&theme=ff00cc&theme=ff00cc&ccolor=%23ff00cc&ccolor=%23ffffc0&ccolor=%23ffffc0&dims=1&dims=1&dims=1&gcloseable=0&gcloseable=0&gcloseable=0&gnavigable=1&gnavigable=1&gnavigable=1&gperiod=month&gperiod=day&gperiod=month&itype=cv_simpleevent&itype=cv_simpleevent&itype=cv_simpleevent' allowTransparency=true scrolling='no' frameborder=0 height=600 width=800></iframe>"
    print '<br /><br/>Ef þú vilt velja annað mót:'
    print '<br /><br />'
    print '''
    <form id="motalisti" name="motalisti" method="get" action="https://views.scraperwiki.com/run/ksi-mot2ical/" accept-charset="utf-8">
  <label for="mot">Mót:  </label><select name='mot' id='mot'><option value=''>Veldu mót</option>
'''
    html = scraperwiki.scrape('http://www.ksi.is/mot/motalisti/')
    root = lxml.html.fromstring(html)
    table = root.xpath('//table[@id="mot-tafla"]/tr')
    for t in table[1:]:
        print '<option value="'+ (t[1][0].attrib['href'].replace('urslit-stada/?MotNumer=','')).strip() + '|'+ t[1].text_content().strip()+'">' + t[1].text_content().strip()+'</option>'
    print'''
    </select>

    <input type="submit" value="Sýna">

    </form>
    </body>
    '''
    exit()

else:

    playday ="%m/%d/%Y"
    kickoff = "%l:%M %p"

    def replace_all(text, dic):
        for i, j in dic.iteritems():
            text = text.replace(i, j)
        return text

    replacements = {'mán.':'mon','þri.':'tue','mið.':'wed','fim.':'thu','fös.':'fri','lau.':'sat','sun.':'sun','jan.':'jan','feb.':'feb','mar.':'mar','apr.':'apr','maí.':'may','jún.':'jun','júl.':'jul','ágú.':'aug','sep.':'sep','okt.':'oct','nóv.':'nov','des.':'dec'}

    url = 'http://www.ksi.is/mot/motalisti/urslit-stada/?MotNumer=' + qsenv['motnumer'].strip() #26464' #konur 2012

    html = requests.get(url).text
    root = lxml.html.fromstring(html)
    table = root.xpath('//table[@id="leikir-tafla"]/tr')
    mot = root.xpath('//li[@class="mot"]/span/text()')[0].strip()
    ar = root.xpath('//li[@class="filter"]/span/text()')[0].strip()

    cal = Calendar()
    cal.add('prodid', '-// %s %s - %s //' % (mot,ar,'gogn.in'))
    cal.add('version', '2.0')
    cal.add('X-WR-CALNAME', '%s %s' % (mot,ar))
    cal.add('X-WR-TIMEZONE','Atlantic/Reykjavik')
    cal.add('X-WR-CALDESC','www.gogn.in - pallih@gogn.in')

    for t in table[1:]:
        if t[0].tag == 'th':
            continue
        datestring = replace_all(t[1].text[5:].encode('utf-8'),replacements) + ' ' + t[2].text.strip()
        correct_datestring = dateutil.parser.parse(datestring)  
        event = Event()
        try:
            event.add('summary', t[3].text + ' ' + t[5].text)
        except:
            event.add('summary', t[3].text)
        try:
            event.add('url', 'http://www.ksi.is/mot/motalisti/' + t[7][0].attrib['href'][3:])
        except:
            pass
        event.add('location', t[4].text)
        event.add('dtstart', correct_datestring)
        event.add('dtend', (correct_datestring + relativedelta( minutes = +105 )))
        event.add('dtstamp', correct_datestring)
        event['uid'] = unidecode((ar + t[3].text+mot.lower()+'-gogn.in').replace(' ','')).encode('utf-8')
        event.add('class', 'PUBLIC')
        cal.add_component(event)

    filename = 'leikdagar_'+unidecode(mot.replace(' ',''))+unidecode(ar)+'.ics'
    scraperwiki.utils.httpresponseheader("Content-Type", "text/calendar;charset=utf-8")
    scraperwiki.utils.httpresponseheader("Content-Disposition", "inline; filename="+filename)
    sys.stdout.write(cal.to_ical().decode('utf-8'))


# -*- coding: utf-8 -*-
import requests
import scraperwiki
import lxml.html
from datetime import date, datetime
import dateutil
from dateutil.parser import parser
import cgi,os,sys
from dateutil.relativedelta import relativedelta
from icalendar import Calendar, Event
import pytz
import unicodedata
import urllib
from unidecode import unidecode
from json import loads

qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

def shorten(url):
    login =  'pallih'
    apiKey = 'R_4f6dfa301e932acc5fb7d2d26fcc0217'
    r = requests.get("http://api.bit.ly/v3/shorten?longUrl=%s&login=%s&apiKey=%s&format=json" % (url,login,apiKey))
    response = r.text
    j = loads(response)
    if j['status_code'] == 200:
        return j['data']['url']
    else:
        return url

if not qsenv:
    print '''
    <!DOCTYPE html>
<html>
  <head>
    <title>Leikjaskrá KSÍ í iCalendar</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <style type="text/css">
    body {
    background-color: #333;
    margin-left: 30px;
    }
    body,td,th {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 18px;
    color: #F0C;
    }
    a:link, a:visited {
    color: #FFF;
    }
    h2 {
    font-size: 22px;
    color: #FFF;
    }
        h1 {
    font-size: 28px;
    color: #FFF;
    }
 
    </style>
    </head>
    <body>
    <h1>Leikjalisti KSÍ yfir í iCalendar snið</h1>
    <h2>Í boði <a href="http://gogn.in">gogn.in</a></h2>
    Veldu það mót sem þú vilt fá á iCalendar sniði:<br /><br />

<form id="motalisti" name="motalisti" method="get" action="https://views.scraperwiki.com/run/ksi-mot2ical/" accept-charset="utf-8">
  <label for="mot">Mót:  </label><select name='mot' id='mot'><option value=''>Veldu mót</option>
'''
    html = requests.get('http://www.ksi.is/mot/motalisti/').text
    root = lxml.html.fromstring(html)
    table = root.xpath('//table[@id="mot-tafla"]/tr')
    for t in table[1:]:
        if t[2].text_content() == '':
            print '<option value="'+ (t[1][0].attrib['href'].replace('urslit-stada/?MotNumer=','')).strip() + '|'+ t[1].text_content().strip()+'">' + t[1].text_content().strip()+'</option>'
    print'''
    </select>

    <input type="submit" value="Sýna">

    </form>

    </body>
    '''
    exit()

if 'mot' in qsenv:
    
    
    print '''
    <!DOCTYPE html>
<html>
  <head>
    <title>Leikjaskrá KSÍ --> ical</title>
    <meta charset="UTF-8">
    <style type="text/css">
    body {
    background-color: #333;
    margin-left: 30px;
    }
    body,td,th {
    font-family: Arial, Helvetica, sans-serif;
    #font-size: 18px;
    color: #F0C;
    }
    a:link, a:visited {
    color: #FFF;
    }
    h2 {
    font-size: 22px;
    color: #FFF;
    }
    h1 {
    font-size: 28px;
    color: #FFF;
    }
 
    </style>
    </head>
    <body>
    <h1>Leikjalisti KSÍ yfir í iCalendar snið</h1>
    <h2>Í boði <a href="http://gogn.in">gogn.in</a></h2>
    '''
    icalurl= shorten('https://views.scraperwiki.com/run/ksi-mot2ical/?motnumer='+qsenv['mot'].encode('iso-8859-1').partition('|')[0])
    icalurl_encoded = str(urllib.quote_plus(icalurl))
    motanafn =  qsenv['mot'].encode('iso-8859-1').partition('|')[2]
    print 'Þú valdir: <h2>' + motanafn + '</h2>'
    print '<br /><br />'
    print 'Hér er slóð á iCal skrána fyrir þetta mót:<br /><br /> <a href="'+str(icalurl)+'">'+str(icalurl)+'</a>'
    print '<br /><br />'
    print 'Þú getur notað slóðina til að búa til dagatal í Google Calendar (smellir á örina við Other calendars, vinstra megin, og velur "Add by url"), í iCal forritinu á OS X (velur Calendar og svo Subscribe) eða Outlook.'
    print '<br /><br />Hér er sýnishorn: <br /><br />'
    print "<iframe id='cv_if5' src='http://cdn.instantcal.com/cvir.html?id=cv_nav6&id=cv_nav7&cname="+motanafn+"&time24=1&id=cv_nav8&gtype=cv_monthgrid&gtype=cv_daygrid&gtype=cv_listSummary&file="+icalurl_encoded+"&file="+icalurl_encoded+"&file="+icalurl_encoded+"&theme=ff00cc&theme=ff00cc&theme=ff00cc&ccolor=%23ff00cc&ccolor=%23ffffc0&ccolor=%23ffffc0&dims=1&dims=1&dims=1&gcloseable=0&gcloseable=0&gcloseable=0&gnavigable=1&gnavigable=1&gnavigable=1&gperiod=month&gperiod=day&gperiod=month&itype=cv_simpleevent&itype=cv_simpleevent&itype=cv_simpleevent' allowTransparency=true scrolling='no' frameborder=0 height=600 width=800></iframe>"
    print '<br /><br/>Ef þú vilt velja annað mót:'
    print '<br /><br />'
    print '''
    <form id="motalisti" name="motalisti" method="get" action="https://views.scraperwiki.com/run/ksi-mot2ical/" accept-charset="utf-8">
  <label for="mot">Mót:  </label><select name='mot' id='mot'><option value=''>Veldu mót</option>
'''
    html = scraperwiki.scrape('http://www.ksi.is/mot/motalisti/')
    root = lxml.html.fromstring(html)
    table = root.xpath('//table[@id="mot-tafla"]/tr')
    for t in table[1:]:
        print '<option value="'+ (t[1][0].attrib['href'].replace('urslit-stada/?MotNumer=','')).strip() + '|'+ t[1].text_content().strip()+'">' + t[1].text_content().strip()+'</option>'
    print'''
    </select>

    <input type="submit" value="Sýna">

    </form>
    </body>
    '''
    exit()

else:

    playday ="%m/%d/%Y"
    kickoff = "%l:%M %p"

    def replace_all(text, dic):
        for i, j in dic.iteritems():
            text = text.replace(i, j)
        return text

    replacements = {'mán.':'mon','þri.':'tue','mið.':'wed','fim.':'thu','fös.':'fri','lau.':'sat','sun.':'sun','jan.':'jan','feb.':'feb','mar.':'mar','apr.':'apr','maí.':'may','jún.':'jun','júl.':'jul','ágú.':'aug','sep.':'sep','okt.':'oct','nóv.':'nov','des.':'dec'}

    url = 'http://www.ksi.is/mot/motalisti/urslit-stada/?MotNumer=' + qsenv['motnumer'].strip() #26464' #konur 2012

    html = requests.get(url).text
    root = lxml.html.fromstring(html)
    table = root.xpath('//table[@id="leikir-tafla"]/tr')
    mot = root.xpath('//li[@class="mot"]/span/text()')[0].strip()
    ar = root.xpath('//li[@class="filter"]/span/text()')[0].strip()

    cal = Calendar()
    cal.add('prodid', '-// %s %s - %s //' % (mot,ar,'gogn.in'))
    cal.add('version', '2.0')
    cal.add('X-WR-CALNAME', '%s %s' % (mot,ar))
    cal.add('X-WR-TIMEZONE','Atlantic/Reykjavik')
    cal.add('X-WR-CALDESC','www.gogn.in - pallih@gogn.in')

    for t in table[1:]:
        if t[0].tag == 'th':
            continue
        datestring = replace_all(t[1].text[5:].encode('utf-8'),replacements) + ' ' + t[2].text.strip()
        correct_datestring = dateutil.parser.parse(datestring)  
        event = Event()
        try:
            event.add('summary', t[3].text + ' ' + t[5].text)
        except:
            event.add('summary', t[3].text)
        try:
            event.add('url', 'http://www.ksi.is/mot/motalisti/' + t[7][0].attrib['href'][3:])
        except:
            pass
        event.add('location', t[4].text)
        event.add('dtstart', correct_datestring)
        event.add('dtend', (correct_datestring + relativedelta( minutes = +105 )))
        event.add('dtstamp', correct_datestring)
        event['uid'] = unidecode((ar + t[3].text+mot.lower()+'-gogn.in').replace(' ','')).encode('utf-8')
        event.add('class', 'PUBLIC')
        cal.add_component(event)

    filename = 'leikdagar_'+unidecode(mot.replace(' ',''))+unidecode(ar)+'.ics'
    scraperwiki.utils.httpresponseheader("Content-Type", "text/calendar;charset=utf-8")
    scraperwiki.utils.httpresponseheader("Content-Disposition", "inline; filename="+filename)
    sys.stdout.write(cal.to_ical().decode('utf-8'))


