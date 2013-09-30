import scraperwiki

# Blank Python
# Blank Python
import scraperwiki
import urllib
from lxml import etree
from bs4 import BeautifulSoup
import re
from mechanize import Browser

import requests
 
import mechanize
 
url = "http://lus.dacnet.nic.in/dt_lus.aspx"

state = ["01", "32", "02", "03", "33", "23", "34", "36", "35", "40", "04", "05", "06", "07", "24", "08", "09", "37", "10", 
"11", "12", "13", "38", "14", "15", "39", "16", "17", "22", "18", "19", "25", "20", "21"]
year= ["1998-99", "1999-00", "2000-01", "2001-02", "2002-03", "2003-04", "2004-05", "2005-06", "2006-07", "2007-08", "2008-09", "2009-10", "2010-11", "2011-12"]
format=["1", "2"]
for row in range(len(state)):
    br = mechanize.Browser()
    br.set_handle_robots(False) # ignore robots
    r = br.open('http://lus.dacnet.nic.in/dt_lus.aspx')
    br.open(url)
    br.select_form(nr=0)
    br.form['DropDownList1']=[state[row]]
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=500)
    for row in range(len(year)):
               
               br.form['DropDownList2']=[year[row]]
               br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=500) 
               #for row in range(len(format)):
                    
                    #br.form['DropDownList3']=[format[row]]
                    #br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=500)
               br.submit()
               page = br.response().read()
               data = {'page':page}
               scraperwiki.sqlite.save(unique_keys=['page'],data=data)     


import scraperwiki

# Blank Python
# Blank Python
import scraperwiki
import urllib
from lxml import etree
from bs4 import BeautifulSoup
import re
from mechanize import Browser

import requests
 
import mechanize
 
url = "http://lus.dacnet.nic.in/dt_lus.aspx"

state = ["01", "32", "02", "03", "33", "23", "34", "36", "35", "40", "04", "05", "06", "07", "24", "08", "09", "37", "10", 
"11", "12", "13", "38", "14", "15", "39", "16", "17", "22", "18", "19", "25", "20", "21"]
year= ["1998-99", "1999-00", "2000-01", "2001-02", "2002-03", "2003-04", "2004-05", "2005-06", "2006-07", "2007-08", "2008-09", "2009-10", "2010-11", "2011-12"]
format=["1", "2"]
for row in range(len(state)):
    br = mechanize.Browser()
    br.set_handle_robots(False) # ignore robots
    r = br.open('http://lus.dacnet.nic.in/dt_lus.aspx')
    br.open(url)
    br.select_form(nr=0)
    br.form['DropDownList1']=[state[row]]
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=500)
    for row in range(len(year)):
               
               br.form['DropDownList2']=[year[row]]
               br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=500) 
               #for row in range(len(format)):
                    
                    #br.form['DropDownList3']=[format[row]]
                    #br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=500)
               br.submit()
               page = br.response().read()
               data = {'page':page}
               scraperwiki.sqlite.save(unique_keys=['page'],data=data)     


