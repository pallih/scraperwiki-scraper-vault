import scraperwiki
import lxml.html
import datetime
import time
import re
 
DEBUG = False
 
gasp_helper = scraperwiki.utils.swimport("gasp_helper")
 
 
# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/
 
 
# Config
gasp = gasp_helper.GaspHelper("130e13701b67494f95b71f873116ed82", "E000290")
 
def _get_html_dom(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)
 
 
# Scrape contact info for offices
def scrape_offices():
    print "Scraping offices"
    root = _get_html_dom("http://donnaedwards.house.gov/")
    offices = root.cssselect('#pushedid_214 .pushcontent .pusharticle .itembody p') 
    for office in offices:
        office_text = lxml.html.tostring(office)
        office_text = re.sub(r'<\s*br\s*\/?\s*>','\n', office_text)
        office_text = re.sub(r'<\/?strong>', '', office_text)
        office_text = re.sub(r'\n+','\n',office_text)
        address = ''
        phone = ''
        fax = ''
        phone_number = re.compile(r'(\d{3}.?\d{3}.?\d{4}|\(?\d{3}\)?\s*\d{3}.?\d{4})')        
        for (i,line) in enumerate(office_text.split('\n')):
            if (i==0): continue
            line = re.sub(r'<.*?>','',line)
            phone_match = phone_number.search(line)
            if phone_match is not None:
                if 'fax' in line.lower():
                    fax = phone_match.group(1)
                else:
                    phone = phone_match.group(1)
            else:
                address = address + line


        if not DEBUG:
            gasp.add_office(address=address, phone=phone, fax=fax)
        else:
            pass
            print 'found office: ', '|'.join((address, phone, ('fax: %s' % fax)))

 
def scrape_biography():
    print "Scraping bio"
    root = _get_html_dom("http://sarbanes.house.gov/free_details.asp?id=44")
    articles = root.find_class("bodyblock")
    bio_text = lxml.html.tostring(articles[0])
    if not DEBUG:
        gasp.add_biography(bio_text)
 
def scrape_issues():
    print "Scraping Issues"
    root = _get_html_dom("http://donnaedwards.house.gov/index.cfm?sectionid=15&sectiontree=15")
    issues_page_paras = root.cssselect(".introsection .itembody p")
    issues = []
    strong_count = 0
    for potential_issue in issues_page_paras:
        if '<strong>' in lxml.html.tostring(potential_issue):
            strong_count += 1
            continue
        if strong_count==1:
            link = potential_issue.cssselect('a')
            if len(link)>0:
                issues.append(link[0])
        if strong_count>1:
            break

    print issues
    
    for issue in issues:
        issue_title = issue.text_content().strip()
        issue_link = issue.get('href')
        issue_page = _get_html_dom(issue_link)
        issue_content = lxml.html.tostring(issue_page.cssselect('#centerbox .push .pusharticle')[0])        
        if not DEBUG:
            gasp.add_issue(issue_title, issue_content)
        else:
            print issue_title, issue_content
 
def scrape_all_press_releases():
    """Scrape all press releases we can find"""
    print "Scrape all press releases"
    root = _get_html_dom("http://donnaedwards.house.gov/index.cfm?sectionid=24&sectiontree=23,24")
    pr_entries = root.cssselect(".data .sectionitems .article")
    for pr in pr_entries:
        link = pr.cssselect('h3 a')
        pr_href = link[0].get('href')
        pr_link = 'http://donnaedwards.house.gov/%s' % pr_href
        pr_title = link[0].text_content().strip()
        pr_date = pr.cssselect('.sectiondate')[0].text_content()
        
        pr_root = _get_html_dom(pr_link)
        pr_body = lxml.html.tostring(pr_root.cssselect('.contentdata')[0]).strip()


        if not DEBUG:
            gasp.add_press_release(pr_title, pr_date, pr_body, url=pr_link)
        else:
            print 'fetched press release: ', pr_title, pr_link, pr_date, pr_body

        

# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded

# DONE
scrape_issues()
scrape_all_press_releases()
scrape_offices()

# NOT DONE
#scrape_biography()
#scrape_social_media() 
 
