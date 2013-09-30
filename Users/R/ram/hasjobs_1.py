# HasJobs Scraper
# Scrapes from HasGeek Job Board
# http://jobs.hasgeek.in

# Santhosh Kumar Srinivasan
# http://blog.sanspace.in

import scraperwiki
import lxml.html

def save_data(elem, jobs):
    #Get all the span elements which contains necessary information
    for span in elem.cssselect('span'):
        jobs[span.attrib['class']] = span.text_content()
    print scraperwiki.sqlite.save(unique_keys=['link'], data=jobs)


def parse_html(html):
    root = lxml.html.fromstring(html)
    # select all the stickies except the first one
    # Technically siblings of the first stickie that says POST A JOB
    for job in root.cssselect('ul#stickie-area li#newpost ~ li'):
        jobs = dict()
        jobs['link'] = 'http://jobs.hasgeek.in' + job.cssselect('a')[0].attrib['href']

        if (job.attrib['class'] == "stickie grouped"): # group postings
            for elem in job.cssselect('li > *'):
                save_data(elem, jobs)
        else:
            save_data(job, jobs)

def scrape_content(url):
    html = scraperwiki.scrape(url)
    parse_html(html)

#Start scraping
src = 'http://jobs.hasgeek.in'
scrape_content(src)

# HasJobs Scraper
# Scrapes from HasGeek Job Board
# http://jobs.hasgeek.in

# Santhosh Kumar Srinivasan
# http://blog.sanspace.in

import scraperwiki
import lxml.html

def save_data(elem, jobs):
    #Get all the span elements which contains necessary information
    for span in elem.cssselect('span'):
        jobs[span.attrib['class']] = span.text_content()
    print scraperwiki.sqlite.save(unique_keys=['link'], data=jobs)


def parse_html(html):
    root = lxml.html.fromstring(html)
    # select all the stickies except the first one
    # Technically siblings of the first stickie that says POST A JOB
    for job in root.cssselect('ul#stickie-area li#newpost ~ li'):
        jobs = dict()
        jobs['link'] = 'http://jobs.hasgeek.in' + job.cssselect('a')[0].attrib['href']

        if (job.attrib['class'] == "stickie grouped"): # group postings
            for elem in job.cssselect('li > *'):
                save_data(elem, jobs)
        else:
            save_data(job, jobs)

def scrape_content(url):
    html = scraperwiki.scrape(url)
    parse_html(html)

#Start scraping
src = 'http://jobs.hasgeek.in'
scrape_content(src)

