import scraperwiki
import lxml.html     

# Searches the http://www.campaignlive.co.uk/ archives for stories containing search_term
# Returns date of article
 
base_url =  "http://www.campaignlive.co.uk/search/articles/phrase/"
search_term = "engagement"

for page_num in range (1,1460): # manually setting scrape range. Aids in debugging.
    html = scraperwiki.scrape(base_url + search_term + "/sortby/date/dateGroup/all/page/" + str(page_num))
      
    html = lxml.html.fromstring(html)

    for div in html.cssselect("div#resultsList div"):
            story_title = div.cssselect("h3")[0].text_content()
            story_byline = div.cssselect("h4")[0] # intermediate step
# thx to @psychemedia -- running `try` to avoid nasty problem where latin-1 characters were breaking
            try:
                story_date = str(story_byline.text_content()).split("|")[0].strip()
            except:
                story_date = ""
#            story_author = str(story_byline.text_content()).split("|")[1].strip() # not working
            story_excerpt = div.cssselect("p")[0].text_content()
            data = {
                'title' : story_title,
                'date' : story_date,
                'snippet' : story_excerpt,
#                'author' : story_author
            }
#            print data
            scraperwiki.sqlite.save(unique_keys=['title'], data=data)



