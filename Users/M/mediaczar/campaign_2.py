import scraperwiki
import lxml.html     

# Searches the http://www.campaignlive.co.uk/ archives for stories containing search_term
# Returns count of articles


 
base_url =  "http://www.campaignlive.co.uk/search/articles/phrase/"

search_terms = ['content activation','highly engaging', 'social media', 'forum'] # output from bigram_count.pl process

for search_term in search_terms:

    keyword = search_term

    page_name = base_url + "%22" + search_term.replace(" ", "%20") + "%22/sortby/date/dateGroup/all/"

    html = scraperwiki.scrape(page_name)

    html = lxml.html.fromstring(html)


    total_count = html.cssselect("div.resultsSummary span")[1]

    data = {
        'keyword' : keyword,
        'count'   : total_count.text
    }
#    print data

    scraperwiki.sqlite.save(unique_keys=['keyword'], data=data)import scraperwiki
import lxml.html     

# Searches the http://www.campaignlive.co.uk/ archives for stories containing search_term
# Returns count of articles


 
base_url =  "http://www.campaignlive.co.uk/search/articles/phrase/"

search_terms = ['content activation','highly engaging', 'social media', 'forum'] # output from bigram_count.pl process

for search_term in search_terms:

    keyword = search_term

    page_name = base_url + "%22" + search_term.replace(" ", "%20") + "%22/sortby/date/dateGroup/all/"

    html = scraperwiki.scrape(page_name)

    html = lxml.html.fromstring(html)


    total_count = html.cssselect("div.resultsSummary span")[1]

    data = {
        'keyword' : keyword,
        'count'   : total_count.text
    }
#    print data

    scraperwiki.sqlite.save(unique_keys=['keyword'], data=data)