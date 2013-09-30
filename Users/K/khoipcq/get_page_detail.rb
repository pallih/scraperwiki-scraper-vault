# This scraper is to scrape the summary of all Development Applications for Queanbeyan City Council

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



require 'mechanize'

require 'date'



###############################################################################################

# Start of Section: CONSTANTS, PATTERNS, RANGES

###############################################################################################



# The starting URL to get Development Applications from



STARTING_URL = 'https://services.qcc.nsw.gov.au/ePathway/prod/Web/GeneralEnquiry/EnquiryLists.aspx'



# COMMENT_URL_PREFIX: The prefix of the URL where users can provide a response to the council about a particular Development Application.

# That URL needs to be a persistent URL and should be specific to a particular Development Application if possible.

# Email mailto links are also valid in this field.



COMMENT_URL_PREFIX = 'mailto:council@qcc.nsw.gov.au?subject='



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

  page.search('table.ContentPanel tr[class$=ContentPanel]').each do |da_container|

      get_development_application(page, da_container)

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

  # Todo: Put your code here to get the next page to be scraped

  next_page_condition = page.search('input[id$=nextPageHyperLink]')

  if !next_page_condition.empty? 

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

  da_summary = get_da_summary(page, da_container, detail_page)

 

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

def get_da_summary(page, da_container, detail_page)

  # Todo: Put your code to process the da_container to get the Development Application Summary here

  #get info by list item page
  item_general_info = get_item_general_info(page, da_container, detail_page)
  
  #get info by item detail page
  item_detail_info= get_item_detail_info(detail_page)

  da_summary = {

    'info_url' => item_general_info[:info_url],
    'comment_url' => item_general_info[:comment_url],
    'council_reference' => item_general_info[:council_reference],
    'address' => item_general_info[:address],
    'description' => item_general_info[:description],
    'date_scraped' => item_general_info[:date_scraped],

    'people' => item_detail_info[:people],
    'property' => item_detail_info[:property],
    'fee' => item_detail_info[:fee],
    'decision' => item_detail_info[:decision]
  }
  item_detail_info[:info_group] = get_info_group(detail_page)
  item_detail_info[:info_group].each do |item|
    da_summary[item[:key]] = item[:field]
  end
  return da_summary

end

##

#get_item_detail_info

#Parameters::

# *(tag) *params*: detail_page

#Return:: item detail info

#*Author*::

#----------------------------------------------------------------------------

def get_item_detail_info(detail_page)

  item_detail_info = {}
  #get detail info by approciate syn_fieldsetItem
  item_detail_info[:info_group] = get_info_group(detail_page)
  item_detail_info[:people] = get_people(detail_page)
  item_detail_info[:property] = get_property(detail_page)
  item_detail_info[:fee] = get_fee(detail_page)
  item_detail_info[:decision] = get_decision(detail_page)
  return item_detail_info

end

##

#get_people

#Parameters::

# *(tag) *params*: detail_page

#Return:: people

#*Author*::

#----------------------------------------------------------------------------

def get_people(detail_page)
  first_table = detail_page.search('div#ctl00_MainBodyContent_group_17 table.ContentPanel')
  people_array = [] 
  if first_table
    list_tr = first_table.search('tr')
    for i in 1..list_tr.length-1
      list_td = list_tr[i].search('td')
      people_obj = {}
      people_obj[:role] = clean_whitespace(list_td[0].inner_text)
      people_obj[:name] = clean_whitespace(list_td[1].inner_text)
      people_obj[:address] = clean_whitespace(list_td[2].inner_text)
  
      people_array << people_obj
    end
  else
    return ""
  end
  return people_array
end

##
#get_property
#Parameters::
# *(tag) *params*: detail_page
#Return:: property
#*Author*::
#----------------------------------------------------------------------------
def get_property(detail_page)
  property_array = []
  first_table = detail_page.search('div#ctl00_MainBodyContent_group_18 table.ContentPanel')
  if first_table != nil
    list_tr = first_table.search('tr')
    for i in 1..list_tr.length-1
      list_td = list_tr[i].search('td')
      property_obj = {}
      property_obj[:property_address] = clean_whitespace(list_td[0].inner_text)
      property_array << property_obj
    end
  else
    return ""
  end
  return property_array
