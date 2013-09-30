#########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import os
import urlparse

def competitive(x,y):
    return float(str(x)) / float(str(y))

def iscompetitive(num):
  if num > 24:
    return 0.9
  elif num > 18:
    return 0.7
  elif num > 12:
    return 0.5
  elif num > 6:
    return 0.3
  elif num < 6:
    return 0.1
  else:
    return 0.0

sectors = [(18, "Accountancy"),
           (6, "Aerospace"),
           (26, "Agriculture, Fishing, Forestry"),
           (27, "Banking, Insurance, Finance"),
           (3, "Catering & Hospitality"),
           (4, "Construction"),
           (28, "Customer Services"),
           (29, "Education"),
           (7, "Electronics"),
           (15, "Engineering, Manufacturing, Utilities"),
           (22, "Graduate, Trainees"),
           (30, "Health, Nursing"),
           (5, "Human Resources"),
           (1, "IT & Internet"),
           (24, "Legal"),
           (31, "Management Consultancy"),
           (21, "Marketing, Advertising, PR"),
           (32, "Media, New Media, Creative"),
           (42, "Not For Profit, Charities"),
           (88, "Oil, Gas, Alternative Energy"),
           (9, "Property"),
           (33, "Public Sector & Services"),
           (48, "Recruitment Sales"),
           (11, "Retail, Wholesale"),
           (20, "Sales"),
           (10, "Science"),
           (34, "Secretarial, PAs, Administration"),
           (35, "Senior Appointments"),
           (12, "Social Services"),
           (36, "Telecommunications"),
           (25, "Transport, Logistics"),
           (17, "Travel, Leisure, Tourism")]

locations = ["East Anglia","East Midlands","London","North East","North West","Northern Ireland","Scotland",
"South East","South West","Wales","West Midlands","Yorkshire"]

date = "201012"

sourcescraper = "is_it_worth_it"

limit = -1
offset = 0

keys = getKeys(sourcescraper)
keys.sort()  # alphabetically

# print '<h2><b>%s</b>  (%d columns)</h2>' % (sourcescraper, len(keys))

print """<h2>Is it worth it?</h2>"""
print '<table border="1" style="border-collapse:collapse;">'

our_keys = ["date","posted","applications","location","sector"]



option_tmp = r"""<option value="%s">%s</option>"""

start_form = """<form action="http://scraperwikiviews.com/run/show_is_it_worth_it/?">"""
end_form = """<button type="submit">GO!</button></form>"""

locations_tmp = r"""<form action="http://scraperwikiviews.com/run/show_is_it_worth_it/?">
<select name="locations">
%s
</select>"""

sectors_tmp = r"""<select name="sectors">
%s
</select>"""

options1 = [option_tmp % (x,x) for x in locations]
locations_form = locations_tmp % " ".join(options1)

options2 = [option_tmp % (x,x) for y,x in sectors]
sectors_form = sectors_tmp % " ".join(options2)

print start_form
print locations_form
print sectors_form
print end_form

url = os.getenv("URLQUERY")

params = dict(urlparse.parse_qsl(url))

# print params

our_region = params['locations'] # "London"
our_sector = params['sectors'] # "Accountancy"

torep = r"%20"

if torep in our_region:
  show_our_region = our_region.replace(r"%20"," ")
else: show_our_region = our_region
if torep in our_sector:
  show_our_sector = our_sector.replace(r"%20"," ")
else: show_our_sector = our_sector

print r"<h3>Your regions: %s<br>Your sector: %s<br>Date:%s</h3>" % (our_region,our_sector,date)

chart1 = r"""http://chart.apis.google.com/chart?cht=lc&chs=400x120&chbh=14,0,0&chd=t:100|0,100&chds=0,100,0,100&chco=00000000&chma=10,10,28,21&chxt=x,x&chxs=0,000000,0,0,t&chf=c,lg,0,00d10f,0,4ed000,0.1,c8d500,0.2,f07f00,0.567,d03000,0.75,ad0000,1&chxs=0,,11,0,t,000000|1,,11,0,t,000000"""

chart2 = r"""&chxl=0:|Not|Slightly|Normally|Very|Extremely|1:|competitive|competitive|competitive|competitive|competitive&chxp=0,8,30,50,70,90|1,8,30,50,70,90&chm=V,FFFFFF,1,0.2,2|V,FFFFFF,1,0.4,2|V,FFFFFF,1,0.6,2|V,FFFFFF,1,0.8,2|@f%s,777777,1,%s:.8,12,1&chma=0,80,50"""

# column headings
print "<tr>",
for key in our_keys: #keys:
    print "<th>%s</th>" % key,
print "</tr>"

# rows
for row in getData(sourcescraper, limit, offset):
    data = [row.get(key) for key in our_keys] #keys:
    comp = competitive(data[0],data[1])
    iscomp = iscompetitive(comp)
    data = data + [comp,iscomp]
    if our_region in data and our_sector in data and date in data:
        print "<tr>",
        cell = "<td>%s</td>"
        output = [cell % d for d in data]
        print " ".join(output)
        #print "<td>%s</td>" % row.get(key),
        print "</tr>"
        break
    
print "</table>"

mes = {"0.1":"Walk+in+the+park!","0.3":"Remember+your+name","0.5":"Fifty+fifty+mate","0.7":"Slim+chance","0.9":"Fat+chance!"}


chart_str = chart1 + (chart2 % (mes[data[-1]],data[-1]))
print "<p>"
print """<img src="%s"/>""" % chart_str
print "</p>"