if not DEBUG: gasp.finish()import scraperwiki
import lxml.html
import datetime
import time
import re
 
DEBUG = False
 
gasp_helper = scraperwiki.utils.swimport("gasp_helper")
 
 
# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/
 
 
# Config
gasp = gasp_helper.GaspHelper("130e13701b67494f95b71f873116ed82", "E000290")
 
def _get_html_dom(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)
 
 
# Scrape contact info for offices
def scrape_offices():
    print "Scraping offices"
    root = _get_html_dom("http://donnaedwards.house.gov/")
    offices = root.cssselect('#pushedid_214 .pushcontent .pusharticle .itembody p') 
    for office in offices:
        office_text = lxml.html.tostring(office)
        office_text = re.sub(r'<\s*br\s*\/?\s*>','\n', office_text)
        office_text = re.sub(r'<\/?strong>', '', office_text)
        office_text = re.sub(r'\n+','\n',office_text)
        address = ''
        phone = ''
        fax = ''
        phone_number = re.compile(r'(\d{3}.?\d{3}.?\d{4}|\(?\d{3}\)?\s*\d{3}.?\d{4})')        
        for (i,line) in enumerate(office_text.split('\n')):
            if (i==0): continue
            line = re.sub(r'<.*?>','',line)
            phone_match = phone_number.search(line)
            if phone_match is not None:
                if 'fax' in line.lower():
                    fax = phone_match.group(1)
                else:
                    phone = phone_match.group(1)
            else:
                address = address + line


        if not DEBUG:
            gasp.add_office(address=address, phone=phone, fax=fax)
        else:
            pass
            print 'found office: ', '|'.join((address, phone, ('fax: %s' % fax)))

 
def scrape_biography():
    print "Scraping bio"
    root = _get_html_dom("http://sarbanes.house.gov/free_details.asp?id=44")
    articles = root.find_class("bodyblock")
    bio_text = lxml.html.tostring(articles[0])
    if not DEBUG:
        gasp.add_biography(bio_text)
 
def scrape_issues():
    print "Scraping Issues"
    root = _get_html_dom("http://donnaedwards.house.gov/index.cfm?sectionid=15&sectiontree=15")
    issues_page_paras = root.cssselect(".introsection .itembody p")
    issues = []
    strong_count = 0
    for potential_issue in issues_page_paras:
        if '<strong>' in lxml.html.tostring(potential_issue):
            strong_count += 1
            continue
        if strong_count==1:
            link = potential_issue.cssselect('a')
            if len(link)>0:
                issues.append(link[0])
        if strong_count>1:
            break

    print issues
    
    for issue in issues:
        issue_title = issue.text_content().strip()
        issue_link = issue.get('href')
        issue_page = _get_html_dom(issue_link)
        issue_content = lxml.html.tostring(issue_page.cssselect('#centerbox .push .pusharticle')[0])        
        if not DEBUG:
            gasp.add_issue(issue_title, issue_content)
        else:
            print issue_title, issue_content
 
def scrape_all_press_releases():
    """Scrape all press releases we can find"""
    print "Scrape all press releases"
    root = _get_html_dom("http://donnaedwards.house.gov/index.cfm?sectionid=24&sectiontree=23,24")
    pr_entries = root.cssselect(".data .sectionitems .article")
    for pr in pr_entries:
        link = pr.cssselect('h3 a')
        pr_href = link[0].get('href')
        pr_link = 'http://donnaedwards.house.gov/%s' % pr_href
        pr_title = link[0].text_content().strip()
        pr_date = pr.cssselect('.sectiondate')[0].text_content()
        
        pr_root = _get_html_dom(pr_link)
        pr_body = lxml.html.tostring(pr_root.cssselect('.contentdata')[0]).strip()


        if not DEBUG:
            gasp.add_press_release(pr_title, pr_date, pr_body, url=pr_link)
        else:
            print 'fetched press release: ', pr_title, pr_link, pr_date, pr_body

        

# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded

# DONE
scrape_issues()
scrape_all_press_releases()
scrape_offices()

# NOT DONE
#scrape_biography()
#scrape_social_media() 
 
if not DEBUG: gasp.finish()