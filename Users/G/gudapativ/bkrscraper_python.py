#import mechanize
import lxml.html
import scraperwiki
import urlparse
import urllib2
import json

# Blank Pythonbr = mechanize.Browser()
html=scraperwiki.scrape('http://www.bkstr.com/')
print html
usa_url='http://www.bkstr.com/webapp/wcs/stores/servlet/StoreFinderAJAX?requestType=STATESUS&pageType=FLGStoreCatalogDisplay&pageSubType=US&langId=-1&demoKey=d&stateUSAIdSelect='
results_json = urllib2.urlopen(usa_url).read()
print results_json
output=lxml.html.fromstring(results_json).text_content()
#print output start=output.find('(') end=output.find(')') print start,end
output_json=output[19:output.__len__()-2]
print output_json
last=json.loads(output_json)
for post in last['data']:    
    print post    
for key,val in post.items():
    print key
    state_url='http://www.bkstr.com/webapp/wcs/stores/servlet/StoreFinderAJAX?requestType=INSTITUTESUS&pageType=FLGStoreCatalogDisplay&pageSubType=US&langId=-1&demoKey=d&stateProvinceId='+val
    state=lxml.html.fromstring(urllib2.urlopen(state_url).read()).text_content()
    state_output=state[19:state.__len__()-2]
    #print state
    states=json.loads(state_output)
    print states
    for stat in states['data']:
        for state_name,code in stat.items():
            #print state_name+"\t"+code
            univ_url='http://www.bkstr.com/webapp/wcs/stores/servlet/StoreFinderAJAX?requestType=CAMPUSUS&pageType=FLGStoreCatalogDisplay&pageSubType=US&langId=-1&demoKey=d&institutionId='+code
            univ_code=lxml.html.fromstring(urllib2.urlopen(univ_url).read()).text_content()
            univ_output=json.loads(univ_code[19:univ_code.__len__()-2])
            #print univ_output
            for univ in univ_output['data']: 
                for uni_url,cod in univ.items():    
                    url1='http://www.bkstr.com/webapp/wcs/stores/servlet/StoreFinderAJAX?campusId='+cod+'&requestType=STOREDOMAIN&pageType=FLGStoreCatalogDisplay&langId=-1'
                    link1=lxml.html.fromstring(urllib2.urlopen(url1).read()).text_content()
                    link1_json=json.loads(link1[19:link1.__len__()-2])
                    #link1_data=link1_json['data']
                    for lin in link1_json['data']:
                        for key,val in lin.items():
                            if(val.isdidgit()): 
                                print state_name,code,cod,val 
                            



    



