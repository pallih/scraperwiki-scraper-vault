import copy
import datetime
import dateutil.parser
import re

import lxml.html 
import mechanize
import scraperwiki

url = "http://www.cps.edu/Calendar/Student_days_off/Pages/StudentDaysOff.aspx"
# Selector for page title
title_sel = "td.h1"
# Selector for table containing date data
outer_table_sel = "#ctl00_ctl12_g_3ad6631c_67ce_4250_a1ce_e834c158b0b3_ctl00_tblHolidays"
date_row_sel = "%s table tr" % (outer_table_sel)

def parse_schoolyear(title):
    year_re = r'\d{4}'
    return [int(year_str) for year_str in re.findall(year_re, title)]

def parse_date(datestring, years):
    date = dateutil.parser.parse(datestring).date()
    if date.month >= 8 and date.month <= 12:
        date = date.replace(year=years[0])
    else:
        date = date.replace(year=years[1])

    return date
    
def parse_dates(date_text, years):
    dates = []
    parts = [s.strip() for s in re.split(r'-', date_text)]
    start = parse_date(parts[0], years)
    dates.append(start)
    try:
        end = parse_date(parts[1], years)
        current = copy.copy(start)
        while current < end:
            day = datetime.timedelta(days=1)
            current = current + day
            dates.append(current)            
    except IndexError:
        pass
    
    return dates

def parse_desc(text):
    parts = [s.strip() for s in re.split(r'[;:]', text)]
    for part in parts:
        if 'track' in part.lower():
            track = part
            continue
        if part.lower() == 'no classes':
            continue
        reason = part
    return (track, reason)

browser = mechanize.Browser()
r = browser.open(url)
html = r.read()
root = lxml.html.fromstring(html)

title = root.cssselect("td.h1")[0].text_content()
years = parse_schoolyear(title)

for tr in root.cssselect(date_row_sel):
    date_col = tr.cssselect("td:first-child")
    desc_col = tr.cssselect("td:first-child + td")
    if len(date_col) and len(desc_col):
        date_text = date_col[0].text_content()
        desc_text = desc_col[0].text_content()
        dates = parse_dates(date_text, years)
        (track, reason) = parse_desc(desc_text)
        for date in dates:
            data = {
                'date': date.isoformat(),
                'track': track,
                'description': reason,
            }
            scraperwiki.sqlite.save(unique_keys=[], data=data)
