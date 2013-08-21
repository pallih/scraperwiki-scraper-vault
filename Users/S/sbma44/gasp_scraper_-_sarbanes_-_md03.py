import scraperwiki
import lxml.html
import datetime
import time
import re
 
DEBUG = False
 
#if not DEBUG:
gasp_helper = scraperwiki.utils.swimport("gasp_helper")
#else:
#    import gasp_helper
 
 
# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/
 
 
# Config
gasp = gasp_helper.GaspHelper("130e13701b67494f95b71f873116ed82", "S001168")
 
def _get_html_dom(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)
 
 
# Scrape contact info for offices
def scrape_offices():
    print "Scraping offices"
    root = _get_html_dom("http://sarbanes.house.gov/free_details.asp?id=45")
    offices = root.cssselect('.bodyblock table tr td') 
    for office in offices:
        office_text = lxml.html.tostring(office)
        office_text = re.sub(r'<strong>.*?<\/strong>', '', office_text)
        office_text = re.sub(r'<\s*br\s*\/?\s*>','\n', office_text)
        office_text = re.sub(r'\n+','\n',office_text)
        address = ''
        phone = ''
        fax = ''
        phone_number = re.compile(r'(\d{3}.?\d{3}\.?\d{4}|\(?\d{3}\)?\s*\d{3}.?\d{4})')
        for line in office_text.split('\n'):
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
 
def scrape_biography():
    print "Scraping bio"
    root = _get_html_dom("http://sarbanes.house.gov/free_details.asp?id=44")
    articles = root.find_class("bodyblock")
    bio_text = lxml.html.tostring(articles[0])
    if not DEBUG:
        gasp.add_biography(bio_text)
 
def scrape_issues():
    print "Scraping Issues"
    root = _get_html_dom("http://sarbanes.house.gov/index.asp")
    issues = root.cssselect("#main-nav ul li:nth-child(3) ul li a")
    for ish in issues:
        issue_title = ish.text_content()
        issue_link = ish.get('href')
        issue_root = _get_html_dom('http://sarbanes.house.gov%s' % issue_link)
        issue_content = issue_root.find_class("bodyblock")
        issue_content = lxml.html.tostring(issue_content[0])       
        if not DEBUG:
            gasp.add_issue(issue_title, issue_content)
        else:
            print issue_title, issue_content
 
def scrape_all_press_releases():
    """Scrape all press releases we can find"""
    print "Scrape all press releases"
    root = _get_html_dom("http://sarbanes.house.gov/release.asp?id=0")
    pr_entries = root.cssselect(".bodyDate")
    for pr in pr_entries:
        link = pr.cssselect('a')
        pr_href = link[0].get('href')
        pr_title = link[0].text_content().strip()
        link_text = lxml.html.tostring(pr)
        pr_date = pr.cssselect('span span')[0].text_content()
        
        pr_url = "http://sarbanes.house.gov/%s" % pr_href
        pr_root = _get_html_dom(pr_url)
        pr_body = lxml.html.tostring(pr_root.cssselect('.newstext')[0])


        if not DEBUG:
            gasp.add_press_release(pr_title, pr_date, pr_body, url=pr_url)
        else:
            print pr_title, pr_href, pr_date, pr_body

        

# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded
 
# DONE
scrape_biography()
scrape_issues()
scrape_offices()
scrape_all_press_releases()


# TODO

#scrape_social_media()
 
 
if not DEBUG: gasp.finish()