end


##
#get_fee
#Parameters::
# *(tag) *params*: detail_page
#Return:: fee
#*Author*::
#----------------------------------------------------------------------------
def get_fee(detail_page)
  fee_array = []
  first_table = detail_page.search('div#ctl00_MainBodyContent_group_19 table.ContentPanel')
  if first_table != nil
    list_tr = first_table.search('tr')
    for i in 1..list_tr.length-1
      list_td = list_tr[i].search('td')
      fee_obj = {}
      fee_obj[:application_fee_type] = clean_whitespace(list_td[0].inner_text)
      fee_obj[:accepted_fee_amount] = clean_whitespace(list_td[1].inner_text)
      fee_obj[:paid] = clean_whitespace(list_td[2].inner_text)
      fee_obj[:balance] = clean_whitespace(list_td[3].inner_text)
      fee_array << fee_obj
    end
  else
    return ""
  end
  return fee_array
end

##
#get_fee
#Parameters::
# *(tag) *params*: detail_page
#Return:: fee
#*Author*::
#----------------------------------------------------------------------------
def get_decision(detail_page)
  decision_array = []
  first_table = detail_page.search('div#ctl00_MainBodyContent_group_21 table.ContentPanel')
  
  if first_table != nil
    list_tr = first_table.search('tr')
    for i in 1..list_tr.length-1
      list_td = list_tr[i].search('td')
      decision_obj = {}
      decision_obj[:decision] = clean_whitespace(list_td[0].inner_text)
      decision_obj[:decision_date] = clean_whitespace(list_td[1].inner_text)
      decision_obj[:effective_date] = clean_whitespace(list_td[2].inner_text)
      decision_obj[:decision_authority] = clean_whitespace(list_td[3].inner_text)
      decision_obj[:under_appeal] = clean_whitespace((list_td[4] != nil) ? list_td[4].inner_text : "")
      decision_array << decision_obj
    end
  else
    return ""
  end
  return decision_array
end

##
#get_info_group
#Parameters::
# *(tag) *params*: detail_page
#Return:: item detail info
#*Author*::
#----------------------------------------------------------------------------
def get_info_group(detail_page)
  info_group_panel = detail_page.search('div#ctl00_MainBodyContent_group_16 table')[2]
  info_group_tr = info_group_panel.search('tr')
 
  info_group_info = []
  for i in 0..info_group_tr.length - 2
    tr = info_group_tr[i]
    info_group_td = tr.search('td')
    if (info_group_td.size > 0)
      info_group_obj = {}
      info_group_obj[:key] = clean_whitespace(info_group_td[0].inner_text).gsub(" ","_").downcase
      info_group_obj[:field] = clean_whitespace(info_group_td[1].inner_text).downcase
      info_group_info << info_group_obj
    end
  end
  return info_group_info
end

##
#get_item_general_info
#Parameters::
# *(tag) *params*: page, da_container
#Return:: item general info
#*Author*::
#----------------------------------------------------------------------------
def get_item_general_info(page, da_container, detail_page)

  #get td item that contains detail general info

  tds = da_container.search('td')
  item_general_info = {}
  item_general_info[:info_url] = get_info_url(page, tds)
  item_general_info[:council_reference] = get_council_reference(tds)
  item_general_info[:comment_url] = get_comment_url(tds)
  item_general_info[:address] = get_address(tds)
  item_general_info[:description] = get_description(detail_page, tds)
  item_general_info[:date_scraped] = get_date_scraped
  return item_general_info

end


##

#get_council_reference

#Parameters::

# *(tag) *params*:da_container tag

#Return:: council_reference

#*Author*::

#----------------------------------------------------------------------------

