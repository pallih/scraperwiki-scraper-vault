import scraperwiki

import urllib2, json


#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    tckey=qsenv["TCKEY"]
except:
    tckey=''


def crunchScraper(url):
    #http://api.crunchbase.com/v/1/company/revolution-prep.js?api_key=
    url=url.replace('http://www.crunchbase.com/company/','http://api.crunchbase.com/v/1/company/')+'.js?api_key='+tckey
    cb=json.load(urllib2.urlopen(url))
    coredata={'cname':cb['name'], 'url':cb['crunchbase_url'], 'cid':cb['permalink'], 'desc':cb['description']}

    gdata=[]
    for t in cb['tag_list'].split(','):
        data=coredata.copy()
        data['tag']=t
        gdata.append(data)
    scraperwiki.sqlite.save(unique_keys=['url','cid','tag'], table_name='crunchbase_edu_companyTags', data=gdata)

    coredata['tags']=cb['tag_list']

    gdata=[]
    for r in cb['relationships']:
        data=coredata.copy()
        data['title']=r['title']
        data['name']=' '.join([r['person']['first_name'],r['person']['last_name']])
        data['id']=r['person']['permalink']
        if r['is_past']=='false': data['currency']='current'
        else: data['currency']='previous'
        print data
        gdata.append(data.copy())
    scraperwiki.sqlite.save(unique_keys=['url','id'], table_name='crunchbase_edu', data=gdata)

    for r in cb['funding_rounds']:
        gdata=[]
        coredata['round']=r['round_code']
        gdata=coredata.copy()
        for attr in ["raised_amount","raised_currency_code", "funded_year", "funded_month", "funded_day"]:
            gdata[attr]=r[attr]
        gdata['funded_date']='-'.join([str(r["funded_year"]), str(r["funded_month"]).zfill(2), str(r["funded_day"]).zfill(2) ])
        scraperwiki.sqlite.save(unique_keys=['cid','url','round'], table_name='crunchbase_edu_fundingSize', data=gdata)

        gdata=[]
        for i in r['investments']:
            data=coredata.copy()
            if i['company']!=None:
                data['name']=i['company']['name']
                data['id']=i['company']['permalink']
                data['type']='company'
            elif i['financial_org']!=None:
                data['name']=i['financial_org']['name']
                data['id']=i['financial_org']['permalink']
                data['type']='financial_org'
            elif['person']!=None:
                data['name']=' '.join([ i['person']['first_name'], i['person']['last_name'] ])
                data['id']=i['person']['permalink']
                data['type']='person'
            print data
            gdata.append(data.copy())
        scraperwiki.sqlite.save(unique_keys=['url','id','round'], table_name='crunchbase_edu_funding', data=gdata)
        

#URLs via @audreywatters http://hackeducation.com/2013/03/17/the-ed-tech-startup-crunch/
urls=["http://www.crunchbase.com/company/2u", "http://www.crunchbase.com/company/kno", "http://www.crunchbase.com/company/desire2learn", "http://www.crunchbase.com/company/kaltura", "http://www.crunchbase.com/company/rafter", "http://www.crunchbase.com/company/knewton", "http://www.crunchbase.com/company/grockit", "http://www.crunchbase.com/company/xueersi", "http://www.crunchbase.com/company/edmodo", "http://www.crunchbase.com/company/parchment", "http://www.crunchbase.com/company/axilogix-education", "http://www.crunchbase.com/company/connectedu", "http://www.crunchbase.com/company/knowledge-adventure", "http://www.crunchbase.com/company/altius-education", "http://www.crunchbase.com/company/flat-world-knowledge", "http://www.crunchbase.com/company/zeebo", "http://www.crunchbase.com/company/coursera", "http://www.crunchbase.com/company/universitynow", "http://www.crunchbase.com/company/everfi", "http://www.crunchbase.com/company/trovix", "http://www.crunchbase.com/company/bloomfire", "http://www.crunchbase.com/company/apreso-classroom", "http://www.crunchbase.com/company/classteacher-learning-systems", "http://www.crunchbase.com/company/k-12-techno-services", "http://www.crunchbase.com/company/revolution-prep"]

