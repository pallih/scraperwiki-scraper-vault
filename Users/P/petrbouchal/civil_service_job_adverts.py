'''
Created on Feb 11, 2013

@author: petrbouchal
'''
import urllib2
import urllib
from bs4 import BeautifulSoup
from pprint import pprint

from datetime import datetime
import scraperwiki

now = datetime.now()
today = datetime.today()

# build date and time strings
datestring = datetime.strftime(today, '%Y-%m-%d')
datetimestring = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
filedatestring = datetime.strftime(now, '%Y%m%d_%H%M')

storetype = 'sw'

initurl = 'https://jobs.civilservice.gov.uk/company/nghr/jobs.cgi'
#searchpage = urllib2.urlopen(initurl).read()

#spsoup = BeautifulSoup(searchpage)
#print(spsoup)

#print(searchpage)

formpost = {"owner" : "5050000",
            "ownertype" : "fair",
            "brand_id" : "0",
            "register_job_alerts" : "",
            "submitSearchForm" : "0",
            "vac_nghr.nghr_dept" : "-",
            "vac_nghr.nghr_job_category" : "-",
            "vac_nghr.nghr_emp_type" : "-",
            "vac_nghr.nghr_grade" : "-",
            "vac_nghr.nghr_salary" : "-",
            "vac_nghr.nghr_region" : "-",
            "vac_nghr.nghr_town" : "-",
            "vac_nghr.nghr_site" : "",
            "submitSearchForm" : "Search",
            }

formencoded = urllib.urlencode(formpost)
#print(formencoded)

resultspage = urllib2.urlopen(initurl, formencoded).read()
ressoup = BeautifulSoup(resultspage)
prettysoup = ressoup.prettify()

div_res_table = ressoup.find('div', attrs={"class" : "results_table"})
jobs = div_res_table.find_all('tr', attrs={"class" : "table_row"})
for job in jobs:
    jobcells = job.find_all('td')
    joburl = jobcells[2].a['href']
    jobid = jobcells[1].contents[0].strip()
    print(joburl)
    jobpg = urllib2.urlopen(joburl).read()
    jobsoup = BeautifulSoup(jobpg)
    jobtitle = jobsoup.find('div', attrs={'id' : 'app_centre_text'})['title']
    jobt = jobsoup.find('div', attrs={'class' : 'vac_desc'})
    rows = jobt.find_all('div')
    jobdict = {}
    jobdict = {'joburl' : joburl,
               'jobtimeaccessed' : datetimestring,
               'jobid' : jobid,
               'jobtitle' : jobtitle}

    #print('Job full details: ')
    #print(jobid)
    print(jobtitle)
    for row in rows:
        entry = False
        fieldname = row.find('div', attrs={'class' : 'field_title'})
        if fieldname != None:
            fieldnamefin = fieldname.contents[0].strip()
            fieldnamefin = fieldnamefin.replace(' ','_').replace('.','')
            fieldnamefin = fieldnamefin.replace(':','_')
            fieldnamefin = fieldnamefin.replace('?','').replace('(','').replace(')','').replace('/','_')
            fieldnamefin = fieldnamefin.replace('__','_')
            entry = True
        else:
            fieldnamefin = ''
        fieldvalue = row.find('div', attrs={'class' : 'field_value'})
        if fieldvalue != None:
            fieldvaluefin = fieldvalue.contents[0].strip()
            entry = True
        else:
            fieldvaluefin = ''
        if entry == True:
            jobdict[fieldnamefin] = fieldvaluefin
            #print fieldnamefin ,
            #print ': ' + fieldvaluefin
    if storetype == 'sw':
        scraperwiki.sqlite.save(['jobtimeaccessed', 'jobid'], jobdict)
        #readback = scraperwiki.sqlite.execute('select * from swdata')
        #print(readback)


