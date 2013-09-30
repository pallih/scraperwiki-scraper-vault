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
require 'scraperwiki'
require 'rubygems'
require 'mechanize'
require 'pdf-reader'   
require 'open-uri'
require 'active_support'

# The starting URL to get Development Applications from

# Todo: Change the STARTING_URL to reflect your work
STARTING_URL = 'http://www.wattlerange.sa.gov.au/page.aspx?u=1009'
HOME_URL = 'http://www.wattlerange.sa.gov.au'
# COMMENT_URL_PREFIX: The prefix of the URL where users can provide a response to the council about a particular Development Application.
# That URL needs to be a persistent URL and should be specific to a particular Development Application if possible.
# Email mailto links are also valid in this field.

# Todo: Change the COMMENT_URL_PREFIX to reflect your work
COMMENT_URL_PREFIX = 'mailto:council@wattlerange.sa.gov.au?subject='

##
#get_data

#Parameters::
# *(tag) *params*:da_container tag
#Return:: Get data: council_reference, address, description, info_url, comment_url, date_scraped
#*Author*::
#----------------------------------------------------------------------------
def get_data(pdf_link, p_item)
  p "KKKKKKKKKKKKKKKKKKK"
  p p_item
  app_index = (p_item.index("Application Date") != nil) ? p_item.index("Application Date") : p_item.index("ApplicationDate")
  lda_index = (p_item.index("Land Division Approval") != nil) ? p_item.index("Land Division Approval") : ((p_item.index("LandDivision Approval") != nil) ? p_item.index("LandDivision Approval") : p_item.index("Land DivisionApproval")) 
  relevant_index = (p_item.index("RelevantAuthorityCNC") != nil) ?  (p_item.index("RelevantAuthorityCNC") + "RelevantAuthorityCNC".length) : p_item.index("RelevantAuthority") + "RelevantAuthority".length
  result = {
    'council_reference' => p_item[0,app_index].strip,
    'address' => p_item[p_item.index("Applicants Address") + "Applicants Address".length, lda_index - (p_item.index("Applicants Address") + "Applicants Address".length)].strip,
    'description' => p_item[relevant_index, p_item.index("Referredto") - (relevant_index)],
    'info_url' => pdf_link,
    'comment_url' => COMMENT_URL_PREFIX + CGI::escape("Development Application Enquiry: " + p_item[0,app_index].strip),
    'date_scraped' => Date.today.to_s
  }
end


##
#get_da_summary

#Parameters::
# *(tag) *params*:da_container tag
#Return:: The Development Application Summary which contains the list of fields as described on the top of this source file
#*Author*::
#----------------------------------------------------------------------------
def get_da_summary(pdf_link, da_container)
  # Todo: Put your code to process the da_container to get the Development Application Summary here
  
  result = {}
  (1..da_container.length - 1).each do |i|
    p_item = da_container[i]
    sleep(3)
    if p_item
      result = get_data(pdf_link, p_item)
      #if ScraperWiki.select("* from swdata where `council_reference`='#{result['council_reference']}'").empty? 
        ScraperWiki.save_sqlite(['council_reference'], result)
        p result, i
      #else
      #  puts "Skipping already saved record " + result['council_reference']
      #end
    end
  end
 
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


##########  This section contains the callback code that processes the PDF file contents  ######
class PageTextReceiver
  attr_accessor :content, :page_counter
  def initialize
    @content = []
    @page_counter = 0
  end
  # Called when page parsing starts
  def begin_page(arg = nil)
    @page_counter += 1
    @content << ""
  end
  # record text that is drawn on the page
  def show_text(string, *params)
    @content.last << string
  end
  # there's a few text callbacks, so make sure we process them all
  alias :super_show_text :show_text
  alias :move_to_next_line_and_show_text :show_text
  alias :set_spacing_next_line_show_text :show_text

  # this final text callback takes slightly different arguments
  def show_text_with_positioning(array, *params)
    show_text(array.select{|i| i.is_a?(String)}.join(""), params)
    #params = params.first
    #params.each { |str| 
    #sleep(1) 
    #show_text(str) if str.kind_of?(String)}
  end
