import scraperwiki
import urllib
from BeautifulSoup import BeautifulSoup

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

# from_to = "fromdate=201010&todate=201010"
from_to_tmp = "fromdate=%s%s&todate=%s%s" # (yyyy,mm,yyyy,mm)
month_pref = lambda x: len(str(x))==2 and str(x) or '0' + str(x)
years = [2009,2010,2011]
months = range(1,13)
from_tos = [from_to_tmp % (y,month_pref(m),y,month_pref(m)) for y in years for m in months][11:-12]
print "\n".join(from_tos)

iscomp = """
def iscomp(num):
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
"""

# retrieve a page
starting_url = """http://recruiter.totaljobs.com/barometer/Results"""
div = "?"
params = "sector=%s&sectorname=%s&location=%s&%s"

for from_to in from_tos:
      print "Date: %s" % from_to[-6:]
      for i,sector in sectors:
            print "Sector: %s" % sector
            for loc in locations:
                print "Location: %s" % loc
                params_str = params % (i,urllib.quote(sector),urllib.quote(loc),from_to)
                url = starting_url + div + params_str
                try:
                    html = scraperwiki.scrape(url)
                    soup = BeautifulSoup(html)
                    posted = soup.findAll('td',{ "class" : "posted" })[0]
                    views = soup.findAll('td',{ "class" : "views" })[0]
                    applications = soup.findAll('td',{ "class" : "applications" })[0]
                    toint = lambda x: x.text and int(x.text.replace(",","")) or 0
                    #competitive = float(toint(applications)) / toint(posted)
                    #iscompetitive = iscomp(competitive)
                    missing = 0
                    record = {"date":from_to[-6:],"sector":sector,"location":loc,"posted":toint(posted), 
                              "views":toint(views), "applications":toint(applications),"missing":missing,"url":url}
                    cols = ["date","sector","location","posted","views","applications","missing","url"]
                    scraperwiki.sqlite.save(cols, record)
                except:
                    missing = 1
                    print "error",url,from_to,sector,loc
                    record = {"date":from_to[-6:],"sector":sector,"location":loc,"missing":missing,"url":url}
                    cols = ["date","sector","location","missing","url"]
                    scraperwiki.sqlite.save(cols, record)

import scraperwiki
import urllib
from BeautifulSoup import BeautifulSoup

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

# from_to = "fromdate=201010&todate=201010"
from_to_tmp = "fromdate=%s%s&todate=%s%s" # (yyyy,mm,yyyy,mm)
month_pref = lambda x: len(str(x))==2 and str(x) or '0' + str(x)
years = [2009,2010,2011]
months = range(1,13)
from_tos = [from_to_tmp % (y,month_pref(m),y,month_pref(m)) for y in years for m in months][11:-12]
print "\n".join(from_tos)

iscomp = """
def iscomp(num):
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
"""

# retrieve a page
starting_url = """http://recruiter.totaljobs.com/barometer/Results"""
div = "?"
params = "sector=%s&sectorname=%s&location=%s&%s"

for from_to in from_tos:
      print "Date: %s" % from_to[-6:]
      for i,sector in sectors:
            print "Sector: %s" % sector
            for loc in locations:
                print "Location: %s" % loc
                params_str = params % (i,urllib.quote(sector),urllib.quote(loc),from_to)
                url = starting_url + div + params_str
                try:
                    html = scraperwiki.scrape(url)
                    soup = BeautifulSoup(html)
                    posted = soup.findAll('td',{ "class" : "posted" })[0]
                    views = soup.findAll('td',{ "class" : "views" })[0]
                    applications = soup.findAll('td',{ "class" : "applications" })[0]
                    toint = lambda x: x.text and int(x.text.replace(",","")) or 0
                    #competitive = float(toint(applications)) / toint(posted)
                    #iscompetitive = iscomp(competitive)
                    missing = 0
                    record = {"date":from_to[-6:],"sector":sector,"location":loc,"posted":toint(posted), 
                              "views":toint(views), "applications":toint(applications),"missing":missing,"url":url}
                    cols = ["date","sector","location","posted","views","applications","missing","url"]
                    scraperwiki.sqlite.save(cols, record)
                except:
                    missing = 1
                    print "error",url,from_to,sector,loc
                    record = {"date":from_to[-6:],"sector":sector,"location":loc,"missing":missing,"url":url}
                    cols = ["date","sector","location","missing","url"]
                    scraperwiki.sqlite.save(cols, record)

