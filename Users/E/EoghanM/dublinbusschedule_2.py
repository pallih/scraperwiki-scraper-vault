# -*- coding: utf-8 -*-
# Fetch Dublin Bus schedule information from dublinbus.ie
#
# Code is placed under MIT/X11 licence
# (c) 2010-2012 Jean-Paul Bonnet, Jérémie Laval and Eoghan Murray
import re
import urllib2
import sys
from BeautifulSoup import BeautifulSoup
from itertools import combinations
try:
    import scraperwiki
except ImportError:
    scraperwiki = None

baseUrl = "http://www.dublinbus.ie/en/Your-Journey1/Timetables/All-Timetables/"

# columns used 
# busNumber(string) from(string) stops(string, CSV{latitute|longitude}) to(string) mondayFriday(string,CSV{\d\d:\d\d}) saturday(string,CSV{\d\d:\d\d}) sunday(string,CSV{\d\d:\d\d}) isAirport(bool) isAccessible(bool)

def Main():
    for line_number, line_url_part in get_all_routes():
        url = baseUrl + line_url_part + '/'
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        route_finder = {'class':'timetables_title'}
        for route_desc_node in soup.findAll(attrs=route_finder):
            res = {'busNumber': line_number}
            route_container = route_desc_node
            while route_container.parent and len(route_container.parent.findAll(attrs=route_finder)) == 1:
                route_container = route_container.parent
            # gather all next nodes into the same container
            while route_container.nextSibling and (route_container.nextSibling.string or 
                                                     not route_container.nextSibling.find(attrs=route_finder)):
                route_container.insert(len(route_container), route_container.nextSibling)

            route_desc = re.sub('\s+', ' ', get_text(route_desc_node).replace('&nbsp;', ' ')).strip().replace('From ', '')
            from_point, to_point = [e.strip() for e in re.split(re.compile('\s(?:towards|to)\s', re.I), route_desc, 2)]            

            icons = route_container.find("div", attrs={'class': 'timtable_icon'})
            is_airport = icons.find("img", src=re.compile("Airport_Icon.png$|Airlink_Web_Logo.png$")) != None
            is_accessible = icons.find("img", src=re.compile("Accessible_Icon.png$")) != None
            res.update({'from': from_point,
                        'to': to_point,
                        'isAirport': is_airport,
                        'isAccessible': is_accessible })

            # # how to find the entire table
            # mon_to_fri = route_desc_node.findNext(text='Monday to Friday')
            # days_table = mon_to_fri.parent
            # while days_table and not days_table.find(text='Saturday'):
            #     days_table = days_table.parent
            # assert days_table.find(text='Sunday')
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_combos = dict((a.lower()+b, re.compile('%s\s?(?:to|-)\s?%s' % (a, b), re.I)) for a, b in combinations(days, 2))

            # limit what we look for to what is on the page (this is because the absence of 'some_other_period' below will be significant)
            periods = [p for p in day_combos.keys() + days if route_container.find(text=day_combos.get(p, p))]
            for period, some_other_period in combinations(periods, 2):
                period_container = route_container.find(text=day_combos.get(period, period))
                while period_container.parent and not period_container.parent.find(text=day_combos.get(some_other_period, some_other_period)):
                    period_container = period_container.parent
                if not scraperwiki or period in ['mondayFriday', 'saturday', 'sunday']:
                    res[period] = ','.join([time.string.strip() for time in period_container.findAll("div", attrs={'class': 'time'})])

            route_overview = route_desc_node.findNext('div', attrs={'class': 'route_overview'})
            if route_overview:
                journey_time = 0
                for val in route_overview.findAll('span'):
                    mins = re.compile(">> (\d+)mins").search(val.string)
                    if mins:
                        journey_time += int(mins.group(1))
                if journey_time > 0:
                    res['journeyTime'] = journey_time

            view_on_map_node = route_desc_node.find(attrs={'class': 'view_on_map'})

            route_number = None
            if view_on_map_node and view_on_map_node.a:
                match_4 = re.compile("'(.+?)','(.+?)','(.+?)','(.+?)'").search(view_on_map_node.a['onclick'])
                match_3 = re.compile("'(.+?)','(.+?)','(.+?)'").search(view_on_map_node.a['onclick'])
                if match_4:
                    route_number, direction, towards, from_ = match_4.groups()
                elif match_3:
                    route_number, direction, towards = match_3.groups()

            if route_number:
                route_number = route_number.strip()
                # 'towards' isn't critical and we're not sending the exact same strings as the popup is

                # popup_url = http://www.dublinbus.ie/en/Examples/Google-Map/?routeNumber={0}&direction={1}&towards={2}&from={3}
                stops_url = "http://www.dublinbus.ie/Labs.EPiServer/GoogleMap/gmap_conf.aspx?custompageid=1219&routeNumber={0}&direction={1}&towards={2}"
                # Not sure why but need to translate 'direction=IO' to 'direction=I', and same for 'OI'
                maps_url = stops_url.format(route_number, direction[:1], towards)
                xml = None
                try:
                    xml = urllib2.urlopen(maps_url)
                except urllib2.HTTPError:
                    print "Couldn't get %s" % maps_url
                    # Try reverse (not sure how the mapping from 2 letter direction to 1 letter happens in the popup):
                    maps_url = stops_url.format(route_number, direction[1:], towards)
                    try:
                        xml = urllib2.urlopen(maps_url)
                    except urllib2.HTTPError:
                        pass
                    else:
                        print "Got reverse %s" % maps_url
                if xml:
                    print "Got", maps_url
                    map_soup = BeautifulSoup(xml)
                    pois = map_soup.findAll('poi')
                    res['stops'] = ','.join([poi.gpoint.lat.string + '|' + poi.gpoint.lng.string for poi in pois])
            if scraperwiki:
                for period in ['mondayFriday', 'saturday', 'sunday']:
                    if not period in res:
                        res[period] = ''
                scraperwiki.sqlite.save(['busNumber', 'from', 'to'], res)
            else:
                print res


