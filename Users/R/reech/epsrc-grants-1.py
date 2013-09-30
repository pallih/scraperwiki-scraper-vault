import scraperwiki
from scraperwiki import log
from  BeautifulSoup import BeautifulSoup, SoupStrainer
from datetime import datetime
import re
import time
import sys

from scraperwiki import datastore

base_url = 'http://gow.epsrc.ac.uk/'

f =  lambda(x): len(x.strip())
    
def parse_by_summary(page, summary):
    try:
        l = [c.strip() for c in filter(f, page.find('table',{'summary':summary}).findAll(text=True))]
        return ','.join(l)
    except:
        return u''

def parse_grants(page):
    # parse

    grant={}
    try:
        tf = page.find('table',{'id':'tblFound'}).findAll('tr')
    
        grant['epsrc_reference'] = page.find('span',id='lblGrantReference').text
        grant['url'] = '%sViewGrant.aspx?GrantRef=%s' % (base_url, grant['epsrc_reference'])
        grant['title'] = page.find('span',id='lblTitle').find('strong').contents[0]
        grant['principal_investigator'] = page.find('a',id='hlPrincipalInvestigator').text
    
        # some 'links' have no hrefs?
        if page.find('a',{'id':'hlPrincipalInvestigator'}):
            try:
                grant['principal_investicator'] = page.find('a',{'id':'hlPrincipalInvestigator'}).find('a').text
            except AttributeError:
                grant['principal_investicator'] = page.find('a',{'id':'hlPrincipalInvestigator'}).text
            try:
                grant['principal_investigator_url'] = '%s%s' % (
                                               base_url, 
                                               page.find('a',{'id':'hlPrincipalInvestigator'})['href'])
            except Exception:
                try:
                    grant['principal_investigator_url'] = '%s%s' % (
                                               base_url, 
                                               page.find('a',{'id':'hlPrincipalInvestigator'}).find('a')['href'])
                except:
                    log(sys.exc_info())
                

        grant['other_investigators'] = [t.strip() for t in tf[3].findAll('td')[1].findAll(text=True) if len(t.strip())]
        grant['other_investigators'] = ','.join(grant['other_investigators'])
        grant['project_partner'] = tf[5].findAll('td')[1].findAll(text=True)[0].strip()
        grant['project_partner'] = ','.join(grant['project_partner'])
    
        # Adding conditionals as some pages don't have the full info required
        # The exception was causing further data to not be captured
        if page.find('span',id='lblDepartment') != None:
            grant['department'] = page.find('span',id='lblDepartment').contents[0]
        if page.find('span',id='lblOrganisation') != None:
            grant['organisation'] = page.find('span',id='lblOrganisation').contents[0]
        if page.find('span',id='lblAwardType') != None:
            grant['scheme'] = page.find('span',id='lblAwardType').contents[0]
        if page.find('span',id='lblStarts') != None:
            grant['starts'] = page.find('span',id='lblStarts').contents[0]
        if page.find('span',id='lblEnds') != None:
            grant['ends'] = page.find('span',id='lblEnds').contents[0]
        if page.find('span',id='lblValue') != None:
            grant['value'] = page.find('span',id='lblValue').contents[0].replace(',','')
        grant['research_topic_classifications'] = parse_by_summary(page, summary='topic classifications')
        grant['industrial_sector_classifications'] = parse_by_summary(page, summary='sector classifications')
        grant['related_grants'] = parse_by_summary(page, summary='related grants')
        grant['summary'] = page.find('span',id='lblAbstract').find(text=True)
        grant['final_report_summary'] = page.find('span',id='lblFinalReportSummary').find(text=True) #
        grant['further_details'] = tf[-2].findAll('td')[1].findAll(text=True)[0].strip().replace('&nbsp;','')
        grant['organisation_website'] = tf[-1].findAll('a')[0]['href']
    
        #some formatting
        grant['starts'] = datetime.date(datetime.strptime(grant['starts'],'%d %B %Y')).isoformat()
        grant['ends'] = datetime.date(datetime.strptime(grant['ends'],'%d %B %Y')).isoformat()
        print grant
    
        #save to datastore
        datastore.save(unique_keys=['epsrc_reference',], data=grant)
    
    except:
        log(sys.exc_info())

def parse_depts(page):
    depts = page.findAll('a',href=re.compile('ViewDepartment.aspx'))
    for dept_url in depts:
        list_page = fetch_scrape(base_url + dept_url['href'])
        grant_urls = list_page.findAll('a',href=re.compile('ViewGrant.aspx'))
        for g in grant_urls:
            print 'fetching: %s%s' % (base_url, g['href'],)
            grant = fetch_scrape(base_url + g['href'])
            parse_grants(grant)
        
def parse_orgs(bs_resource):
    org_urls = bs_resource.findAll(href=re.compile('ViewOrg'))
    for o in org_urls:
        org_page = fetch_scrape(base_url + o['href'])
        parse_depts(org_page)
        
def fetch_scrape(url):
    html = scraperwiki.scrape(url)
    return BeautifulSoup(html)

# Main
initial_page= fetch_scrape('http://gow.epsrc.ac.uk/ListOrganisations.aspx')
parse_orgs(initial_page)

# note:
# seems to break here: http://gow.epsrc.ac.uk/ViewGrant.aspx?GrantRef=EP/G032904/1


