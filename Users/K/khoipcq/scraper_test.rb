# This scraper is to scrape the summary of all Development Applications for Armidale Dumaresq Council
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
#    Example: '2013-01-18'
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
STARTING_URL = 'https://epathway.newengland.nsw.gov.au/ePathway/Production/Web/GeneralEnquiry/EnquiryLists.aspx'
# COMMENT_URL_PREFIX: The prefix of the URL where users can provide a response to the council about a particular Development Application.
# That URL needs to be a persistent URL and should be specific to a particular Development Application if possible.
# Email mailto links are also valid in this field.
COMMENT_URL_PREFIX = 'mailto:council@armidale.nsw.gov.au?subject='
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
  next_page_condition = page.search('input[id$=ctl00_MainBodyContent_mNextButton]')
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
#Return:: The Development Application which contains the list of fields as described on the top of this source file
#*Author*::
#----------------------------------------------------------------------------
def get_da_summary(page, da_container, detail_page)
  #get info by list item page
  item_general_info = get_item_general_info(page, da_container)
  
  #get info by item detail page
  item_detail_info= get_item_detail_info(detail_page)
  da_summary = {
    'info_url' => item_general_info[:info_url],
    'comment_url' => item_general_info[:comment_url],
    'council_reference' => item_general_info[:council_reference],
    'address' => item_general_info[:address],
    'description' => item_general_info[:description],
    'date_scraped' => item_general_info[:date_scraped],
    'status' => item_detail_info[:status],
    
    'responsible_officer_name' => item_detail_info[:responsible_officer_name].to_json,
    
    'responsible_officer_property' => item_detail_info[:responsible_officer_property].to_json
    
  }
  
  return da_summary
end
##
#get_item_general_info
#Parameters::
# *(tag) *params*: page, da_container
#Return:: item general info
#*Author*::
#----------------------------------------------------------------------------
def get_item_general_info(page, da_container)
  #get td item that contains detail general info
  tds = da_container.search('td')
  
  item_general_info = {}
  
  item_general_info[:info_url] = get_info_url(page, tds)
  item_general_info[:council_reference] = get_council_reference(tds)
  item_general_info[:comment_url] = get_comment_url(tds)
  item_general_info[:address] = get_address(tds)
  item_general_info[:description] = get_description(tds)
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
  return tds[0].at('a').text
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
  return clean_whitespace(tds[1].at('div').text)
end
##
#get_description
#Parameters::
# *(tag) *params*:da_container tag
#Return:: description
#*Author*::
#----------------------------------------------------------------------------
def get_description(tds)
  return CGI::unescapeHTML(clean_whitespace(tds[2].at('div').text))
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
#get_item_detail_info
#Parameters::
# *(tag) *params*: detail_page
#Return:: item detail info
#*Author*::
#----------------------------------------------------------------------------
def get_item_detail_info(detail_page)
  item_detail_info = {}
  
  #get detail info by approciate syn_fieldsetItem
  item_detail_info[:status] = get_status(detail_page)
  item_detail_info[:responsible_officer_name] = get_responsible_officer_name(detail_page)
  item_detail_info[:responsible_officer_property] = get_responsible_officer_property(detail_page)
  
  return item_detail_info
end
##
#get_status
#Parameters::
# *(tag) *params*: detail_page
#Return:: item status
#*Author*::
#----------------------------------------------------------------------------
def get_status(detail_page)
  status = ""
  status_content = detail_page.search('.AlternateContentText')
  if (status_content.size > 3)
    status = status_content[3].inner_text
  end
  
  return status