def get_all_routes():
    lines = []
    i = 0
    while(True):
        i = i + 1
        try:
            lines += get_routes(i)  
        except:
            break
    return lines

def get_text(elem):
    if elem.string:
        return unicode(elem.string)
    text = ""
    for e in elem:
        text += get_text(e)
        if hasattr(e, 'tail') and e.tail:
            text += e.tail
    return text

def get_routes(page):
    routes = []
    routes_url = "http://www.dublinbus.ie/en/Your-Journey1/Timetables/?searchtype=&searchquery=&filter=&currentIndex=" + str(page)
    html = urllib2.urlopen(routes_url)
    soup = BeautifulSoup(html)
    pattern = re.compile(".+/(.+)/$")
    
    tds = soup.findAll("td", {"class": "RouteNumberColumn"})
    for td in tds:
        a = td.find(True)
        routes.append((a.contents[0].strip().replace('/', ''), pattern.search(a['href']).group(1)))
    return routes
    
Main()
# -*- coding: utf-8 -*-
# Fetch Dublin Bus schedule information from dublinbus.ie
#
# Code is placed under MIT/X11 licence
# (c) 2010-2012 Jean-Paul Bonnet, Jérémie Laval and Eoghan Murray
import re
import urllib2
import sys
from BeautifulSoup import BeautifulSoup
from itertools import combinations
try:
    import scraperwiki
except ImportError:
    scraperwiki = None

baseUrl = "http://www.dublinbus.ie/en/Your-Journey1/Timetables/All-Timetables/"

# columns used 
# busNumber(string) from(string) stops(string, CSV{latitute|longitude}) to(string) mondayFriday(string,CSV{\d\d:\d\d}) saturday(string,CSV{\d\d:\d\d}) sunday(string,CSV{\d\d:\d\d}) isAirport(bool) isAccessible(bool)

