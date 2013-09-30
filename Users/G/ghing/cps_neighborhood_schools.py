"""
Retrieve a list of Neighborhood Schools from the Chicago Public Schools Website.

More about neighborhood schools: http://www.cps.edu/Schools/Elementary_schools/Pages/Neighborhood.aspx

This lives at http://scraperwiki.com/scrapers/cps_neighborhood_schools/
"""

import scraperwiki
import mechanize
import re
from BeautifulSoup import BeautifulSoup, Tag
    
def build_address(address_tree):
    """Convert the HTML tree of the address to a single string."""
    address = ""
    for item in address_tree:
        if isinstance(item, Tag):
            # The only tags in the address are <br />.
            # Convert them to newlines
            address += "\n"
        else:
            address += item

    return address

def find_next_link(soup, page):
    """Get the link object for the next page."""
    #print page
    # BOOKMARK
    # TODO: Handle the % 5 pages Links look like <<...678910...>>
    link_text = str(page)
    if page % 5 == 1 and page != 1:
        link_text = '...'
        matches = soup.findAll(text=link_text)
        if len(matches) == 2:
            #print link_text
            #print soup.findAll(text=link_text)[1].parent['href']         
            return soup.findAll(text=link_text)[1].parent

    else:                       
        for match in soup.findAll(text=link_text):
            if match.parent.name == 'a':
                # print match.parent['href']
                return match.parent         
    
    #print soup
    return None

def get_event_target_and_argument(link):
    """
    Extract the target and argument from an APS.NET postback link.
    
    The links look something like this:
    javascript:__doPostBack('ctl00$ctl12$g_e65941ee_65d3_4025_90ba_967093604d8d$ctl00$gvSchoolSearchResults','Page$2')
    """
    match = re.search("'([a-zA-Z0-9\$_]+)','(Page\$[0-9]+)'", link['href'])
    return (match.group(1), match.group(2))
    
def do_post_back(link):
    br.select_form(name='aspnetForm')
    br.form.set_all_readonly(False)
    (target, argument) = get_event_target_and_argument(link)
    print "DEBUG: target = %s, argument = %s\n" % (target, argument)
    br['__EVENTTARGET'] = target
    br['__EVENTARGUMENT'] = argument

    return br.submit()

def assert_page_equals(soup, page):
    """
    Confirm that we're scraping the page we think we're scraping.


    I.e. when we do the postback, are we really being directed to the next page?
    """
    # We figure out what page we're on by looking at the paging links.  The current page
    # is wrapped in a span, e.g. <span>1</span> for page 1.
    # There should be two links, one before the list and one after
    assert len(soup.findAll(lambda tag: tag.name == 'span' and tag.string == str(page))) == 2

def find_page_number(soup):
    return soup.findAll(lambda tag: tag.name == 'span' and tag.string != None and re.search("^[0-9]+$", tag.string) != None)[0].string

def scrape_and_look_for_next_link(html, page=1):
    soup = BeautifulSoup(html)
    try:
        assert_page_equals(soup, page)
        print "Scraping page %d ..." % (page)
        # BEGIN DEBUG
        if page == 6:
            print soup
        # END DEBUG
        scrape(soup)
        # Search for link to next page
        next_link = find_next_link(soup, page + 1)
    
        if next_link != None:
            print "Clicking on link %s ...\n" % (next_link)
            response = do_post_back(next_link)
            scrape_and_look_for_next_link(response.read(), page + 1)

    except AssertionError:
        print "Error: We want to be scraping page %s but we're actually scraping page %s\n" % \
              (page, find_page_number(soup))
    
def scrape(soup):
    """Use BeautifulSoup to get all school rows"""
    for school_row in soup.findAll("tr", { "class" : "CPS_borderGray1px" }):
        #print school_row
        school_record = {
            "name" : None,
            "url" : None,
            "address" : None,
            "type" : None,
            "zone" : None,
            "grades" : None,
            "num_students" : None
        }

        columns = school_row.findAll("td", recursive=False)
    
        school_record['name'] = columns[1].find("a").string
        school_record['url'] = "http://www.cps.edu" + columns[1].find("a")["href"]
        school_record['address'] = build_address(columns[1].find("span").contents)
        #print columns[2]
        school_record['type'] = columns[2].find("div", { "class" : "CPS_text_center CPS_icon_description" }).find("span").string
        school_record['zone'] = columns[3].find("div", { "class" : "CPS_text_center CPS_icon_description" }).find("span").string
        school_record['grades'] = columns[4].find("div", { "class" : "CPS_text_center CPS_icon_description" }).find("span").string
        school_record['num_students'] = columns[5].find("div", { "class" : "CPS_text_center CPS_icon_description" }).find("span").string
        
        scraperwiki.datastore.save(["name"], school_record)