end
################  End of TextReceiver #############################
def get_data_from_pdf_link(pdf_link)
  p "UUUUUUUUUUUUU"  
  pdf = open(pdf_link)
  p "1"
  #######  Instantiate the receiver and the reader
  receiver = PageTextReceiver.new
  p "2"
  pdf_reader = PDF::Reader.new
  p "3"
  #######  Now you just need to make the call to parse...
  pdf_reader.parse(pdf, receiver)
  my_data = receiver.content.join(" ").gsub("\u00A0", " ").gsub("\u2010", " ").split("Application No")
  p "4"
  #######  ...and do whatever you want with the text.  
  #######  This just outputs it.
  #get_da_summary(pdf_link, my_data)
  
end

def get_data_link()
  begin
    @index = ScraperWiki.get_var('link_index')
    p "KKKKKKKKKKK"
    p @index
    p @a_links[@index]
    pdf_link = (HOME_URL + @a_links[@index][:href])
    page = @agent.get(STARTING_URL)
    get_data_from_pdf_link(pdf_link)    
    ScraperWiki.save_var('link_index', @index + 1 )
    if (@index + 1) < @a_links.length
      get_data_link()
    end
  rescue Exception => ex
    if ex.message.match('CPU')
      ScraperWiki.save_var('link_index', @index)
      sleep(2)
      get_data_link()
    else
      puts "Error, unexpected exception"
    end
  end 
end

#Start running
@agent = Mechanize.new{|a|
  a.ssl_version,
  a.verify_mode = 'SSLv3',
  OpenSSL::SSL::VERIFY_NONE,
  Net::HTTP::Persistent,
  a.idle_timeout = 1000000000,
  a.open_timeout = 1000000000,
  a.read_timeout = 1000000000,
  a.user_agent_alias = 'Linux Firefox'
}
@agent.max_history = 0 
page = @agent.get(STARTING_URL)

if ScraperWiki.show_tables()["swdata"] == nil
  ScraperWiki.sqliteexecute("CREATE TABLE 'swdata' ('date_scraped' text, 'description' text, 'info_url' text, 'council_reference' text, 'address' text, 'comment_url' text)")
end
@a_links = page.search('div[class$=unityHtmlArticle] div a')
@data = []

p "IIIIIIIIIIII"
ScraperWiki.save_var('link_index', 0)
@index = 0
get_data_link()
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
require 'scraperwiki'
require 'rubygems'
require 'mechanize'
require 'pdf-reader'   
require 'open-uri'
require 'active_support'

# The starting URL to get Development Applications from

# Todo: Change the STARTING_URL to reflect your work
STARTING_URL = 'http://www.wattlerange.sa.gov.au/page.aspx?u=1009'
HOME_URL = 'http://www.wattlerange.sa.gov.au'
# COMMENT_URL_PREFIX: The prefix of the URL where users can provide a response to the council about a particular Development Application.
# That URL needs to be a persistent URL and should be specific to a particular Development Application if possible.
# Email mailto links are also valid in this field.

# Todo: Change the COMMENT_URL_PREFIX to reflect your work
COMMENT_URL_PREFIX = 'mailto:council@wattlerange.sa.gov.au?subject='

##
#get_data

#Parameters::
# *(tag) *params*:da_container tag
#Return:: Get data: council_reference, address, description, info_url, comment_url, date_scraped
#*Author*::
#----------------------------------------------------------------------------
def get_data(pdf_link, p_item)
  p "KKKKKKKKKKKKKKKKKKK"
  p p_item
  app_index = (p_item.index("Application Date") != nil) ? p_item.index("Application Date") : p_item.index("ApplicationDate")
  lda_index = (p_item.index("Land Division Approval") != nil) ? p_item.index("Land Division Approval") : ((p_item.index("LandDivision Approval") != nil) ? p_item.index("LandDivision Approval") : p_item.index("Land DivisionApproval")) 
  relevant_index = (p_item.index("RelevantAuthorityCNC") != nil) ?  (p_item.index("RelevantAuthorityCNC") + "RelevantAuthorityCNC".length) : p_item.index("RelevantAuthority") + "RelevantAuthority".length
  result = {
    'council_reference' => p_item[0,app_index].strip,
    'address' => p_item[p_item.index("Applicants Address") + "Applicants Address".length, lda_index - (p_item.index("Applicants Address") + "Applicants Address".length)].strip,
    'description' => p_item[relevant_index, p_item.index("Referredto") - (relevant_index)],
    'info_url' => pdf_link,
    'comment_url' => COMMENT_URL_PREFIX + CGI::escape("Development Application Enquiry: " + p_item[0,app_index].strip),
    'date_scraped' => Date.today.to_s
  }
