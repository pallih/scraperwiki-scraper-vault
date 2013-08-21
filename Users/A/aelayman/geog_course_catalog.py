# This scraper pulls the course titles from the spring 2013 time schedule fror the department of geography at UW

import scraperwiki           
import lxml.html

# specify html document to scrape
html = scraperwiki.scrape("https://www.washington.edu/students/timeschd/SPR2013/geog.html")
root = lxml.html.fromstring(html)

#loop through all tables with green background color
for titlerow in root.cssselect("table[bgcolor='#ccffcc']"):
    # all anchor elements
    links = titlerow.cssselect('a')
    #first link as split table
    fl = links[0].text_content().strip().split()
    #second link
    sl = links[1].text_content().strip()
    #td elements
    cells = titlerow.cssselect('td')
    # specify data to save
    data = {
        'dept' : fl[0],
        'course_number' : fl[1],
        'course_title' : sl,
        'aok': cells[1].text_content().strip(),
        'prereqs': cells[2].text_content().strip()
    }
    print data
    # save data
    scraperwiki.sqlite.save(unique_keys=['dept','course_number'], data=data)