def get_council_reference(tds)
  clean_whitespace(tds[0].at('a').inner_text)
end



##

#get_comment_url

#Parameters::

# *(tag) *params*:da_container tag

#Return:: comment_url

#*Author*::

#----------------------------------------------------------------------------

def get_comment_url(tds)
  COMMENT_URL_PREFIX + CGI::escape("Development Application Enquiry: " + clean_whitespace(tds[0].at('a').inner_text))
end



##

#get_info_url

#Parameters::

# *(tag) *params*:da_container tag

#Return:: info_url

#*Author*::

#----------------------------------------------------------------------------

def get_info_url(page, tds)
  (page.uri + tds[0].at('a')['href']).to_s
end



##

#get_address

#Parameters::

# *(tag) *params*:da_container tag

#Return:: address

#*Author*::

#----------------------------------------------------------------------------

def get_address(tds)
  clean_whitespace(tds[2].at('div').inner_text)
end



##

#get_description

#Parameters::

# *(tag) *params*:da_container tag

#Return:: description

#*Author*::

#----------------------------------------------------------------------------

def get_description(detail_page, tds)
  table = detail_page.search('table')[31]

  tr = table.search('tr')[3]

  tds_detail_description = tr.search('td')

  description = ""

  if !tds_detail_description[1].at('span').nil? 

    description = clean_whitespace(tds_detail_description[1].at('span').text)

  else

    description = clean_whitespace(tds_detail_description[1].text)

  end
  return description
end



##

#get_date_scraped

#Parameters::

# *(tag) *params*:

#Return:: date scraped

#*Author*::

#----------------------------------------------------------------------------

def get_date_scraped

  return Date.today.to_s

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

  first_page_form = page.forms.first

  first_page_form.radiobuttons[0].click

  page = first_page_form.click_button

  page = page.forms.first.submit(page.forms.first.button_with(:value => "Search"))

  

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



@agent = Mechanize.new do |a|

  a.verify_mode = OpenSSL::SSL::VERIFY_NONE

end



page = @agent.get(STARTING_URL)



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





# This scraper is to scrape the summary of all Development Applications for Queanbeyan City Council

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



require 'mechanize'

require 'date'



###############################################################################################

# Start of Section: CONSTANTS, PATTERNS, RANGES

###############################################################################################



# The starting URL to get Development Applications from



STARTING_URL = 'https://services.qcc.nsw.gov.au/ePathway/prod/Web/GeneralEnquiry/EnquiryLists.aspx'



# COMMENT_URL_PREFIX: The prefix of the URL where users can provide a response to the council about a particular Development Application.

# That URL needs to be a persistent URL and should be specific to a particular Development Application if possible.

# Email mailto links are also valid in this field.



COMMENT_URL_PREFIX = 'mailto:council@qcc.nsw.gov.au?subject='



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

  page.search('table.ContentPanel tr[class$=ContentPanel]').each do |da_container|

      get_development_application(page, da_container)

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

  # Todo: Put your code here to get the next page to be scraped

  next_page_condition = page.search('input[id$=nextPageHyperLink]')

  if !next_page_condition.empty? 

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

  da_summary = get_da_summary(page, da_container, detail_page)

 

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

def get_da_summary(page, da_container, detail_page)

  # Todo: Put your code to process the da_container to get the Development Application Summary here

  #get info by list item page
  item_general_info = get_item_general_info(page, da_container, detail_page)
  
  #get info by item detail page
  item_detail_info= get_item_detail_info(detail_page)

  da_summary = {

    'info_url' => item_general_info[:info_url],
    'comment_url' => item_general_info[:comment_url],
    'council_reference' => item_general_info[:council_reference],
    'address' => item_general_info[:address],
    'description' => item_general_info[:description],
    'date_scraped' => item_general_info[:date_scraped],

    'people' => item_detail_info[:people],
    'property' => item_detail_info[:property],
    'fee' => item_detail_info[:fee],
    'decision' => item_detail_info[:decision]
  }
  item_detail_info[:info_group] = get_info_group(detail_page)
  item_detail_info[:info_group].each do |item|
    da_summary[item[:key]] = item[:field]
  end
  return da_summary