#########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import os
import urlparse

def competitive(x,y):
    return float(str(x)) / float(str(y))

def iscompetitive(num):
  if num > 24:
    return 0.9
  elif num > 18:
    return 0.7
  elif num > 12:
    return 0.5
  elif num > 6:
    return 0.3
  elif num < 6:
    return 0.1
  else:
    return 0.0

sectors = [(18, "Accountancy"),
           (6, "Aerospace"),
           (26, "Agriculture, Fishing, Forestry"),
           (27, "Banking, Insurance, Finance"),
           (3, "Catering & Hospitality"),
           (4, "Construction"),
           (28, "Customer Services"),
           (29, "Education"),
           (7, "Electronics"),
           (15, "Engineering, Manufacturing, Utilities"),
           (22, "Graduate, Trainees"),
           (30, "Health, Nursing"),
           (5, "Human Resources"),
           (1, "IT & Internet"),
           (24, "Legal"),
           (31, "Management Consultancy"),
           (21, "Marketing, Advertising, PR"),
           (32, "Media, New Media, Creative"),
           (42, "Not For Profit, Charities"),
           (88, "Oil, Gas, Alternative Energy"),
           (9, "Property"),
           (33, "Public Sector & Services"),
           (48, "Recruitment Sales"),
           (11, "Retail, Wholesale"),
           (20, "Sales"),
           (10, "Science"),
           (34, "Secretarial, PAs, Administration"),
           (35, "Senior Appointments"),
           (12, "Social Services"),
           (36, "Telecommunications"),
           (25, "Transport, Logistics"),
           (17, "Travel, Leisure, Tourism")]

locations = ["East Anglia","East Midlands","London","North East","North West","Northern Ireland","Scotland",
"South East","South West","Wales","West Midlands","Yorkshire"]

date = "201012"

sourcescraper = "is_it_worth_it"

limit = -1
offset = 0

keys = getKeys(sourcescraper)
keys.sort()  # alphabetically

# print '<h2><b>%s</b>  (%d columns)</h2>' % (sourcescraper, len(keys))

print """<h2>Is it worth it?</h2>"""
print '<table border="1" style="border-collapse:collapse;">'

our_keys = ["date","posted","applications","location","sector"]



option_tmp = r"""<option value="%s">%s</option>"""

start_form = """<form action="http://scraperwikiviews.com/run/show_is_it_worth_it/?">"""
end_form = """<button type="submit">GO!</button></form>"""

locations_tmp = r"""<form action="http://scraperwikiviews.com/run/show_is_it_worth_it/?">
<select name="locations">
%s
</select>"""

sectors_tmp = r"""<select name="sectors">
%s
</select>"""

options1 = [option_tmp % (x,x) for x in locations]
locations_form = locations_tmp % " ".join(options1)

options2 = [option_tmp % (x,x) for y,x in sectors]
sectors_form = sectors_tmp % " ".join(options2)

print start_form
print locations_form
print sectors_form
print end_form

url = os.getenv("URLQUERY")

params = dict(urlparse.parse_qsl(url))

# print params

our_region = params['locations'] # "London"
our_sector = params['sectors'] # "Accountancy"

torep = r"%20"

if torep in our_region:
  show_our_region = our_region.replace(r"%20"," ")
else: show_our_region = our_region
if torep in our_sector:
  show_our_sector = our_sector.replace(r"%20"," ")
else: show_our_sector = our_sector

print r"<h3>Your regions: %s<br>Your sector: %s<br>Date:%s</h3>" % (our_region,our_sector,date)

chart1 = r"""http://chart.apis.google.com/chart?cht=lc&chs=400x120&chbh=14,0,0&chd=t:100|0,100&chds=0,100,0,100&chco=00000000&chma=10,10,28,21&chxt=x,x&chxs=0,000000,0,0,t&chf=c,lg,0,00d10f,0,4ed000,0.1,c8d500,0.2,f07f00,0.567,d03000,0.75,ad0000,1&chxs=0,,11,0,t,000000|1,,11,0,t,000000"""

chart2 = r"""&chxl=0:|Not|Slightly|Normally|Very|Extremely|1:|competitive|competitive|competitive|competitive|competitive&chxp=0,8,30,50,70,90|1,8,30,50,70,90&chm=V,FFFFFF,1,0.2,2|V,FFFFFF,1,0.4,2|V,FFFFFF,1,0.6,2|V,FFFFFF,1,0.8,2|@f%s,777777,1,%s:.8,12,1&chma=0,80,50"""

# column headings
print "<tr>",
for key in our_keys: #keys:
    print "<th>%s</th>" % key,
print "</tr>"

# rows
for row in getData(sourcescraper, limit, offset):
    data = [row.get(key) for key in our_keys] #keys:
    comp = competitive(data[0],data[1])
    iscomp = iscompetitive(comp)
    data = data + [comp,iscomp]
    if our_region in data and our_sector in data and date in data:
        print "<tr>",
        cell = "<td>%s</td>"
        output = [cell % d for d in data]
        print " ".join(output)
        #print "<td>%s</td>" % row.get(key),
        print "</tr>"
        break
    
print "</table>"

mes = {"0.1":"Walk+in+the+park!","0.3":"Remember+your+name","0.5":"Fifty+fifty+mate","0.7":"Slim+chance","0.9":"Fat+chance!"}


chart_str = chart1 + (chart2 % (mes[data[-1]],data[-1]))
print "<p>"
print """<img src="%s"/>""" % chart_str
print "</p>"




