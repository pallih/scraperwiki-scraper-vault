from scraperwiki import scrape
from scraperwiki.sqlite import save,get_var
from urllib2 import urlopen
from lxml.html import fromstring
from datetime import *

pagedata=scrape('http://www.dcnr.state.pa.us/topogeo/groundwater/PaGWIS/SelectRecords.asp?Type=ALL')
county_values=[i.values()[0] for i in fromstring(pagedata).cssselect("['name'='cboCountyCode'] option") if i.values()[0]]

for county in county_values:
    urlstr = 'http://www.dcnr.state.pa.us/topogeo/groundwater/PaGWIS/DisplayDownload.asp?Type=All&PageType=pagwis&UserType=&cboCountyCode=%s&txtLookForLicense=&txtLookForID=&txtLookForDate=&txtLookForName=&cboMunicipalityCode=' % county
    pagedata= scrape(urlstr)
    welldata = fromstring(pagedata).cssselect('pre')[0].text_content().splitlines()
    welldata.pop(0)
    headers= welldata.pop(0).split(',')
    for rec in welldata:
       try:
           save([], dict(zip(headers, rec.split(','))))
       except Exception as e:
          print e
          print dict(zip(headers, rec.split(',')))\
        from scraperwiki import scrape
from scraperwiki.sqlite import save,get_var
from urllib2 import urlopen
from lxml.html import fromstring
from datetime import *

pagedata=scrape('http://www.dcnr.state.pa.us/topogeo/groundwater/PaGWIS/SelectRecords.asp?Type=ALL')
county_values=[i.values()[0] for i in fromstring(pagedata).cssselect("['name'='cboCountyCode'] option") if i.values()[0]]

for county in county_values:
    urlstr = 'http://www.dcnr.state.pa.us/topogeo/groundwater/PaGWIS/DisplayDownload.asp?Type=All&PageType=pagwis&UserType=&cboCountyCode=%s&txtLookForLicense=&txtLookForID=&txtLookForDate=&txtLookForName=&cboMunicipalityCode=' % county
    pagedata= scrape(urlstr)
    welldata = fromstring(pagedata).cssselect('pre')[0].text_content().splitlines()
    welldata.pop(0)
    headers= welldata.pop(0).split(',')
    for rec in welldata:
       try:
           save([], dict(zip(headers, rec.split(','))))
       except Exception as e:
          print e
          print dict(zip(headers, rec.split(',')))\
        