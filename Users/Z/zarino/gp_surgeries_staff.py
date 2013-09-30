# Scrapes the URL and name of GP surgeries
# eg: Grove House Surgery, http://www.nhs.uk/ServiceDirectories/Pages/GP.aspx?pid=71243E73-BB80-417D-A817-E776017854B9

# Basic surgery info (address, phone, opening hours) can be found at that URL
# Detailed staff info (including name and GMC number of doctors) can be found by appending '&TopicId=9' to the URL

import scraperwiki
import lxml.html
import re

# Reset current page
# scraperwiki.sqlite.save_var('last_page_scraped', 1 )

# Drop tables (alternative to clicking "empty datastore")
# scraperwiki.sqlite.execute('DROP TABLE IF EXISTS surgeries')
# scraperwiki.sqlite.execute('DROP TABLE IF EXISTS staff')
# scraperwiki.sqlite.commit()

# Creating tables manually because that's how I roll
scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `staff` (`name` text, `gmc_number` text, `job_title` text, `qualifications` text, `pagenum` integer, `surgery` text)')
scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `surgeries` (`id` text, `name` text, `address` text)')
scraperwiki.sqlite.commit()

# 1) Find out how many surgeries there are, and on how many results pages
base = "http://www.nhs.uk/Scorecard/Pages/Results.aspx?OrgType=1&Coords=1799%%2c5148&SearchTerm=ub1+3hw&DistanceFrom=-1&TabId=30&SortType=2"
html = scraperwiki.scrape(base)
page = lxml.html.fromstring(html)
link = page.cssselect('.scorecard-header .pagination a')[0].attrib.get('href')
total_pages = re.search("PageCount=([0-9]+)", link).group(1)
wefound = page.cssselect('.filter-heading strong')[0].text
total_surgeries = re.search("([0-9]+)", wefound).group(1)

# 2) Save the numbers for later
scraperwiki.sqlite.save_var('total_pages', total_pages )
scraperwiki.sqlite.save_var('total_surgeries', total_surgeries )

# 3) Fetch the most recently scraped results page (lets us pick up where we left off if last run failed)
last_page_scraped = scraperwiki.sqlite.get_var('last_page_scraped', 1)

# 4) Loop over each results page remaining...
for pagenum in range(int(last_page_scraped), int(total_pages) + 1):

    # 4.1) Get results page content (a list of surgeries)
    html = scraperwiki.scrape(base + "&PageCount=" + str(total_pages) + "&PageNumber=" + str(pagenum))
    page = lxml.html.fromstring(html)

    # 4.2) Loop over each surgery listed on the page...
    for o in page.cssselect('div.organisation'):

        # 4.2.1) Get and save this surgery's details
        name = o.cssselect('.organisation-header h2 a')[0].attrib.get('title')
        address = o.cssselect('.address li')[0].text
        id = re.search("([^=]+)$", o.cssselect('.organisation-header h2 a')[0].attrib.get('href')).group(1)
        scraperwiki.sqlite.save(['id'], {'id': id, 'name': name, 'address': address}, table_name='surgeries' )

        # (The staff at every surgery listed on the page will be added to this object)
        staff = [] 

        # 4.2.2) Get the list of staff at this surgery
        html2 = scraperwiki.scrape('http://www.nhs.uk/ServiceDirectories/Pages/GP.aspx?Pid=%s&TopicId=9' % id)
        page2 = lxml.html.fromstring(html2)

        # 4.2.3) Loop over each member of staff...
        i = 1
        for s in page2.cssselect('.staff-details'):
            name = s.cssselect('h3')[0].text
            try:
                job_title = page2.xpath('//div[@class="staff-block clear"][' + str(i) + ']/div[@class="staff-details"]/h4[text()="Job Title:"]/following-sibling::*')[0].text
            except:
                job_title = None
            try:
                gmc_number = page2.xpath('//div[@class="staff-block clear"][' + str(i) + ']/div[@class="staff-details"]/h4[text()="GMC Number:"]/following-sibling::*')[0].text
            except:
                gmc_number = 'unavailable: ' + name
            try:
                qualifications = page2.xpath('//div[@class="staff-block clear"][' + str(i) + ']/div[@class="staff-details"]/h4[text()="Other qualifications:"]/following-sibling::*')[0].text
            except:
                qualifications = None
            staff.append({'gmc_number': gmc_number, 'name': name, 'job_title': job_title, 'qualifications': qualifications, 'surgery': id, 'pagenum': pagenum})
            print str(id) + ' // ' + str(i) + ':'
            print {'gmc_number': gmc_number, 'name': name, 'job_title': job_title, 'qualifications': qualifications, 'surgery': id, 'pagenum': pagenum}
            i = i + 1

        # 4.2.4) Save that list of all the staff at this surgery
        print 'SAVE:'
        print staff
        scraperwiki.sqlite.save(['gmc_number'], staff, table_name='staff')

        # 4.2.5) Make a note that this was the most recently scraped surgery page
        scraperwiki.sqlite.save_var('last_surgery_scraped', id )
    
    # 4.3) Make a note that this was the most recently scraped results page
    scraperwiki.sqlite.save_var('last_page_scraped', pagenum )