# retrieve a page
starting_url = 'http://www.cps.edu/Schools/Find_a_school/Pages/SchoolSearchResults.aspx?Type=1&Filter=CPSSchoolGrade=Elementary%20school;CPSSchoolType=Neighborhood'
br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16')]
br.open(starting_url)
html = br.response().read()
scrape_and_look_for_next_link(html)
"""
Retrieve a list of Neighborhood Schools from the Chicago Public Schools Website.

More about neighborhood schools: http://www.cps.edu/Schools/Elementary_schools/Pages/Neighborhood.aspx

This lives at http://scraperwiki.com/scrapers/cps_neighborhood_schools/
"""

import scraperwiki
import mechanize
import re
from BeautifulSoup import BeautifulSoup, Tag
    
def build_address(address_tree):
    """Convert the HTML tree of the address to a single string."""
    address = ""
    for item in address_tree:
        if isinstance(item, Tag):
            # The only tags in the address are <br />.
            # Convert them to newlines
            address += "\n"
        else:
            address += item

    return address

def find_next_link(soup, page):
    """Get the link object for the next page."""
    #print page
    # BOOKMARK
    # TODO: Handle the % 5 pages Links look like <<...678910...>>
    link_text = str(page)
    if page % 5 == 1 and page != 1:
        link_text = '...'
        matches = soup.findAll(text=link_text)
        if len(matches) == 2:
            #print link_text
            #print soup.findAll(text=link_text)[1].parent['href']         
            return soup.findAll(text=link_text)[1].parent

    else:                       
        for match in soup.findAll(text=link_text):
            if match.parent.name == 'a':
                # print match.parent['href']
                return match.parent         
    
    #print soup
    return None

def get_event_target_and_argument(link):
    """
    Extract the target and argument from an APS.NET postback link.
    
    The links look something like this:
    javascript:__doPostBack('ctl00$ctl12$g_e65941ee_65d3_4025_90ba_967093604d8d$ctl00$gvSchoolSearchResults','Page$2')
    """
    match = re.search("'([a-zA-Z0-9\$_]+)','(Page\$[0-9]+)'", link['href'])
    return (match.group(1), match.group(2))
    
def do_post_back(link):
    br.select_form(name='aspnetForm')
    br.form.set_all_readonly(False)
    (target, argument) = get_event_target_and_argument(link)
    print "DEBUG: target = %s, argument = %s\n" % (target, argument)
    br['__EVENTTARGET'] = target
    br['__EVENTARGUMENT'] = argument

    return br.submit()

def assert_page_equals(soup, page):
    """
    Confirm that we're scraping the page we think we're scraping.


    I.e. when we do the postback, are we really being directed to the next page?
    """
    # We figure out what page we're on by looking at the paging links.  The current page
    # is wrapped in a span, e.g. <span>1</span> for page 1.
    # There should be two links, one before the list and one after
    assert len(soup.findAll(lambda tag: tag.name == 'span' and tag.string == str(page))) == 2

def find_page_number(soup):
    return soup.findAll(lambda tag: tag.name == 'span' and tag.string != None and re.search("^[0-9]+$", tag.string) != None)[0].string

def scrape_and_look_for_next_link(html, page=1):
    soup = BeautifulSoup(html)
    try:
        assert_page_equals(soup, page)
        print "Scraping page %d ..." % (page)
        # BEGIN DEBUG
        if page == 6:
            print soup
        # END DEBUG
        scrape(soup)
        # Search for link to next page
        next_link = find_next_link(soup, page + 1)
    
        if next_link != None:
            print "Clicking on link %s ...\n" % (next_link)
            response = do_post_back(next_link)
            scrape_and_look_for_next_link(response.read(), page + 1)

    except AssertionError:
        print "Error: We want to be scraping page %s but we're actually scraping page %s\n" % \
              (page, find_page_number(soup))
    
def scrape(soup):
    """Use BeautifulSoup to get all school rows"""
    for school_row in soup.findAll("tr", { "class" : "CPS_borderGray1px" }):
        #print school_row
        school_record = {
            "name" : None,
            "url" : None,
            "address" : None,
            "type" : None,
            "zone" : None,
            "grades" : None,
            "num_students" : None
        }

        columns = school_row.findAll("td", recursive=False)
    
        school_record['name'] = columns[1].find("a").string
        school_record['url'] = "http://www.cps.edu" + columns[1].find("a")["href"]
        school_record['address'] = build_address(columns[1].find("span").contents)
        #print columns[2]
        school_record['type'] = columns[2].find("div", { "class" : "CPS_text_center CPS_icon_description" }).find("span").string
        school_record['zone'] = columns[3].find("div", { "class" : "CPS_text_center CPS_icon_description" }).find("span").string
        school_record['grades'] = columns[4].find("div", { "class" : "CPS_text_center CPS_icon_description" }).find("span").string
        school_record['num_students'] = columns[5].find("div", { "class" : "CPS_text_center CPS_icon_description" }).find("span").string
        
        scraperwiki.datastore.save(["name"], school_record)


# retrieve a page
starting_url = 'http://www.cps.edu/Schools/Find_a_school/Pages/SchoolSearchResults.aspx?Type=1&Filter=CPSSchoolGrade=Elementary%20school;CPSSchoolType=Neighborhood'
br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16')]
br.open(starting_url)
html = br.response().read()
scrape_and_look_for_next_link(html)
