import scraperwiki  
import lxml.html           
         
import urllib2
import re
  
stuff = ["AF","AL","DZ","AO","AG","AR",
"AM","AW","AU","AT","AZ","BS","BH","BD",
"BB","BY","BE","BZ","BJ","BM","BO","BQ",
"BA","BR","BN","BG","BF","BI","KH","CM",
"CA","CV","KY","TD","CL","CN","TW","CO",
"CG","CK","CR","CI","HR","CU","CW","CY",
"CZ","CD","DK","DJ","DO","EC","EG","SV",
"GQ","ER","EE","ET","FJ","FI","FR","PF",
"GA","GM","GE","DE","GH","GR","GD","GP",
"GU","GT","GN","GW","HT","HN","HK","HU",
"IS","IN","ID","IR","IQ","IE","IL","IT",
"JM","JP","JE","JO","KZ","KE","KR","KP",
"KW","KG","LA","LV","LB","LR","LY","LT",
"LU","MO","MK","MW","MY","MV","ML","MT",
"MH","MQ","MR","MU","MX","FM","MD","MN",
"ME","MA","MZ","MM","NA","NP","NL","NC",
"NZ","NI","NE","NG","NU","NF","MP","NO",
"OM","PK","PW","PA","PY","PE","PH","PL",
"PT","PR","QA","RO","RU","RW","KN","LC",
"WS","ST","SA","SN","RS","SC","SL","SG",
"SX","SK","SI","SO","ZA","SS","ES","LK",
"SD","SE","CH","SY","TJ","TZ","TH","TG",
"TO","TT","TN","TR","TM","TC","UG","UA",
"AE","GB","US","UY","UZ","VU","VE","VN",
"VI","YE","ZM","ZW"]  
  
for things in stuff:
    data = urllib2.urlopen("http://www.staralliance.com/destination_overview1.do?language=en&method=fetchAirports&country=%s" % (things)).read()
    for airports in re.findall(r'\b[A-Z]{3}\b', data):
        print "%s: %s" % (things, airports)
        scraperwiki.sqlite.save(["Airport"], data=dict(Airport=airports,Country=things))