import scraperwiki
from scraperwiki import log
from  BeautifulSoup import BeautifulSoup, SoupStrainer
from datetime import datetime
import re
import time
import sys

from scraperwiki import datastore

base_url = 'http://gow.epsrc.ac.uk/'

f =  lambda(x): len(x.strip())
    
def parse_by_summary(page, summary):
    try:
        l = [c.strip() for c in filter(f, page.find('table',{'summary':summary}).findAll(text=True))]
        return ','.join(l)
    except:
        return u''

def parse_grants(page):
    # parse

    grant={}
    try:
        tf = page.find('table',{'id':'tblFound'}).findAll('tr')
    
        grant['epsrc_reference'] = page.find('span',id='lblGrantReference').text
        grant['url'] = '%sViewGrant.aspx?GrantRef=%s' % (base_url, grant['epsrc_reference'])
        grant['title'] = page.find('span',id='lblTitle').find('strong').contents[0]
        grant['principal_investigator'] = page.find('a',id='hlPrincipalInvestigator').text
    
        # some 'links' have no hrefs?
        if page.find('a',{'id':'hlPrincipalInvestigator'}):
            try:
                grant['principal_investicator'] = page.find('a',{'id':'hlPrincipalInvestigator'}).find('a').text
            except AttributeError:
                grant['principal_investicator'] = page.find('a',{'id':'hlPrincipalInvestigator'}).text
            try:
                grant['principal_investigator_url'] = '%s%s' % (
                                               base_url, 
                                               page.find('a',{'id':'hlPrincipalInvestigator'})['href'])
            except Exception:
                try:
                    grant['principal_investigator_url'] = '%s%s' % (
                                               base_url, 
                                               page.find('a',{'id':'hlPrincipalInvestigator'}).find('a')['href'])
                except:
                    log(sys.exc_info())
                

        grant['other_investigators'] = [t.strip() for t in tf[3].findAll('td')[1].findAll(text=True) if len(t.strip())]
        grant['other_investigators'] = ','.join(grant['other_investigators'])
        grant['project_partner'] = tf[5].findAll('td')[1].findAll(text=True)[0].strip()
        grant['project_partner'] = ','.join(grant['project_partner'])
    
        # Adding conditionals as some pages don't have the full info required
        # The exception was causing further data to not be captured
        if page.find('span',id='lblDepartment') != None:
            grant['department'] = page.find('span',id='lblDepartment').contents[0]
        if page.find('span',id='lblOrganisation') != None:
            grant['organisation'] = page.find('span',id='lblOrganisation').contents[0]
        if page.find('span',id='lblAwardType') != None:
            grant['scheme'] = page.find('span',id='lblAwardType').contents[0]
        if page.find('span',id='lblStarts') != None:
            grant['starts'] = page.find('span',id='lblStarts').contents[0]
        if page.find('span',id='lblEnds') != None:
            grant['ends'] = page.find('span',id='lblEnds').contents[0]
        if page.find('span',id='lblValue') != None:
            grant['value'] = page.find('span',id='lblValue').contents[0].replace(',','')
        grant['research_topic_classifications'] = parse_by_summary(page, summary='topic classifications')
        grant['industrial_sector_classifications'] = parse_by_summary(page, summary='sector classifications')
        grant['related_grants'] = parse_by_summary(page, summary='related grants')
        grant['summary'] = page.find('span',id='lblAbstract').find(text=True)
        grant['final_report_summary'] = page.find('span',id='lblFinalReportSummary').find(text=True) #
        grant['further_details'] = tf[-2].findAll('td')[1].findAll(text=True)[0].strip().replace('&nbsp;','')
        grant['organisation_website'] = tf[-1].findAll('a')[0]['href']
    
        #some formatting
        grant['starts'] = datetime.date(datetime.strptime(grant['starts'],'%d %B %Y')).isoformat()
        grant['ends'] = datetime.date(datetime.strptime(grant['ends'],'%d %B %Y')).isoformat()
        print grant
    
        #save to datastore
        datastore.save(unique_keys=['epsrc_reference',], data=grant)
    
    except:
        log(sys.exc_info())

def parse_depts(page):
    depts = page.findAll('a',href=re.compile('ViewDepartment.aspx'))
    for dept_url in depts:
        list_page = fetch_scrape(base_url + dept_url['href'])
        grant_urls = list_page.findAll('a',href=re.compile('ViewGrant.aspx'))
        for g in grant_urls:
            print 'fetching: %s%s' % (base_url, g['href'],)
            grant = fetch_scrape(base_url + g['href'])
            parse_grants(grant)
        
def parse_orgs(bs_resource):
    org_urls = bs_resource.findAll(href=re.compile('ViewOrg'))
    for o in org_urls:
        org_page = fetch_scrape(base_url + o['href'])
        parse_depts(org_page)
        
def fetch_scrape(url):
    html = scraperwiki.scrape(url)
    return BeautifulSoup(html)

# Main
initial_page= fetch_scrape('http://gow.epsrc.ac.uk/ListOrganisations.aspx')
parse_orgs(initial_page)

# note:
# seems to break here: http://gow.epsrc.ac.uk/ViewGrant.aspx?GrantRef=EP/G032904/1


