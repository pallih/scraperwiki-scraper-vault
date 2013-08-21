import sys
import traceback
import urllib
import csv
import re
from datetime import datetime
import time
from scraperwiki import datastore
import scraperwiki
from BeautifulSoup import BeautifulSoup

#scrape page
base_url = 'http://www.stfc.ac.uk'
full_list_url = 'http://www.stfc.ac.uk/GOW/Sm/Inst.asp?cx=01&sc=0&so=oa'

l = lambda x,i=0: x.contents[i].strip()


def main():
    parse_ins(fetch_scrape(full_list_url))

# credit to Julian Todd for SW csv stuff
def get_institution_data(url):
    # create index of current institution totals from our current scraped data
    s = urllib.urlopen(url)
    c = csv.reader(s.readlines())
    headers = c.next()
    alldata = []
    ins_ids = set()
    institution_data = {}
    for row in c:
        #print row
        ins_ids.add(row[10]) #collect unique institution ids
        r = dict([(k, v)  for k, v in zip(headers, row) if v])
        alldata.append(r)
    print '###############################'
    print ins_ids
    for ins in ins_ids:
        print ins
        institution_data[ins] = {'institution_id':ins, 'current_grants':int(0), 'grants_total':int(0) }
        for grant in alldata:
            try:
                if int(grant['institution_id']) == int(ins):
                    institution_data[ins]['current_grants'] += 1
                    institution_data[ins]['grants_total'] += int(grant['value'])
            except:
                print ins
                pass
    s = False
    c = False
    return institution_data


def check_diff(new_ins_data, current_ins_data):
    
    for i, d in current_ins_data.items():  
        matched = False
        if int(d['institution_id']) == int(new_ins_data['id']):
            print 'match'
            matched = True
            # check for any total changes
            if int(d['current_grants']) == int(new_ins_data['current_grants']) and \
            int(d['grants_total']) - int(new_ins_data['announced_grants_total']) < 4:
                # the published grant_value sums do not always match the summed values of the 
                # respective institutions- could be a rounding issue. (usually out by a pound or 3) !?
                # and int(d['current_grants']) == int(new_ins_data['current_grants'] :
                #print int(d['grants_total']) - int(new_ins_data['announced_grants_total']) > 2
                #print 'no chg'
                return False
            else:
                #print new_ins_data['institution']
                #print "%d -> %d" % (int(d['grants_total']), int(new_ins_data['announced_grants_total']))
                #print "%d -> %d" % (int(d['current_grants']), int(new_ins_data['current_grants']))
                return True
    if not matched:
        print 'no match'
        # new institution
        return True
    return False
    

def fetch_scrape(url):
    print 'scraping '+ url
    html = scraperwiki.scrape(url)
    return BeautifulSoup(html)

def parse_ins(institution_list):
    #http://scraperwiki.com/scrapers/export/stfc-institution-data/
    url = "http://scraperwiki.com/scrapers/export/science-grants/"
    current_ins_data = get_institution_data(url)
    ins = institution_list.findAll('tr', {'class':'tHigh', 'class':'tLow', })  
    cls_map = {'dc2':'institution', 'dc4':'current_grants', 'dc5':'announced_grants_total', }
    # cached_institution_data = get_scraper_data("http://alpha:letmein@alpha.scraperwiki.com/scrapers/export/stfc-institution-data/")
    
    # loop through all rows
    for i in ins:
        institution = {}
        link = i.find('a', {'class':'noUndStd'})
        institution['stfc_url'] = base_url + link['href']
        institution['id'] = re.match('.*in=(\-{0,1}[0-9]*)$',institution['stfc_url']).groups()[0]
        for cell_cls, name in cls_map.iteritems():
            institution[name] = i.find('td', {'class':cell_cls}).text.strip()
        institution['announced_grants_total']  = int(institution['announced_grants_total'].replace(',',''))
        # check if there are changes for the institution
        if check_diff(institution, current_ins_data):
            print str(institution['institution']) + ' - '+ str(institution['stfc_url']) + ' changed.'
            # scrape
            parse_org_depts(institution['stfc_url'], institution['id'], institution['institution'])
        else:
            print 'no change for ' + institution['institution']
            