end


##
#get_da_summary

#Parameters::
# *(tag) *params*:da_container tag
#Return:: The Development Application Summary which contains the list of fields as described on the top of this source file
#*Author*::
#----------------------------------------------------------------------------
def get_da_summary(pdf_link, da_container)
  # Todo: Put your code to process the da_container to get the Development Application Summary here
  
  result = {}
  (1..da_container.length - 1).each do |i|
    p_item = da_container[i]
    sleep(3)
    if p_item
      result = get_data(pdf_link, p_item)
      #if ScraperWiki.select("* from swdata where `council_reference`='#{result['council_reference']}'").empty? 
        ScraperWiki.save_sqlite(['council_reference'], result)
        p result, i
      #else
      #  puts "Skipping already saved record " + result['council_reference']
      #end
    end
  end
 
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


##########  This section contains the callback code that processes the PDF file contents  ######
class PageTextReceiver
  attr_accessor :content, :page_counter
  def initialize
    @content = []
    @page_counter = 0
  end
  # Called when page parsing starts
  def begin_page(arg = nil)
    @page_counter += 1
    @content << ""
  end
  # record text that is drawn on the page
  def show_text(string, *params)
    @content.last << string
  end
  # there's a few text callbacks, so make sure we process them all
  alias :super_show_text :show_text
  alias :move_to_next_line_and_show_text :show_text
  alias :set_spacing_next_line_show_text :show_text

  # this final text callback takes slightly different arguments
  def show_text_with_positioning(array, *params)
    show_text(array.select{|i| i.is_a?(String)}.join(""), params)
    #params = params.first
    #params.each { |str| 
    #sleep(1) 
    #show_text(str) if str.kind_of?(String)}
  end
end
################  End of TextReceiver #############################
def get_data_from_pdf_link(pdf_link)
  p "UUUUUUUUUUUUU"  
  pdf = open(pdf_link)
  p "1"
  #######  Instantiate the receiver and the reader
  receiver = PageTextReceiver.new
  p "2"
  pdf_reader = PDF::Reader.new
  p "3"
  #######  Now you just need to make the call to parse...
  pdf_reader.parse(pdf, receiver)
  my_data = receiver.content.join(" ").gsub("\u00A0", " ").gsub("\u2010", " ").split("Application No")
  p "4"
  #######  ...and do whatever you want with the text.  
  #######  This just outputs it.
  #get_da_summary(pdf_link, my_data)
  
end

def get_data_link()
  begin
    @index = ScraperWiki.get_var('link_index')
    p "KKKKKKKKKKK"
    p @index
    p @a_links[@index]
    pdf_link = (HOME_URL + @a_links[@index][:href])
    page = @agent.get(STARTING_URL)
    get_data_from_pdf_link(pdf_link)    
    ScraperWiki.save_var('link_index', @index + 1 )
    if (@index + 1) < @a_links.length
      get_data_link()
    end
  rescue Exception => ex
    if ex.message.match('CPU')
      ScraperWiki.save_var('link_index', @index)
      sleep(2)
      get_data_link()
    else
      puts "Error, unexpected exception"
    end
  end 
end

#Start running
@agent = Mechanize.new{|a|
  a.ssl_version,
  a.verify_mode = 'SSLv3',
  OpenSSL::SSL::VERIFY_NONE,
  Net::HTTP::Persistent,
  a.idle_timeout = 1000000000,
  a.open_timeout = 1000000000,
  a.read_timeout = 1000000000,
  a.user_agent_alias = 'Linux Firefox'
}
@agent.max_history = 0 
page = @agent.get(STARTING_URL)

if ScraperWiki.show_tables()["swdata"] == nil
  ScraperWiki.sqliteexecute("CREATE TABLE 'swdata' ('date_scraped' text, 'description' text, 'info_url' text, 'council_reference' text, 'address' text, 'comment_url' text)")
end
@a_links = page.search('div[class$=unityHtmlArticle] div a')
@data = []

p "IIIIIIIIIIII"
ScraperWiki.save_var('link_index', 0)
@index = 0
get_data_link()
