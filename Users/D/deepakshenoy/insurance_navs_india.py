import scraperwiki
import mechanize
import cookielib

import urllib
import urllib2
import csv
import re
from BeautifulSoup import BeautifulSoup
import time
import datetime
from datetime import date, timedelta
import math
import random
import sys
import string
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

#scraperwiki.sqlite.execute("delete from swdata")
#scraperwiki.sqlite.commit()

#####################################################
## Mechanize Presets ##
#####################################################

br = mechanize.Browser()

###Cookie Jar###
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

###Browser options###
br.set_handle_equiv(True)
#br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

##Follows refresh 0 but not hangs on refresh > 0##
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

###Mechanize Debugging###
#~ br.set_debug_http(True)
#~ br.set_debug_redirects(True)
#~ br.set_debug_responses(True)

###User-Agent###
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

###################################################

base_url = "http://www.lifeinscouncil.org/logins/index.php"

#Write loops for query parameters

begin_date= datetime.date(2012, 12,8); #strptime("08/12/2012", "%d/%m/%Y")  + relativedelta(days=0); #(date.today() + relativedelta(months=-7));

end_date = date.today() ; # + relativedelta(days=+10);
print end_date

houses = [85];

for housenum in houses:
    while begin_date<=end_date: 
                
        #needed to set a bunch of form field values to list objects. For some reason...
        pars = { "submit" : "Go",
            "product" : housenum,
            "from_date": begin_date.strftime('%Y-%m-%d')
            }
        print pars;

        response = br.open(base_url, urllib.urlencode(pars))
        response_read=response.read()
        soup=BeautifulSoup(response_read)
        
        tables = soup.findAll('table', {'cellspacing':'1'})
                        
        for table in tables:
            trs=table.findAll('tr')
            if trs.count<=1: 
                continue;
            count=0;
            for tr in trs:
                if count==0:
                    count=1;
                    continue;
                tds=tr.findAll('td')
                
                data = { "FundName": tds[2].text,
                         "House": housenum,
                         "NavDate": tds[3].text, #time.strptime(tds[3].text, "%d/%m/%Y") ,
                         "NAV": float(tds[4].text)
                        };
                #print data; 
                scraperwiki.sqlite.save(unique_keys=[], data=data)
            
        begin_date=(begin_date + relativedelta(days=1));
import scraperwiki
import mechanize
import cookielib

import urllib
import urllib2
import csv
import re
from BeautifulSoup import BeautifulSoup
import time
import datetime
from datetime import date, timedelta
import math
import random
import sys
import string
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

#scraperwiki.sqlite.execute("delete from swdata")
#scraperwiki.sqlite.commit()

#####################################################
## Mechanize Presets ##
#####################################################

br = mechanize.Browser()

###Cookie Jar###
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

###Browser options###
br.set_handle_equiv(True)
#br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

##Follows refresh 0 but not hangs on refresh > 0##
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

###Mechanize Debugging###
#~ br.set_debug_http(True)
#~ br.set_debug_redirects(True)
#~ br.set_debug_responses(True)

###User-Agent###
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

###################################################

base_url = "http://www.lifeinscouncil.org/logins/index.php"

#Write loops for query parameters

begin_date= datetime.date(2012, 12,8); #strptime("08/12/2012", "%d/%m/%Y")  + relativedelta(days=0); #(date.today() + relativedelta(months=-7));

end_date = date.today() ; # + relativedelta(days=+10);
print end_date

houses = [85];

for housenum in houses:
    while begin_date<=end_date: 
                
        #needed to set a bunch of form field values to list objects. For some reason...
        pars = { "submit" : "Go",
            "product" : housenum,
            "from_date": begin_date.strftime('%Y-%m-%d')
            }
        print pars;

        response = br.open(base_url, urllib.urlencode(pars))
        response_read=response.read()
        soup=BeautifulSoup(response_read)
        
        tables = soup.findAll('table', {'cellspacing':'1'})
                        
        for table in tables:
            trs=table.findAll('tr')
            if trs.count<=1: 
                continue;
            count=0;
            for tr in trs:
                if count==0:
                    count=1;
                    continue;
                tds=tr.findAll('td')
                
                data = { "FundName": tds[2].text,
                         "House": housenum,
                         "NavDate": tds[3].text, #time.strptime(tds[3].text, "%d/%m/%Y") ,
                         "NAV": float(tds[4].text)
                        };
                #print data; 
                scraperwiki.sqlite.save(unique_keys=[], data=data)
            
        begin_date=(begin_date + relativedelta(days=1));
