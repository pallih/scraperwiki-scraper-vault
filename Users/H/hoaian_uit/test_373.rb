# This scraper is to scrape the summary of all Development Applications for a Sample Council
# The summary of a Development Application includes:

# 1. council_reference: The unique identification assigned for a Development Application by the authority

#    Example: 'TA/00323/2012'

# 2. address: The physical address that the Development Application relates to. This will be geocoded so doesn't need to be a specific format
#    but obviously the more explicit it is the more likely it will be successfully geo-coded.
#    If the original address did not include the state (e.g. "QLD") at the end, then add it.

#    Example: '1 Sowerby St, Goulburn, NSW'

# 3. description: A text description of what the Development Application seeks to carry out.

#    Example: 'Ground floor alterations to rear and first floor addition'

# 4. info_url:  A URL that provides more information about the Development Application.
#    This should be a persistent URL that preferably is specific to this particular Development Application.
#    In many cases councils force users to click through a license to access Development Application.
#    In this case be careful about what URL you provide. Test clicking the link in a browser that hasn't established a session
#    with the council's site to ensure you will be able to click the link and not be presented with an error.

#    Example: 'http://foo.gov.au/app?key=527230'

# 5. comment_url:  A URL where users can provide a response to council about this particular Development Application.
#    As in info_url this needs to be a persistent URL and should be specific to this particular Development Application if possible.
#    Email mailto links are also valid in this field.

#    Example: 'http://foo.gov.au/comment?key=527230'

# 6. date_scraped:  The date that the scraper collects this data (i.e. now). Should be in ISO 8601 format.
#    Use the following Ruby code: Date.today.to_s

#    Example: '2012-08-01'

# History: December 27, 2012
# By nhuanvn

# Required libraries

require 'rubygems'
require 'mechanize'

# The starting URL to get Development Applications from

STARTING_URL = 'http://www.easy.co.il/%D7%A7%D7%98%D7%92%D7%95%D7%A8%D7%99%D7%95%D7%AA-%D7%A4%D7%95%D7%A4%D7%95%D7%9C%D7%A8%D7%99%D7%95%D7%AA/'


# COMMENT_URL_PREFIX: The prefix of the URL where users can provide a response to the council about a particular Development Application.
# That URL needs to be a persistent URL and should be specific to a particular Development Application if possible.
# Email mailto links are also valid in this field.

COMMENT_URL_PREFIX = 'mailto:info@moreland.vic.gov.au?subject='


##
#get_all_das
#Parameters::
# *(Page) *params*:page
#Return:: All Development Applications from this council
#*Author*::
#----------------------------------------------------------------------------
def get_all_das(page)
  while (is_available(page)) do
    get_all_das_in_page(page)
    page = get_next_page(page)
    p page.body
  end
end


##
#is_available
#Parameters::
# *(Page) *params*:page
#Return:: Return true if the page is available for scraping Development Applications. Return false otherwise
#*Author*::
#----------------------------------------------------------------------------
def is_available(page)
  # Todo: Return true if the page is available for scraping Development Applications. Return false otherwise
  return !page.nil? 
end

##
#get_all_das_in_page

#Parameters::
# *(Page) *params*:page
#Return:: list of da in page
#*Author*::
#----------------------------------------------------------------------------
def get_all_das_in_page(page)
  # Todo: For each element of the page that contains the Development Application, get Development Application Summary.
  # For example:

  page.search('table.ContentPanel tr[class$=ContentPanel]').each do |tr|
    get_da_summary(page, tr)
  end
end

##
#is available
#Parameters::
# *(Page) *params*:page
#Return:: true or false
#*Author*::
#----------------------------------------------------------------------------
def has_next_page(page)
  next_page_condition = page.at('input[id$=nextPageHyperLink]')
  unless next_page_condition.nil? || next_page_condition['onclick'] =~ /return false/
    return true
  else
    return false
  end
end

##
#get_next_page
#Parameters::
# *(Page) *params*:page
#Return:: The next page to be scraped
#*Author*::
#----------------------------------------------------------------------------
def get_next_page(page)
  if has_next_page(page)
    next_page_condition = page.at('input[id$=nextPageHyperLink]')
    link = get_next_url()
    p "==>" + link.to_s
    
    page = @agent.get(link)
    return page
  else
    return nil
  end
end

##
#get_da_summary

#Parameters::
# *(tag) *params*:da_container tag
#Return:: The Development Application Summary which contains the list of fields as described on the top of this source file
#*Author*::
#----------------------------------------------------------------------------
def get_da_summary(page, da_container)
  # Todo: Put your code to process the da_container to get the Development Application Summary here
  
  tds = da_container.search('td')
  h = tds.map{|td| td.inner_html}

  record = {
    'info_url' => (page.uri + tds[0].at('a')['href']).to_s,
    'comment_url' => COMMENT_URL_PREFIX + CGI::escape("Development Application Enquiry: " + clean_whitespace(tds[0].at('a').inner_text)),
    'council_reference' => clean_whitespace(tds[0].at('a').inner_text),
    'date_received' => Date.strptime(clean_whitespace(tds[1].at('span').inner_text), '%d/%m/%Y').to_s,
    'address' => clean_whitespace(tds[3].at('span').inner_text),
    'description' => CGI::unescapeHTML(clean_whitespace(tds[2].at('span').inner_text)),
    'date_scraped' => Date.today.to_s
  }
  #if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty?
    ScraperWiki.save_sqlite(['council_reference'], record)
  #else
  #  puts "Skipping already saved record " + record['council_reference']
  #end
end

###############################################################################################
# Start of helper functions section
###############################################################################################

##
#clean whitespace
#Parameters::
# *(tag) *params*: a tag
#Return::a tag
#*Author*::
#----------------------------------------------------------------------------
def clean_whitespace(a)
  a.gsub("\r", ' ').gsub("\n", ' ').squeeze(" ").strip
end

def get_next_url
  @index = @index + 1
  link = @url.to_s + "?PageNumber="
  link = link +  @index.to_s
  p link
  return link
end

def process_category link

  p "Category ==>" + link
 
  # get page
  page_category = @agent.get(link)
  p page_category.body
  
  # get all regions link
  #page_category.search('a') do |item|
  #  p "-" + item[:href].to_s
  #nd

  # p "Ki da"
  
end

def process_regions link
  page_category = @agent.get(link)
  p page_category.body
end

###############################################################################################
# End of helper functions section
###############################################################################################


###############################################################################################
# The code to scrape will start running here
###############################################################################################

@agent = Mechanize.new
page = @agent.get('http://www.cars.com')
p page.body

form = page.form_with(:name=>'newForm')
field = form.field_with(:name=>'make')
p field.options


#get_all_das(page)