def Main():
    for line_number, line_url_part in get_all_routes():
        url = baseUrl + line_url_part + '/'
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        route_finder = {'class':'timetables_title'}
        for route_desc_node in soup.findAll(attrs=route_finder):
            res = {'busNumber': line_number}
            route_container = route_desc_node
            while route_container.parent and len(route_container.parent.findAll(attrs=route_finder)) == 1:
                route_container = route_container.parent
            # gather all next nodes into the same container
            while route_container.nextSibling and (route_container.nextSibling.string or 
                                                     not route_container.nextSibling.find(attrs=route_finder)):
                route_container.insert(len(route_container), route_container.nextSibling)

            route_desc = re.sub('\s+', ' ', get_text(route_desc_node).replace('&nbsp;', ' ')).strip().replace('From ', '')
            from_point, to_point = [e.strip() for e in re.split(re.compile('\s(?:towards|to)\s', re.I), route_desc, 2)]            

            icons = route_container.find("div", attrs={'class': 'timtable_icon'})
            is_airport = icons.find("img", src=re.compile("Airport_Icon.png$|Airlink_Web_Logo.png$")) != None
            is_accessible = icons.find("img", src=re.compile("Accessible_Icon.png$")) != None
            res.update({'from': from_point,
                        'to': to_point,
                        'isAirport': is_airport,
                        'isAccessible': is_accessible })

            # # how to find the entire table
            # mon_to_fri = route_desc_node.findNext(text='Monday to Friday')
            # days_table = mon_to_fri.parent
            # while days_table and not days_table.find(text='Saturday'):
            #     days_table = days_table.parent
            # assert days_table.find(text='Sunday')
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_combos = dict((a.lower()+b, re.compile('%s\s?(?:to|-)\s?%s' % (a, b), re.I)) for a, b in combinations(days, 2))

            # limit what we look for to what is on the page (this is because the absence of 'some_other_period' below will be significant)
            periods = [p for p in day_combos.keys() + days if route_container.find(text=day_combos.get(p, p))]
            for period, some_other_period in combinations(periods, 2):
                period_container = route_container.find(text=day_combos.get(period, period))
                while period_container.parent and not period_container.parent.find(text=day_combos.get(some_other_period, some_other_period)):
                    period_container = period_container.parent
                if not scraperwiki or period in ['mondayFriday', 'saturday', 'sunday']:
                    res[period] = ','.join([time.string.strip() for time in period_container.findAll("div", attrs={'class': 'time'})])

            route_overview = route_desc_node.findNext('div', attrs={'class': 'route_overview'})
            if route_overview:
                journey_time = 0
                for val in route_overview.findAll('span'):
                    mins = re.compile(">> (\d+)mins").search(val.string)
                    if mins:
                        journey_time += int(mins.group(1))
                if journey_time > 0:
                    res['journeyTime'] = journey_time

            view_on_map_node = route_desc_node.find(attrs={'class': 'view_on_map'})

            route_number = None
            if view_on_map_node and view_on_map_node.a:
                match_4 = re.compile("'(.+?)','(.+?)','(.+?)','(.+?)'").search(view_on_map_node.a['onclick'])
                match_3 = re.compile("'(.+?)','(.+?)','(.+?)'").search(view_on_map_node.a['onclick'])
                if match_4:
                    route_number, direction, towards, from_ = match_4.groups()
                elif match_3:
                    route_number, direction, towards = match_3.groups()

            if route_number:
                route_number = route_number.strip()
                # 'towards' isn't critical and we're not sending the exact same strings as the popup is

                # popup_url = http://www.dublinbus.ie/en/Examples/Google-Map/?routeNumber={0}&direction={1}&towards={2}&from={3}
                stops_url = "http://www.dublinbus.ie/Labs.EPiServer/GoogleMap/gmap_conf.aspx?custompageid=1219&routeNumber={0}&direction={1}&towards={2}"
                # Not sure why but need to translate 'direction=IO' to 'direction=I', and same for 'OI'
                maps_url = stops_url.format(route_number, direction[:1], towards)
                xml = None
                try:
                    xml = urllib2.urlopen(maps_url)
                except urllib2.HTTPError:
                    print "Couldn't get %s" % maps_url
                    # Try reverse (not sure how the mapping from 2 letter direction to 1 letter happens in the popup):
                    maps_url = stops_url.format(route_number, direction[1:], towards)
                    try:
                        xml = urllib2.urlopen(maps_url)
                    except urllib2.HTTPError:
                        pass
                    else:
                        print "Got reverse %s" % maps_url
                if xml:
                    print "Got", maps_url
                    map_soup = BeautifulSoup(xml)
                    pois = map_soup.findAll('poi')
                    res['stops'] = ','.join([poi.gpoint.lat.string + '|' + poi.gpoint.lng.string for poi in pois])
            if scraperwiki:
                for period in ['mondayFriday', 'saturday', 'sunday']:
                    if not period in res:
                        res[period] = ''
                scraperwiki.sqlite.save(['busNumber', 'from', 'to'], res)
            else:
                print res


def get_all_routes():
    lines = []
    i = 0
    while(True):
        i = i + 1
        try:
            lines += get_routes(i)  
        except:
            break
    return lines

def get_text(elem):
    if elem.string:
        return unicode(elem.string)
    text = ""
    for e in elem:
        text += get_text(e)
        if hasattr(e, 'tail') and e.tail:
            text += e.tail
    return text

def get_routes(page):
    routes = []
    routes_url = "http://www.dublinbus.ie/en/Your-Journey1/Timetables/?searchtype=&searchquery=&filter=&currentIndex=" + str(page)
    html = urllib2.urlopen(routes_url)
    soup = BeautifulSoup(html)
    pattern = re.compile(".+/(.+)/$")
    
    tds = soup.findAll("td", {"class": "RouteNumberColumn"})
    for td in tds:
        a = td.find(True)
        routes.append((a.contents[0].strip().replace('/', ''), pattern.search(a['href']).group(1)))
    return routes
    
Main()