# Scrapes the URL and name of GP surgeries
# eg: Grove House Surgery, http://www.nhs.uk/ServiceDirectories/Pages/GP.aspx?pid=71243E73-BB80-417D-A817-E776017854B9

# Basic surgery info (address, phone, opening hours) can be found at that URL
# Detailed staff info (including name and GMC number of doctors) can be found by appending '&TopicId=9' to the URL

import scraperwiki
import lxml.html
import re

# Reset current page
# scraperwiki.sqlite.save_var('last_page_scraped', 1 )

# Drop tables (alternative to clicking "empty datastore")
# scraperwiki.sqlite.execute('DROP TABLE IF EXISTS surgeries')
# scraperwiki.sqlite.execute('DROP TABLE IF EXISTS staff')
# scraperwiki.sqlite.commit()

# Creating tables manually because that's how I roll
scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `staff` (`name` text, `gmc_number` text, `job_title` text, `qualifications` text, `pagenum` integer, `surgery` text)')
scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `surgeries` (`id` text, `name` text, `address` text)')
scraperwiki.sqlite.commit()

# 1) Find out how many surgeries there are, and on how many results pages
base = "http://www.nhs.uk/Scorecard/Pages/Results.aspx?OrgType=1&Coords=1799%%2c5148&SearchTerm=ub1+3hw&DistanceFrom=-1&TabId=30&SortType=2"
html = scraperwiki.scrape(base)
page = lxml.html.fromstring(html)
link = page.cssselect('.scorecard-header .pagination a')[0].attrib.get('href')
total_pages = re.search("PageCount=([0-9]+)", link).group(1)
wefound = page.cssselect('.filter-heading strong')[0].text
total_surgeries = re.search("([0-9]+)", wefound).group(1)

# 2) Save the numbers for later
scraperwiki.sqlite.save_var('total_pages', total_pages )
scraperwiki.sqlite.save_var('total_surgeries', total_surgeries )

# 3) Fetch the most recently scraped results page (lets us pick up where we left off if last run failed)
last_page_scraped = scraperwiki.sqlite.get_var('last_page_scraped', 1)

# 4) Loop over each results page remaining...
for pagenum in range(int(last_page_scraped), int(total_pages) + 1):

    # 4.1) Get results page content (a list of surgeries)
    html = scraperwiki.scrape(base + "&PageCount=" + str(total_pages) + "&PageNumber=" + str(pagenum))
    page = lxml.html.fromstring(html)

    # 4.2) Loop over each surgery listed on the page...
    for o in page.cssselect('div.organisation'):

        # 4.2.1) Get and save this surgery's details
        name = o.cssselect('.organisation-header h2 a')[0].attrib.get('title')
        address = o.cssselect('.address li')[0].text
        id = re.search("([^=]+)$", o.cssselect('.organisation-header h2 a')[0].attrib.get('href')).group(1)
        scraperwiki.sqlite.save(['id'], {'id': id, 'name': name, 'address': address}, table_name='surgeries' )

        # (The staff at every surgery listed on the page will be added to this object)
        staff = [] 

        # 4.2.2) Get the list of staff at this surgery
        html2 = scraperwiki.scrape('http://www.nhs.uk/ServiceDirectories/Pages/GP.aspx?Pid=%s&TopicId=9' % id)
        page2 = lxml.html.fromstring(html2)

        # 4.2.3) Loop over each member of staff...
        i = 1
        for s in page2.cssselect('.staff-details'):
            name = s.cssselect('h3')[0].text
            try:
                job_title = page2.xpath('//div[@class="staff-block clear"][' + str(i) + ']/div[@class="staff-details"]/h4[text()="Job Title:"]/following-sibling::*')[0].text
            except:
                job_title = None
            try:
                gmc_number = page2.xpath('//div[@class="staff-block clear"][' + str(i) + ']/div[@class="staff-details"]/h4[text()="GMC Number:"]/following-sibling::*')[0].text
            except:
                gmc_number = 'unavailable: ' + name
            try:
                qualifications = page2.xpath('//div[@class="staff-block clear"][' + str(i) + ']/div[@class="staff-details"]/h4[text()="Other qualifications:"]/following-sibling::*')[0].text
            except:
                qualifications = None
            staff.append({'gmc_number': gmc_number, 'name': name, 'job_title': job_title, 'qualifications': qualifications, 'surgery': id, 'pagenum': pagenum})
            print str(id) + ' // ' + str(i) + ':'
            print {'gmc_number': gmc_number, 'name': name, 'job_title': job_title, 'qualifications': qualifications, 'surgery': id, 'pagenum': pagenum}
            i = i + 1

        # 4.2.4) Save that list of all the staff at this surgery
        print 'SAVE:'
        print staff
        scraperwiki.sqlite.save(['gmc_number'], staff, table_name='staff')

        # 4.2.5) Make a note that this was the most recently scraped surgery page
        scraperwiki.sqlite.save_var('last_surgery_scraped', id )
    
    # 4.3) Make a note that this was the most recently scraped results page
    scraperwiki.sqlite.save_var('last_page_scraped', pagenum )