def formatExceptionInfo(maxTBlevel=5):
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.__dict__["args"]
    except KeyError:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, maxTBlevel)
    return (excName, excArgs, excTb)             

def parse_dept(dept_page, dept_data):
    # get list of grant URLS
    grant_list = dept_page.find('ul', {'class':'gList'})
    # print grant_list
    grant_raw = grant_list.findAll('li')
    #  parse dept grants
    for g in grant_raw:
        parse_grant(g, dept_data)
        
def parse_grant(grant_html, dept_data):
    grant={}
    i=0
    grant['co_investigators'] = None
    grant['value']  = None
    grant['scheme'] = None
    grant['title'] = None
    grant['principal_investigator'] = None
    grant['value'] = None
    grant['abstract'] = None
    grant['period'] = None
    
    mapping = { 'Title:':'title',
                'Principal investigator:':'principal_investigator',
                'Co-Investigator(s):':'co_investigators',
                'Abstract:':'abstract',
                'UK &pound; Value:':'value',
                'Period:':'period',
                'Scheme:':'scheme',
                'Reference:':'reference', }
    
    elems = grant_html.findAll('div', {'class':['gLeft','gCapt','gData','gBody']})
    
    while len(elems) >= i:
        try:
            grant[mapping[elems[i].contents[0].strip()]] = elems[i+1]
        except:
            pass
        i=i+2
    # format, clean up
    grant['title'] = l(grant['title'])
    
    if grant['scheme'].contents:
        grant['scheme'] = l(grant['scheme'])
    else:
        grant['scheme'] = None
        
    grant['institution'] = dept_data['in_name']
    # grant['institution_url'] = dept_data['in_url']
    grant['institution_id'] = dept_data['in_id']
    grant['department'] = dept_data['name']
    grant['department_url'] = dept_data['url']
    grant['department_id'] = dept_data['id']
    grant['principal_investigator_url'] = base_url + str(grant['principal_investigator'].find('a')['href'])
    grant['principal_investigator'] = grant['principal_investigator'].find('a').contents[0].replace('&nbsp;',' ')
    grant['principal_investigator_id'] = re.match('.*pi=(\-{0,1}[0-9]*)$',grant['principal_investigator_url']).groups()
    grant['principal_investigator_id'] = grant['principal_investigator_id'][0]
    grant['period'] = [d.strip() for d in l(grant['period']).split('-')]
    grant['abstract'] = grant['abstract'].find(text=True).strip()
    grant['period_start'] = datetime.date(datetime.strptime(grant['period'][0],'%d/%m/%Y')).isoformat()
    grant['period_end'] = datetime.date(datetime.strptime(grant['period'][1],'%d/%m/%Y')).isoformat()
    grant['period'] = False
    
    if grant['co_investigators']:
        grant['co_investigators'] = ', '.join([l(ci) for ci in grant['co_investigators'].findAll('a')])

    if grant['value'].contents:
        grant['value'] = l(grant['value']).strip().replace(',','')
    else:
        grant['value'] = None

    grant['reference'] = l(grant['reference'],1)
    print grant['reference']
    # save
    try:
        datastore.save(unique_keys=['reference',], data=grant)
    except:
        print formatExceptionInfo()
        print '-- not saved --'
        
# parses org depts
def parse_org_depts(in_url, in_id, in_name):
    
    dept_page=fetch_scrape(in_url)
    # parse dept data
    dept_links = dept_page.findAll('a', {'class':'noUndStd'})
    # grab URL, details from link
    dept_details = [[base_url+link['href'], link.contents[0], re.match('.*dp=(\-{0,1}[0-9]*)$',link['href']).groups()[0],] for link in dept_links]
    # loop through each dept
    for d in dept_details:
        dept_data={}
        dept_data['url']=d[0]
        dept_data['name'] = d[1]
        dept_data['id']=d[2]
        dept_data['in_name']=in_name
        dept_data['in_id']=in_id
        dept_data['in_url']=in_url
        dept_page=fetch_scrape(d[0])
        print 'Fetching '+ dept_data['name'] +' grants, '+ dept_data['in_name']
        parse_dept(dept_page, dept_data)
        time.sleep(2)

main()