end

##

#get_item_detail_info

#Parameters::

# *(tag) *params*: detail_page

#Return:: item detail info

#*Author*::

#----------------------------------------------------------------------------

def get_item_detail_info(detail_page)

  item_detail_info = {}
  #get detail info by approciate syn_fieldsetItem
  item_detail_info[:info_group] = get_info_group(detail_page)
  item_detail_info[:people] = get_people(detail_page)
  item_detail_info[:property] = get_property(detail_page)
  item_detail_info[:fee] = get_fee(detail_page)
  item_detail_info[:decision] = get_decision(detail_page)
  return item_detail_info

end

##

#get_people

#Parameters::

# *(tag) *params*: detail_page

#Return:: people

#*Author*::

#----------------------------------------------------------------------------

def get_people(detail_page)
  first_table = detail_page.search('div#ctl00_MainBodyContent_group_17 table.ContentPanel')
  people_array = [] 
  if first_table
    list_tr = first_table.search('tr')
    for i in 1..list_tr.length-1
      list_td = list_tr[i].search('td')
      people_obj = {}
      people_obj[:role] = clean_whitespace(list_td[0].inner_text)
      people_obj[:name] = clean_whitespace(list_td[1].inner_text)
      people_obj[:address] = clean_whitespace(list_td[2].inner_text)
  
      people_array << people_obj
    end
  else
    return ""
  end
  return people_array
end

##
#get_property
#Parameters::
# *(tag) *params*: detail_page
#Return:: property
#*Author*::
#----------------------------------------------------------------------------
def get_property(detail_page)
  property_array = []
  first_table = detail_page.search('div#ctl00_MainBodyContent_group_18 table.ContentPanel')
  if first_table != nil
    list_tr = first_table.search('tr')
    for i in 1..list_tr.length-1
      list_td = list_tr[i].search('td')
      property_obj = {}
      property_obj[:property_address] = clean_whitespace(list_td[0].inner_text)
      property_array << property_obj
    end
  else
    return ""
  end
  return property_array
end


##
#get_fee
#Parameters::
# *(tag) *params*: detail_page
#Return:: fee
#*Author*::
#----------------------------------------------------------------------------
def get_fee(detail_page)
  fee_array = []
  first_table = detail_page.search('div#ctl00_MainBodyContent_group_19 table.ContentPanel')
  if first_table != nil
    list_tr = first_table.search('tr')
    for i in 1..list_tr.length-1
      list_td = list_tr[i].search('td')
      fee_obj = {}
      fee_obj[:application_fee_type] = clean_whitespace(list_td[0].inner_text)
      fee_obj[:accepted_fee_amount] = clean_whitespace(list_td[1].inner_text)
      fee_obj[:paid] = clean_whitespace(list_td[2].inner_text)
      fee_obj[:balance] = clean_whitespace(list_td[3].inner_text)
      fee_array << fee_obj
    end
  else
    return ""
  end
  return fee_array
end

##
#get_fee
#Parameters::
# *(tag) *params*: detail_page
#Return:: fee
#*Author*::
#----------------------------------------------------------------------------
def get_decision(detail_page)
  decision_array = []
  first_table = detail_page.search('div#ctl00_MainBodyContent_group_21 table.ContentPanel')
  
  if first_table != nil
    list_tr = first_table.search('tr')
    for i in 1..list_tr.length-1
      list_td = list_tr[i].search('td')
      decision_obj = {}
      decision_obj[:decision] = clean_whitespace(list_td[0].inner_text)
      decision_obj[:decision_date] = clean_whitespace(list_td[1].inner_text)
      decision_obj[:effective_date] = clean_whitespace(list_td[2].inner_text)
      decision_obj[:decision_authority] = clean_whitespace(list_td[3].inner_text)
      decision_obj[:under_appeal] = clean_whitespace((list_td[4] != nil) ? list_td[4].inner_text : "")
      decision_array << decision_obj
    end
  else
    return ""
  end
  return decision_array
