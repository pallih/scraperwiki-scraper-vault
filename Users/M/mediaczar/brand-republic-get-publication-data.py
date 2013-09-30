import scraperwiki
import lxml.html
import math

# Searches the http://www.campaignlive.co.uk/ archives for stories containing search_term
# Returns date of article, search term, article title, and SERP

base_url =  "http://www.campaignlive.co.uk/search/articles/phrase/"
url_suffix = "%22/sortby/date/dateGroup/all/"
#url_suffix = url_suffix + "magazine/PRW/pr-week-uk/"

search_terms = ['the death of','is dead'] 

for search_term in search_terms:

# First let's get the total number of pages so that we know when to stop crawling
    keyword = search_term
    page_name = base_url + "%22" + search_term.replace(" ", "%20") + url_suffix
    html = scraperwiki.scrape(page_name)
    html = lxml.html.fromstring(html)
    total_count = html.cssselect("div.resultsSummary span")[1]
    new_count = int(math.ceil((int(total_count.text)-1)/10))+1 # lots of fiddly stuff to make sure the numbers work...


# Now we do the actual crawl
    for page_num in range (1, new_count+1):

# Build the target URL
        page_name = base_url + "%22" + search_term.replace(" ", "%20") + url_suffix + "page/" + str(page_num)
        html = scraperwiki.scrape(page_name)
        html = lxml.html.fromstring(html)

# We're using CSS selectors to choose the bits we want to keep
        for div in html.cssselect("div#resultsList div"):
                story_title = div.cssselect("h3")[0].text_content()
                story_byline = div.cssselect("h4")[0] # intermediate step
                story_excerpt = div.cssselect("p")[0].text_content()

# Split out the byline to get the date
# thx to @psychemedia -- running `try` to avoid nasty problem 
# where latin-1 characters were breaking the scraper
                try:
                    story_date = str(story_byline.text_content()).split("|")[0].strip()
                except:
                    story_date = ""


# Bundle it all up neatly...
                data = {
                    'keyword'    : search_term,
                    'page'       : page_num,
                    'title'      : story_title,
                    'date'       : story_date,
                    'snippet'    : story_excerpt
                }

# ..and export it to scraperwiki's database
                scraperwiki.sqlite.save(unique_keys=['title'], data=data)
#               print data

import scraperwiki
import lxml.html
import math

# Searches the http://www.campaignlive.co.uk/ archives for stories containing search_term
# Returns date of article, search term, article title, and SERP

base_url =  "http://www.campaignlive.co.uk/search/articles/phrase/"
url_suffix = "%22/sortby/date/dateGroup/all/"
#url_suffix = url_suffix + "magazine/PRW/pr-week-uk/"

search_terms = ['the death of','is dead'] 

for search_term in search_terms:

# First let's get the total number of pages so that we know when to stop crawling
    keyword = search_term
    page_name = base_url + "%22" + search_term.replace(" ", "%20") + url_suffix
    html = scraperwiki.scrape(page_name)
    html = lxml.html.fromstring(html)
    total_count = html.cssselect("div.resultsSummary span")[1]
    new_count = int(math.ceil((int(total_count.text)-1)/10))+1 # lots of fiddly stuff to make sure the numbers work...


# Now we do the actual crawl
    for page_num in range (1, new_count+1):

# Build the target URL
        page_name = base_url + "%22" + search_term.replace(" ", "%20") + url_suffix + "page/" + str(page_num)
        html = scraperwiki.scrape(page_name)
        html = lxml.html.fromstring(html)

# We're using CSS selectors to choose the bits we want to keep
        for div in html.cssselect("div#resultsList div"):
                story_title = div.cssselect("h3")[0].text_content()
                story_byline = div.cssselect("h4")[0] # intermediate step
                story_excerpt = div.cssselect("p")[0].text_content()

# Split out the byline to get the date
# thx to @psychemedia -- running `try` to avoid nasty problem 
# where latin-1 characters were breaking the scraper
                try:
                    story_date = str(story_byline.text_content()).split("|")[0].strip()
                except:
                    story_date = ""


# Bundle it all up neatly...
                data = {
                    'keyword'    : search_term,
                    'page'       : page_num,
                    'title'      : story_title,
                    'date'       : story_date,
                    'snippet'    : story_excerpt
                }

# ..and export it to scraperwiki's database
                scraperwiki.sqlite.save(unique_keys=['title'], data=data)
#               print data