end
##
#get_responsible_officer_name
#Parameters::
# *(tag) *params*: detail_page
#Return:: list responsible officer name
#*Author*::
#----------------------------------------------------------------------------
def get_responsible_officer_name(detail_page)
  responsible_officer_name = []
  
  responsible_officer_name_panel = detail_page.search('table.ContentPanel')
  if(responsible_officer_name_panel.size > 0)
    responsible_officer_name_panel = responsible_officer_name_panel[0]
    responsible_officer_name_tr = responsible_officer_name_panel.search('tr')
    if (responsible_officer_name_tr.size > 1)
      for i in 1..responsible_officer_name_tr.length-1
        responsible_officer_name_object = {}
        responsible_officer_name_object[:name_role_type] = ""
        responsible_officer_name_object[:name] = ""
        responsible_officer_name_object[:postal_address] = ""
        
        responsible_officer_name_td = responsible_officer_name_tr[i].search('td')
        if (responsible_officer_name_td.size > 0)
          responsible_officer_name_object[:name_role_type] = responsible_officer_name_td[0].inner_text
        end
        if (responsible_officer_name_td.size > 1)
          responsible_officer_name_object[:name] = responsible_officer_name_td[1].inner_text
        end
        if (responsible_officer_name_td.size > 2)
          responsible_officer_name_object[:postal_address] = responsible_officer_name_td[2].inner_text
        end
        
        responsible_officer_name << responsible_officer_name_object
      end
    end
  end
  
  return responsible_officer_name
end
##
#get_responsible_officer_property
#Parameters::
# *(tag) *params*: detail_page
#Return:: list responsible officer property
#*Author*::
#----------------------------------------------------------------------------
def get_responsible_officer_property(detail_page)
  responsible_officer_property = []
  responsible_officer_property_panel = detail_page.search('table.ContentPanel')
  if (responsible_officer_property_panel.size > 1)
    responsible_officer_property_panel = responsible_officer_property_panel[1]
    responsible_officer_property_tr = responsible_officer_property_panel.search('tr')
    if (responsible_officer_property_tr.size > 1)
      for i in 1..responsible_officer_property_tr.length-1
        responsible_officer_property_object = {}
        responsible_officer_property_object[:property_address] = ""
        
        responsible_officer_property_td = responsible_officer_property_tr[i].search('td')
        if (responsible_officer_property_td.size > 0)
          responsible_officer_property_object[:property_address] = responsible_officer_property_td[0].inner_text
        end
        
        responsible_officer_property << responsible_officer_property_object
      end
    end
  end
  
  return responsible_officer_property
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
    ScraperWiki.sqliteexecute("CREATE TABLE 'swdata' ('date_scraped' text, 'description' text, 'info_url' text, 'council_reference' text, 'address' text, 'comment_url' text, 'page_content' text, 'status' text, 'responsible_officer_name' text, 'responsible_officer_property' text)");
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
  #if ScraperWiki.select("* from swdata where 'council_reference'='#{record['council_reference']}'").empty?
  #  ScraperWiki.save_sqlite(['council_reference'], record)
  #else
  #  puts "Skipping already saved record " + record['council_reference']
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
  iterator_from_date = (Date.today - PERIOD_DATE).strftime("%d/%m/%Y")
  today = Date.today.strftime("%d/%m/%Y")
  first_page_form = page.forms.first
  first_page_form.radiobuttons[3].click
  page = first_page_form.click_button
  second_page_form = page.forms.first
  second_page_form.add_field!('__EVENTTARGET','ctl00$MainBodyContent$mGeneralEnquirySearchControl$mSearchTabStrip')
  second_page_form.add_field!('__EVENTARGUMENT','2')
  p "LLLLLLLLLLLLLLLL"
  p second_page_form
  second_page_form.field_with(:name => /SearchTabStrip_State/).value = "2"
  p "KKKKKKKKKKKKKKKKKKK"
  p second_page_form
  second_page_address_search_tab = second_page_form.submit
  form_search = second_page_address_search_tab.forms.first
  form_search.field_with(:name => "ctl00$MainBodyContent$mGeneralEnquirySearchControl$ctl14$mDateFromTextBox$dateTextBox").value = iterator_from_date
  form_search.field_with(:name => "ctl00$MainBodyContent$mGeneralEnquirySearchControl$ctl14$mDateToTextBox$dateTextBox").value = today
  page = second_page_address_search_tab.forms.first.submit(second_page_address_search_tab.forms.first.button_with(:value => "Search"))
  
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
#Create global variable @agent
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