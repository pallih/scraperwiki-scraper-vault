import scraperwiki
import urllib
from lxml import etree
from bs4 import BeautifulSoup
import re
from mechanize import Browser
import selenium

import requests
 
import mechanize
 
url = "http://agcensus.dacnet.nic.in/TalukCharacteristics.aspx"
year = ['2000']
state = ['1a']#'25a', '32a', '26a', '27a', '4a', '5a', '6a', '7a', '8a', '9a', '30a', '10a', '11a', '12a', '13a', '28a', '14a','15a', '29a', '16a', '17a', '18a', '19a', '20a', '21a', '22a']
#dist = ['1','2']#,'3','4','5','6','7','8','9','10','11']

for year_ind in range(len(year)):
    for state_ind in range(len(state)):   
        br = mechanize.Browser()
        br.set_handle_robots(False) # ignore robots
        br.open(url)
        r = br.open('http://agcensus.dacnet.nic.in/TalukCharacteristics.aspx')
        br.select_form(nr=0)
        #br.form['_ctl0:ContentPlaceHolder1:DropDownList1']=[state[state_ind]]
        br.find_control('_ctl0:ContentPlaceHolder1:DropDownList1').items[1].selected = True
        selenium.fireevent(url,click);
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        print br.find_control('_ctl0:ContentPlaceHolder1:DropDownList7')
        resp = br.submit()
        print resp.read()
        #br.form['_ctl0:ContentPlaceHolder1:Dropdownlist2'] = [year[year_ind]]
        #br.submit()
        #page = br.response().read()          
        #print br.response().read()
        #data = {'page':page}
        #scraperwiki.sqlite.save(unique_keys=['page'],data=data) 




    