for u in urls:
    crunchScraper(u)

import scraperwiki

import urllib2, json


#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    tckey=qsenv["TCKEY"]
except:
    tckey=''


def crunchScraper(url):
    #http://api.crunchbase.com/v/1/company/revolution-prep.js?api_key=
    url=url.replace('http://www.crunchbase.com/company/','http://api.crunchbase.com/v/1/company/')+'.js?api_key='+tckey
    cb=json.load(urllib2.urlopen(url))
    coredata={'cname':cb['name'], 'url':cb['crunchbase_url'], 'cid':cb['permalink'], 'desc':cb['description']}

    gdata=[]
    for t in cb['tag_list'].split(','):
        data=coredata.copy()
        data['tag']=t
        gdata.append(data)
    scraperwiki.sqlite.save(unique_keys=['url','cid','tag'], table_name='crunchbase_edu_companyTags', data=gdata)

    coredata['tags']=cb['tag_list']

    gdata=[]
    for r in cb['relationships']:
        data=coredata.copy()
        data['title']=r['title']
        data['name']=' '.join([r['person']['first_name'],r['person']['last_name']])
        data['id']=r['person']['permalink']
        if r['is_past']=='false': data['currency']='current'
        else: data['currency']='previous'
        print data
        gdata.append(data.copy())
    scraperwiki.sqlite.save(unique_keys=['url','id'], table_name='crunchbase_edu', data=gdata)

    for r in cb['funding_rounds']:
        gdata=[]
        coredata['round']=r['round_code']
        gdata=coredata.copy()
        for attr in ["raised_amount","raised_currency_code", "funded_year", "funded_month", "funded_day"]:
            gdata[attr]=r[attr]
        gdata['funded_date']='-'.join([str(r["funded_year"]), str(r["funded_month"]).zfill(2), str(r["funded_day"]).zfill(2) ])
        scraperwiki.sqlite.save(unique_keys=['cid','url','round'], table_name='crunchbase_edu_fundingSize', data=gdata)

        gdata=[]
        for i in r['investments']:
            data=coredata.copy()
            if i['company']!=None:
                data['name']=i['company']['name']
                data['id']=i['company']['permalink']
                data['type']='company'
            elif i['financial_org']!=None:
                data['name']=i['financial_org']['name']
                data['id']=i['financial_org']['permalink']
                data['type']='financial_org'
            elif['person']!=None:
                data['name']=' '.join([ i['person']['first_name'], i['person']['last_name'] ])
                data['id']=i['person']['permalink']
                data['type']='person'
            print data
            gdata.append(data.copy())
        scraperwiki.sqlite.save(unique_keys=['url','id','round'], table_name='crunchbase_edu_funding', data=gdata)
        

#URLs via @audreywatters http://hackeducation.com/2013/03/17/the-ed-tech-startup-crunch/
urls=["http://www.crunchbase.com/company/2u", "http://www.crunchbase.com/company/kno", "http://www.crunchbase.com/company/desire2learn", "http://www.crunchbase.com/company/kaltura", "http://www.crunchbase.com/company/rafter", "http://www.crunchbase.com/company/knewton", "http://www.crunchbase.com/company/grockit", "http://www.crunchbase.com/company/xueersi", "http://www.crunchbase.com/company/edmodo", "http://www.crunchbase.com/company/parchment", "http://www.crunchbase.com/company/axilogix-education", "http://www.crunchbase.com/company/connectedu", "http://www.crunchbase.com/company/knowledge-adventure", "http://www.crunchbase.com/company/altius-education", "http://www.crunchbase.com/company/flat-world-knowledge", "http://www.crunchbase.com/company/zeebo", "http://www.crunchbase.com/company/coursera", "http://www.crunchbase.com/company/universitynow", "http://www.crunchbase.com/company/everfi", "http://www.crunchbase.com/company/trovix", "http://www.crunchbase.com/company/bloomfire", "http://www.crunchbase.com/company/apreso-classroom", "http://www.crunchbase.com/company/classteacher-learning-systems", "http://www.crunchbase.com/company/k-12-techno-services", "http://www.crunchbase.com/company/revolution-prep"]

for u in urls:
    crunchScraper(u)

