import requests
import scraperwiki
import lxml.html

'''Idea is to generate a list of links to
blog posts containing a search term
(variable: term)
'''

# The search pattern for URI's in Wordpress is:
# http://www.computing.co.uk/jobs-search-page?Keywords=software&AndOr=0


term = ""

# Passing paramaters to the site uri using "payload" dict:

site = 'http://www.cwjobs.co.uk/JobLink/Results.aspx'

payload = {
  'Keywords': term,
  'AndOr': 0,
  'ResultsUrl': 'http://www.computing.co.uk/jobs-search-page',
  'DetailsUrl': 'http://www.computing.co.uk/jobs-detail',
  'Css': 'http://www.computing.co.uk/stylesheets/job-result.css',
  'PageSize': 100
}

r = requests.get(site, params=payload)  # This'll be the results page
print r.url
html = r.text
root = lxml.html.fromstring(html)  # parsing the HTML into the var root

for i in root.cssselect(".ResultsItem h3 a"):
#     link = i.cssselect("a")
#     text = i.text_content()
    data = {
        'uri': i.get('href'),
        'job-title': i.text,
        'search-term': term
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['uri'], data=data)
