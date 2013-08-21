import scraperwiki


import urllib
from lxml import etree
from bs4 import BeautifulSoup
import re
from mechanize import Browser

import requests
 
import mechanize

 
url = "http://agcensus.dacnet.nic.in/TalukCharacteristics.aspx"
loop = ['23a', '1a', '24a', '2a', '3a', '31a', '25a', '32a', '26a', '27a', '4a', '5a', '6a', '7a', '8a', '9a', '30a', '10a', '11a', '12a', '13a', '28a', '14a','15a', '29a', '16a', '17a', '18a', '19a', '20a', '21a', '22a']
year= ['1995','2000','2005']
for row in range(len(year)):
    br = mechanize.Browser()
    br.set_handle_robots(False) # ignore robots
    br.open(url)
    r = br.open('http://agcensus.dacnet.nic.in/TalukCharacteristics.aspx')
    br.select_form(nr=0)
    br.form['_ctl0:ContentPlaceHolder1:Dropdownlist2']=[year[row]]
    br.submit()
    page = br.response().read()
    print page                
    data = {'page':page}
    scraperwiki.sqlite.save(unique_keys=['page'],data=data)


