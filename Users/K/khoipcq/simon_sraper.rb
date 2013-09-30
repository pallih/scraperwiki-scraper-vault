# This scraper is to scrape the summary of all Development Applications for MoreLand Council
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
# History: January 11, 2013
# By VuHT

###############################################################################################

# Required libraries

###############################################################################################



require 'rubygems'

require 'mechanize'



###############################################################################################

# Start of Section: CONSTANTS, PATTERNS, RANGES

###############################################################################################



# The starting URL to get Development Applications from

HOME_URL = "https://epathway.yarraranges.vic.gov.au/ePathway/Production/Web/default.aspx"


#base_url = "https://epathway.nillumbik.vic.gov.au/ePathway/Production/web/GeneralEnquiry/"

STARTING_URL = 'https://epathway.yarraranges.vic.gov.au/ePathway/Production/Web/GeneralEnquiry/EnquirySearch.aspx'



# COMMENT_URL_PREFIX: The prefix of the URL where users can provide a response to the council about a particular Development Application.

# That URL needs to be a persistent URL and should be specific to a particular Development Application if possible.

# Email mailto links are also valid in this field.

COMMENT_URL_PREFIX = 'mailto:nillumbik@nillumbik.vic.gov.au'



###############################################################################################

# End of Section: CONSTANTS, PATTERNS, RANGES

###############################################################################################



###############################################################################################

# Global variables

###############################################################################################



#index of page

@index = 0

#url of page

@url = ""

###############################################################################################

# Main Functions

###############################################################################################



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
    get_development_application(page, tr)
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
    page = @agent.get(link)
    return page
  else
    return nil
  end
end



##

#get_development_application and save to database

#Parameters::

# *(tag) *params*:da_container tag

#Return::

#*Author*::

#----------------------------------------------------------------------------

def get_development_application(page, da_container)

  #Get detail page of da

  detail_page = get_da_detail_page(page, da_container)
  #Get da summary
  da_summary = get_da_summary(page, da_container)
  #Create a record that includes da_summary and detail_page to save to the database
  record = da_summary
  record['page_content'] = detail_page.body.to_s.force_encoding('utf-8')
  #Save record to database
  save_record_to_database(record)
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
  da_summary = {
    'info_url' => (page.uri + tds[0].at('a')['href']).to_s,
    'comment_url' => COMMENT_URL_PREFIX + CGI::escape("Development Application Enquiry: " + clean_whitespace(tds[0].at('a').inner_text)),
    'council_reference' => clean_whitespace(tds[0].at('a').inner_text),
    'date_received' => Date.strptime(clean_whitespace(tds[1].at('span').inner_text), '%d/%m/%Y').to_s,
    'address' => clean_whitespace(tds[2].at('div').inner_text),
    'description' => CGI::unescapeHTML(clean_whitespace(tds[3].at('div').inner_text)),
    'date_scraped' => Date.today.to_s

  }
  return da_summary

end



##

#get_da_detail_page

#Parameters::

# *(tag) *params*:da_container tag

#Return:: Detail page of a da

#*Author*::

#----------------------------------------------------------------------------

def get_da_detail_page(page, da_container)
  tds = da_container.search('td')
  href = tds[0].at('a')['href']
  detail_page = page.link_with(:href => "#{href}").click
  return detail_page
end



##

#get_next_url

#Parameters::

#Return:: Link of next url

#*Author*::

#----------------------------------------------------------------------------

def get_next_url
  @index = @index + 1
  link = @url.to_s + "?PageNumber="
  link = link +  @index.to_s
  return link
end
##

#create_initial table in database to save data

#Parameters::

#Return::

#*Author*::

#----------------------------------------------------------------------------

def create_initial_table_in_database
  if ScraperWiki.show_tables()["swdata"] == nil
    ScraperWiki.sqliteexecute("CREATE TABLE 'swdata' ('date_scraped' text, 'description' text, 'info_url' text, 'council_reference' text, 'address' text, 'comment_url' text, 'page_content' text)");
  end
end



##

#save_record_to_database

#Parameters::

# *(tag) *params*: record

#Return:: Save record to database

#*Author*::

#----------------------------------------------------------------------------

