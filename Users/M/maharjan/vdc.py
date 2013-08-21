# PLEASE READ THIS BEFORE EDITING
#
# This script generates your email alerts, to tell you when your scrapers
# are broken or someone has edited them.
#
# It works by emailing you the output of this script. If you read the code and
# know what you're doing, you can customise it, and make it send other emails
# for other purposes.

import scraperwiki
import urllib2
import urllib
import BeautifulSoup as bs
import re
import json



url ='http://202.166.205.141/bbvrs/index_process.php'

def getpage(url, query_args):
    data = urllib.urlencode(query_args)
    request = urllib2.Request(url, data)
    response = urllib2.urlopen(request)
    page = response.read()
    jsonpage = json.loads(page)
    optdata=jsonpage['result']
    html = bs.BeautifulSoup(optdata)
    return html.findAll('option')


def getward(vdcno):
    query_args = { 'vdc':vdcno, 'list_type':'ward' } 
    data = urllib.urlencode(query_args)
    request = urllib2.Request(url, data)

    response = urllib2.urlopen(request)
    page = response.read()
    jsonpage = json.loads(page)
    optdata=jsonpage['result']
    vdctype=jsonpage['vdc_type']
    html = bs.BeautifulSoup(optdata)
    opts=html.findAll('option')
    retval = {'wards':(len(opts)-1), 'vdc_type':vdctype}
    return retval
     

for i in range(2, 2):
    query_args = { 'district':i, 'list_type':'vdc' } 
    vdcs=getpage(url, query_args)

    for vdc in vdcs:
        try:
            wardsinfo=getward(vdc['value'])
            no_of_wards=wardsinfo['wards']
            vdc_type=wardsinfo['vdc_type']
            for k in range(1, (no_of_wards+1)):
                query = { 'vdc':vdc['value'], 'ward':k, 'list_type':'reg_centre' } 
                regions=getpage(url, query)
                if(vdc_type<4):
                        vtpe='mun'
                else:
                    vtype='vdc'

                for region in regions:
                        try:
                        
                            if(region['value']!=''):
                                data = { 'vdc_name' : vdc.getText(), 'vdc_id' : vdc['value'], 'district_id':i, 'region_name':region.getText(), 'region_id' : region['value'], 'wards':k, 'vdc_type':vtype }
                                scraperwiki.sqlite.save(unique_keys=['district_id'], data=data)
                        except:
                            pass
                
                    
        except:
            pass

    

