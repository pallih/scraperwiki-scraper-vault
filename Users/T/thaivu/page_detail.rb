# This scraper is to scrape the summary of all Development Applications for Wodonga Council
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
require 'active_support'
###############################################################################################
# Start of Section: CONSTANTS, PATTERNS, RANGES
###############################################################################################
# The starting URL to get Development Applications from
STARTING_URL = 'https://eservices.wodonga.vic.gov.au/ePathway/Production/Web/GeneralEnquiry/EnquiryLists.aspx'
STARTING_URL_SORTED = 'https://eservices.wodonga.vic.gov.au/ePathway/Production/Web/GeneralEnquiry/EnquirySummaryView.aspx?SortFieldNumber=1&SortDirection=Descending'
# COMMENT_URL_PREFIX: The prefix of the URL where users can provide a response to the council about a particular Development Application.
# That URL needs to be a persistent URL and should be specific to a particular Development Application if possible.
# Email mailto links are also valid in this field.
COMMENT_URL_PREFIX = 'mailto:info@wodonga.vic.gov.au?subject='
PERIOD_DATE = 15.days
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
@end_date = Date.today - PERIOD_DATE
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
  # Todo: Return true if the page is available for scraping Development Applications. Return false otherwise
  result = false
  if !page.nil? 
    contents = page.search('table.ContentPanel tr[class$=ContentPanel]')
    if contents.length > 0
      #Check date for the first record (all records nust sort by date)
      first_record = contents[0]
      tds = first_record.search('td')
      first_record_date = get_date_received(tds)
      if first_record_date >= @end_date
        result = true
      end  
    end
  end
  return result
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
  tds = da_container.search('td')
  record_date = get_date_received(tds)
  if record_date >= @end_date
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
    'date_received' => item_general_info[:date_received],
    'type_detail' => item_detail_info[:type_detail].to_json
  }
  
  item_detail_info[:property_detail].each do |item|
    da_summary[item[:key]] = item[:field]
  end
  
  item_detail_info[:app_detail].each do |item|
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
  item_detail_info[:app_detail] = get_app_detail(detail_page)
  item_detail_info[:property_detail] = get_property_detail(detail_page)
  item_detail_info[:type_detail] = get_type_detail(detail_page)
  return item_detail_info
end

def get_app_detail(detail_page)
  app_detail = []
  app_detail_heading = detail_page.search('.AlternateContentHeading')
  app_detail_content = detail_page.search('.AlternateContentText')
  if(app_detail_heading.size > 0 && app_detail_content.size > app_detail_heading.size)
    list_app_detail_key = []
    for i in 0..app_detail_heading.length-1
      list_app_detail_key << clean_whitespace(app_detail_heading[i].inner_text).gsub(" ","_").gsub(":","").gsub(".","").downcase
    end
    
    for i in 0..app_detail_content.length-1
      if(!list_app_detail_key[i].nil?)
        detail_obj = {}
        detail_obj[:key] = list_app_detail_key[i]
        detail_obj[:field] = clean_whitespace(app_detail_content[i+1].inner_text)
        
        app_detail << detail_obj
      end
    end
  end

  return app_detail
end

def get_property_detail(detail_page)
  detail = []
  table_content = detail_page.search('table.ContentPanel')
  if(table_content.size > 0)
    detail_table = table_content[0]
    detail_tr = detail_table.search('tr')
    if(detail_tr.size > 1)
      key_tr = detail_tr[0]
      list_key_th = key_tr.search('th')
      if(list_key_th.size > 0)
        list_key = []
        list_key_th.each do |item|
          list_key << clean_whitespace(item.inner_text).gsub(" ","_").gsub(":","").gsub(".","").downcase
        end

        info_tr = detail_tr[1]
        list_info_td = info_tr.search('td')
        for i in 0..list_key.length-1
          detail_obj = {}
          detail_obj[:key] = list_key[i]
          detail_obj[:field] = clean_whitespace(list_info_td[i].inner_text)

          detail << detail_obj
        end
      end
    end
  end
  
  return detail
end

def get_type_detail(detail_page)
  detail = []
  table_content = detail_page.search('table.ContentPanel')
  if(table_content.size > 1)
    detail_table = table_content[1]
    detail_tr = detail_table.search('tr')
    if(detail_tr.size > 1)
      key_tr = detail_tr[0]
      list_key_th = key_tr.search('th')
      if(list_key_th.size > 0)
        list_key = []
        list_key_th.each do |item|
          list_key << clean_whitespace(item.inner_text).gsub(" ","_").gsub(":","").gsub(".","").downcase
        end
                 
        for i in 1..detail_tr.length-1
          one_detail = []
          list_info_td = detail_tr[i].search('td')
          for i in 0..list_key.length-1
            detail_obj = {}
            detail_obj[:key] = list_key[i]
            detail_obj[:field] = clean_whitespace(list_info_td[i].inner_text)
  
            one_detail << detail_obj
          end
          detail << one_detail
        end
      end
    end
  end
  
  return detail
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
  return clean_whitespace(tds[0].at('a').inner_text)
end
##
#get_date_received
#Parameters::
# *(tag) *params*:da_container tag
#Return:: date_received
#*Author*::
#----------------------------------------------------------------------------
def get_date_received(tds)
  return Date.strptime(clean_whitespace(tds[1].at('span').text), '%d/%m/%Y')
end
##
#get_comment_url
#Parameters::
# *(tag) *params*:da_container tag
#Return:: comment_url
#*Author*::
#----------------------------------------------------------------------------
def get_comment_url(tds)
  return COMMENT_URL_PREFIX + CGI::escape("Development Application Enquiry: " + tds[0].at('a').text)
end
##
#get_info_url
#Parameters::
# *(tag) *params*:da_container tag
#Return:: info_url
#*Author*::
#----------------------------------------------------------------------------
def get_info_url(page, tds)
  return (page.uri + tds[0].at('a')['href']).to_s
end
##
#get_address
#Parameters::
# *(tag) *params*:da_container tag
#Return:: address
#*Author*::
#----------------------------------------------------------------------------
def get_address(tds)
  return clean_whitespace(tds[2].at('span').text)
end
##
#get_description
#Parameters::
# *(tag) *params*:da_container tag
#Return:: description
#*Author*::
#----------------------------------------------------------------------------
def get_description(detail_page, tds)
  return CGI::unescapeHTML(clean_whitespace(tds[3].at('span').text))
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

#
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
  #if ScraperWiki.select("* from swdata where council_reference = '#{record['council_reference']}'").empty?
    ScraperWiki.save_sqlite(['council_reference'], record)
  #else
    #puts "Skipping already saved record " + record['council_reference']
  #end
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
page = @agent.get(STARTING_URL_SORTED)
#Initiate global variable @index
@index = 1  
#Assign global variable @url
@url = page.uri
create_initial_table_in_database
get_all_das(page)
###############################################################################################
# The code to test will start running here
###############################################################################################
