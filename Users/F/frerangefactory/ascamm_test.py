# login and scrape the website opencores.org

import scraperwiki
import lxml.html
from lxml.html.clean import clean_html
from lxml import etree
from BeautifulSoup import BeautifulSoup as soup

from BeautifulSoup import Comment

import mechanize
import cookielib

import re, pprint, sys

pp = pprint.PrettyPrinter(indent=4)

user='vincent_'
pwd='2zpyasqk'

url = "http://www.opencores.org/login"
url_prj = "http://www.opencores.org/projects"

# function to get all projects from a specific URL
def get_projects(_url):
    r = br.open(_url)
    _html_content = r.read()
    _lxml_content = lxml.html.fromstring(_html_content) #turn the HTML into lxml object
    #print 'DEBUG', _html_content

    # Extract all projects
    projects_name = []
    projects_url = []

    # Find all 'a' elements inside 'tbody tr.row1 td.project'
    for a in _lxml_content.cssselect('tbody tr td.project a'):
        projects_name.append(a.text)
    #print 'DEBUG', projects_name

    # Find all 'a' elements inside 'tbody tr.row1 td.project' and get the 'href' link
    links = _lxml_content.cssselect('tbody tr td.project a')
    for a in links:
        projects_url.append(a.get('href'))
    #print 'DEBUG', projects_url

    # clean up text with regular expressions because
    # project names contains unwanted spaces and carriage returns
    # replace/delete unwanted text
    for i,x in enumerate(projects_name):
        projects_name[i]= re.sub('(\\n *)','',x)
    for i,x in enumerate(projects_url):
        projects_url[i]= "http://opencores.org/" + re.sub('(\\n *)','',x)
    #print 'DEBUG', projects_url

    # count how many projects there are
    #print 'Grand total of',len(projects_name),' projects:', projects_name

    # alternative and more complicated re solution
    #prjs=[]
    #for x in projects:
    #    whole=re.search('(^\\n *)(.*)(\\n *)',x)
    #    _clean = whole.group(2)
    #    prjs.append(_clean)
    #print 'Grand total of:',len(prjs),' projects:', prjs

    return projects_name, projects_url

# structure to store everything
class opencores():
    def __init__(self,):
        self.categories=[]
        self.categories_num=0
        self.categories_url=[]
        self.projects=[]
        self.projects_url=[]
        self.projects_name=[]
        self.projects_num=[]
        self.projects_html_info=[]
        self.projects_download_url=[]

# clean up html code from unwanted stuff
def filter_html(in_html):
    doc = soup(in_html)

#recs = doc.findAll("div", { "class": "class_name"})

    # remove unwanted tags
    for div in doc.findAll('head'):
        div.extract()
    for div in doc.findAll(['i', 'h1', 'script']):
        div.extract()
    for div in doc.findAll('div','top'):
        div.extract()
    for div in doc.findAll('div','bot'):
        div.extract()
    for div in doc.findAll('div','line'):
        div.extract()
    for div in doc.findAll('div','mainmenu'):
        div.extract()
    for div in doc.findAll('div','banner'):
        div.extract()
    for div in doc.findAll('div','maintainers'):
        div.extract()

    #for div in doc.findAll('div', {'style':'clear:both;margin-left:200px;'}):
    #    div.extract()

    # remove html comments
    comments = doc.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]

    out_html = doc.body.prettify()
    #out_html = re.sub('(\\n *)','\\n',out_html)

    # a little more cleaning
    out_html = re.sub('(<dd>)\\n','',out_html)
    out_html = re.sub('(</dd>)\\n','',out_html)
    out_html = re.sub('<br />','<br/>',out_html)

    return out_html

################################ MAIN ##################################

# create a structure to save everything
opencores_mem = opencores()

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
#br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Open login page and select the first form in the page
# maybe a better method to search for the form would be better
r = br.open(url)
br.select_form(nr=0)

#Aauthenticate and submit
br['user'] = user
br['pass'] = pwd

# TODO check that you have successfully authenticated
res = br.submit()
#print res.get_data()

# Access a password protected site
r = br.open(url_prj)
print 'Opening website:', br.title()

# Open page
_html_content = r.read()
#print _html_content
_lxml_content = lxml.html.fromstring(_html_content) #turn the HTML into lxml object

# Extract all project categories
for el in _lxml_content.cssselect("span.title"):
    opencores_mem.categories.append(el.text)

# count how many categories there are
opencores_mem.categories_num = len(opencores_mem.categories)
#print 'Grand total of:',opencores_mem.categories_num,' project categories:', opencores_mem.categories

# save categories
#_cat = [ {"categories":x} for x in opencores_mem.categories]
#scraperwiki.sqlite.save(["categories"], _cat)

# Extract all project url for each category with: "GET http://opencores.org/projects,category,0"
for x in range(opencores_mem.categories_num):
    opencores_mem.categories_url.append('http://opencores.org/projects,category,'+str(x))

# Extract all project for each url that defines a category
for i,x in enumerate(opencores_mem.categories_url):
    prjs_name,prjs_url = get_projects(x)
    opencores_mem.projects_url.append(prjs_url)
    opencores_mem.projects_name.append(prjs_name)
    opencores_mem.projects_num.append(len(prjs_url))

    # count how many projects there are in this specific category
    #print 'Grand total of',len(prjs_url), 'projects in the category:',opencores_mem.categories[i], '.', prjs_name

    # save project names
    #_prj = [ {"projects":x} for x in prjs ]
    #scraperwiki.sqlite.save(["projects"], _prj)


# Extract html info page for each project
for i,x in enumerate(opencores_mem.projects_name):
    opencores_mem.projects_html_info.append([])
    print 'Project category:',opencores_mem.categories[i]
    for ii,y in enumerate(x):
        _url=opencores_mem.projects_url[i][ii]
        print 'Downloading content from:', _url
        _html = br.open(_url).read()
        _html = filter_html(_html)
        #print _html
        #sys.exit(0)
        opencores_mem.projects_html_info[i].append(_html)
        if ii > 2:
            sys.exit(0)

# DEBUG - print the whole memory content
#pp.pprint(opencores_mem.categories)
#pp.pprint(opencores_mem.categories_num)
#pp.pprint(opencores_mem.categories_url)
#pp.pprint(opencores_mem.projects)
#pp.pprint(opencores_mem.projects_num)


# save opencores_mem in a database
# TODO