end

##
#get_info_group
#Parameters::
# *(tag) *params*: detail_page
#Return:: item detail info
#*Author*::
#----------------------------------------------------------------------------
def get_info_group(detail_page)
  info_group_panel = detail_page.search('div#ctl00_MainBodyContent_group_16 table')[2]
  info_group_tr = info_group_panel.search('tr')
 
  info_group_info = []
  for i in 0..info_group_tr.length - 2
    tr = info_group_tr[i]
    info_group_td = tr.search('td')
    if (info_group_td.size > 0)
      info_group_obj = {}
      info_group_obj[:key] = clean_whitespace(info_group_td[0].inner_text).gsub(" ","_").downcase
      info_group_obj[:field] = clean_whitespace(info_group_td[1].inner_text).downcase
      info_group_info << info_group_obj
    end
  end
  return info_group_info
end

##
#get_item_general_info
#Parameters::
# *(tag) *params*: page, da_container
#Return:: item general info
#*Author*::
#----------------------------------------------------------------------------
def get_item_general_info(page, da_container, detail_page)

  #get td item that contains detail general info

  tds = da_container.search('td')
  item_general_info = {}
  item_general_info[:info_url] = get_info_url(page, tds)
  item_general_info[:council_reference] = get_council_reference(tds)
  item_general_info[:comment_url] = get_comment_url(tds)
  item_general_info[:address] = get_address(tds)
  item_general_info[:description] = get_description(detail_page, tds)
  item_general_info[:date_scraped] = get_date_scraped
  return item_general_info

end


##

#get_council_reference

#Parameters::

# *(tag) *params*:da_container tag

#Return:: council_reference

#*Author*::

#----------------------------------------------------------------------------

def get_council_reference(tds)
  clean_whitespace(tds[0].at('a').inner_text)
end



##

#get_comment_url

#Parameters::

# *(tag) *params*:da_container tag

#Return:: comment_url

#*Author*::

#----------------------------------------------------------------------------

def get_comment_url(tds)
  COMMENT_URL_PREFIX + CGI::escape("Development Application Enquiry: " + clean_whitespace(tds[0].at('a').inner_text))
end



##

#get_info_url

#Parameters::

# *(tag) *params*:da_container tag

#Return:: info_url

#*Author*::

#----------------------------------------------------------------------------

def get_info_url(page, tds)
  (page.uri + tds[0].at('a')['href']).to_s
end



##

#get_address

#Parameters::

# *(tag) *params*:da_container tag

#Return:: address

#*Author*::

#----------------------------------------------------------------------------

def get_address(tds)
  clean_whitespace(tds[2].at('div').inner_text)
end



##

#get_description

#Parameters::

# *(tag) *params*:da_container tag

#Return:: description

#*Author*::

#----------------------------------------------------------------------------

def get_description(detail_page, tds)
  table = detail_page.search('table')[31]

  tr = table.search('tr')[3]

  tds_detail_description = tr.search('td')

  description = ""

  if !tds_detail_description[1].at('span').nil? 

    description = clean_whitespace(tds_detail_description[1].at('span').text)

  else

    description = clean_whitespace(tds_detail_description[1].text)

  end
  return description
end



##

#get_date_scraped

#Parameters::

# *(tag) *params*:

#Return:: date scraped

#*Author*::

#----------------------------------------------------------------------------

def get_date_scraped

  return Date.today.to_s

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

  first_page_form = page.forms.first

  first_page_form.radiobuttons[0].click

  page = first_page_form.click_button

  page = page.forms.first.submit(page.forms.first.button_with(:value => "Search"))

  

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



@agent = Mechanize.new do |a|

  a.verify_mode = OpenSSL::SSL::VERIFY_NONE

end



page = @agent.get(STARTING_URL)



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





