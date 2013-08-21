###############################################################################
# Basic scraper- modified to test a means of alerting me about planning applications in my road
# for whatever reason, such a service does not exist on the waverley website
###############################################################################

require 'nokogiri'

# retrieve a page
starting_url = 'http://waverweb.waverley.gov.uk/live/wbc/PWL.nsf/Weekly%20List%20New?SearchView&Query=FIELD+postcode+CONTAINS+GU27%202LG&count=20&start=1'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all <td> tags
doc = Nokogiri::HTML(html)
doc.search('td').each do |td|
    puts td
    record = {'td' => td.inner_html}
    ScraperWiki.save(['td'], record)


#from visual inspection: fields include 
#
#planning application reference number  : RefNoLU
#Date of application, status, appeal allowed
#Name of applicant
#House name/address with street name, town, and post code
#Summary
#
#NOTE this query returns only 20 lines, with a next button at the bottom of the page -- added a postcode to the search to narrow results... normally <20 ...
#
end