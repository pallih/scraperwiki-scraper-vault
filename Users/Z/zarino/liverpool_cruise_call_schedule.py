import scraperwiki
import requests
import lxml.html
import dateutil.parser
import datetime
import re

def cell_value(tr, id):
    v = tr.cssselect('td')[id].text
    if v in (u'\xa0', ' ', '',):
        return None
    else:
        return v

def parse_date(string, format=None):
    if string:
        try:
            d = dateutil.parser.parse(string).date()
        except:
            return string
        else:
            if format:
                return d.strftime(format)
            else:
                return d
    else:
        return None

def parse_time(string, default=None):
    if string:
        matches = re.findall(r'(\d{1,2})[.:](\d\d)', string)
        if matches:
            return str(matches[0][0]).zfill(2) + ':' + str(matches[0][1])
        else:
            return default
    else:
        return default

# defaults to use when the schedule is incomplete
default_start_time = '08:00'
default_end_time = '18:00'

# get the schedule
r = requests.get('http://www.cruise-liverpool.com/cruise-call-schedule/')
html = r.text
dom = lxml.html.fromstring(html)
ships = []

# scrape each line of the schedule
for tr in dom.cssselect('#content tr tr'):
    if len(tr.cssselect('td')):
        if not re.search(u"\u2013", cell_value(tr,0)):
            date = parse_date(cell_value(tr,0),format='%Y-%m-%d')
            start = date + ' ' + parse_time(cell_value(tr,4),default_start_time)
            end = date + ' ' + parse_time(cell_value(tr,5),default_end_time)
        else:
            (start_date,end_date) = cell_value(tr,0).split(u" \u2013 ")
            if not re.search(r'\d{4}', start_date):
                start_date += ' ' + end_date.split(' ')[-1]
            start = start_date + ' ' + parse_time(cell_value(tr,4),default_start_time)
            end = end_date + ' ' + parse_time(cell_value(tr,5),default_end_time)

        ships.append({
            #'date': parse_date(cell_value(tr,0)),
            #'eta': parse_time(cell_value(tr,4)),
            #'etd': parse_time(cell_value(tr,5)),
            #'day': cell_value(tr,1),
            'vessel': cell_value(tr,2),
            'category': cell_value(tr,3),
            'cruise_line': cell_value(tr,6),
            'start': dateutil.parser.parse(start),
            'end': dateutil.parser.parse(end),
            'raw_date': parse_date(cell_value(tr,0))
        })

# save events - index by date and vessel name (so updates will overwrite)
scraperwiki.sqlite.save(['raw_date','vessel'], ships, 'schedule')