def save_record_to_database(record)
  if ScraperWiki.select("* from swdata where 'council_reference'='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
end



##

#go_to_development_application_page

#Parameters::

# *(tag) *params*: page

#Return:: Go to development application page from starting page

#*Author*::

#----------------------------------------------------------------------------

def go_to_development_application_page(page)
  groupContentPanel = page.search("div[class$=GroupContentPanel]")[1]
  href = groupContentPanel.at('a')[:href]
  first_page = page.link_with(:href => "#{href}").click
  first_page_form = first_page.forms.first
  page = first_page_form.click_button
  #page= page.forms.first.click_button(page.forms.first.button_with(:value=>"Search"))
  return page
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
###############################################################################################

# End of helper functions section

###############################################################################################







###############################################################################################

# The code to scrape will start running here

###############################################################################################



@agent = Mechanize.new{|a|
  a.ssl_version,
  a.verify_mode = 'SSLv3',
  OpenSSL::SSL::VERIFY_NONE,
  a.user_agent_alias = 'Linux Firefox'
}

page = @agent.get(HOME_URL)
page = go_to_development_application_page(page)

#Initiate global variable @index

@index = 1  



#Assign global variable @url

@url = page.uri



create_initial_table_in_database



get_all_das(page)





###############################################################################################

# The code to test will start running here

###############################################################################################







# This scraper is to scrape the summary of all Development Applications for MoreLand Council
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
# History: January 11, 2013
# By VuHT

###############################################################################################

# Required libraries

###############################################################################################



require 'rubygems'

require 'mechanize'



###############################################################################################

# Start of Section: CONSTANTS, PATTERNS, RANGES

###############################################################################################



# The starting URL to get Development Applications from

HOME_URL = "https://epathway.yarraranges.vic.gov.au/ePathway/Production/Web/default.aspx"


#base_url = "https://epathway.nillumbik.vic.gov.au/ePathway/Production/web/GeneralEnquiry/"

STARTING_URL = 'https://epathway.yarraranges.vic.gov.au/ePathway/Production/Web/GeneralEnquiry/EnquirySearch.aspx'



# COMMENT_URL_PREFIX: The prefix of the URL where users can provide a response to the council about a particular Development Application.

# That URL needs to be a persistent URL and should be specific to a particular Development Application if possible.

# Email mailto links are also valid in this field.

COMMENT_URL_PREFIX = 'mailto:nillumbik@nillumbik.vic.gov.au'



###############################################################################################

# End of Section: CONSTANTS, PATTERNS, RANGES

###############################################################################################



###############################################################################################

# Global variables

###############################################################################################



#index of page

@index = 0

#url of page

@url = ""

###############################################################################################

# Main Functions

###############################################################################################



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
    get_development_application(page, tr)
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
    page = @agent.get(link)
    return page
  else
    return nil
  end
end



##

#get_development_application and save to database

#Parameters::

# *(tag) *params*:da_container tag

#Return::

#*Author*::

#----------------------------------------------------------------------------

def get_development_application(page, da_container)

  #Get detail page of da

  detail_page = get_da_detail_page(page, da_container)
  #Get da summary
  da_summary = get_da_summary(page, da_container)
  #Create a record that includes da_summary and detail_page to save to the database
  record = da_summary
  record['page_content'] = detail_page.body.to_s.force_encoding('utf-8')
  #Save record to database
  save_record_to_database(record)
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
  da_summary = {
    'info_url' => (page.uri + tds[0].at('a')['href']).to_s,
    'comment_url' => COMMENT_URL_PREFIX + CGI::escape("Development Application Enquiry: " + clean_whitespace(tds[0].at('a').inner_text)),
    'council_reference' => clean_whitespace(tds[0].at('a').inner_text),
    'date_received' => Date.strptime(clean_whitespace(tds[1].at('span').inner_text), '%d/%m/%Y').to_s,
    'address' => clean_whitespace(tds[2].at('div').inner_text),
    'description' => CGI::unescapeHTML(clean_whitespace(tds[3].at('div').inner_text)),
    'date_scraped' => Date.today.to_s

  }
  return da_summary

end



##

#get_da_detail_page

#Parameters::

# *(tag) *params*:da_container tag

#Return:: Detail page of a da

#*Author*::

#----------------------------------------------------------------------------

def get_da_detail_page(page, da_container)
  tds = da_container.search('td')
  href = tds[0].at('a')['href']
  detail_page = page.link_with(:href => "#{href}").click
  return detail_page
end



##

#get_next_url

#Parameters::

#Return:: Link of next url

#*Author*::

#----------------------------------------------------------------------------

def get_next_url
  @index = @index + 1
  link = @url.to_s + "?PageNumber="
  link = link +  @index.to_s
  return link
end
##

#create_initial table in database to save data

#Parameters::

#Return::

#*Author*::

#----------------------------------------------------------------------------

def create_initial_table_in_database
  if ScraperWiki.show_tables()["swdata"] == nil
    ScraperWiki.sqliteexecute("CREATE TABLE 'swdata' ('date_scraped' text, 'description' text, 'info_url' text, 'council_reference' text, 'address' text, 'comment_url' text, 'page_content' text)");
  end
end



##

#save_record_to_database

#Parameters::

# *(tag) *params*: record

#Return:: Save record to database

#*Author*::

#----------------------------------------------------------------------------

def save_record_to_database(record)
  if ScraperWiki.select("* from swdata where 'council_reference'='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
end



##

#go_to_development_application_page

#Parameters::

# *(tag) *params*: page

#Return:: Go to development application page from starting page

#*Author*::

#----------------------------------------------------------------------------

def go_to_development_application_page(page)
  groupContentPanel = page.search("div[class$=GroupContentPanel]")[1]
  href = groupContentPanel.at('a')[:href]
  first_page = page.link_with(:href => "#{href}").click
  first_page_form = first_page.forms.first
  page = first_page_form.click_button
  #page= page.forms.first.click_button(page.forms.first.button_with(:value=>"Search"))
  return page
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
###############################################################################################

# End of helper functions section

###############################################################################################







###############################################################################################

# The code to scrape will start running here

###############################################################################################



@agent = Mechanize.new{|a|
  a.ssl_version,
  a.verify_mode = 'SSLv3',
  OpenSSL::SSL::VERIFY_NONE,
  a.user_agent_alias = 'Linux Firefox'
}

page = @agent.get(HOME_URL)
page = go_to_development_application_page(page)

#Initiate global variable @index

@index = 1  



#Assign global variable @url

@url = page.uri



create_initial_table_in_database



get_all_das(page)





###############################################################################################

# The code to test will start running here

###############################################################################################







