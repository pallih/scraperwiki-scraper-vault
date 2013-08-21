# This scraper is to scrape all merchants information from easy.co.il
# The information for each merchant includes:

# 1. To be listed here

#    Example: To be listed here

# 2. To be listed here

#    Example: To be listed here

# 3. To be listed here

#    Example: To be listed here

# 4. To be listed here

#    Example: To be listed here

# 5. To be listed here

#    Example: To be listed here

# 6. To be listed here

#    Example: To be listed here

# History: January 09, 2013
# By nhuanvn

# Required libraries

require 'rubygems'
require 'mechanize'

# The starting URL to get merchants from

# Todo: Change the STARTING_URL to reflect your work
#GET_ALL_INFO_STARTING_URL = 'http://www.alexa.com/topsites/category/Top/Regional/North_America/United_States'
#STARTING_URL = 'http://www.alexa.com/topsites/category/Top/Regional/North_America/United_States/Alabama/Education/K-12/School_Districts'
STARTING_URL = 'http://www.alexa.com/topsites/category/Top/Regional/North_America/United_States/Alabama/Arts_and_Entertainment/Libraries/Public'

##
#get_all_merchants
#Parameters::
# *(Page) *params*:page
#Return:: All merchants
#*Author*::
#----------------------------------------------------------------------------
def get_all_merchants(page)
  while (is_available(page)) do
    get_all_merchants_in_page(page)
    page = get_next_page(page)
  end
end


##
#is_available
#Parameters::
# *(Page) *params*:page
#Return:: Return true if the page is available for scraping merchants. Return false otherwise
#*Author*::
#----------------------------------------------------------------------------
def is_available(page)
  # Todo: Return true if the page is available for scraping merchants. Return false otherwise
  #listSubCatUl = page.search('#catList .categories ul')

  #return listSubCatUl.size > 0 ? false : true 
  return !page.nil? 
end

##
#get_all_merchants_in_page

#Parameters::
# *(Page) *params*:page
#Return:: list of merchants in page
#*Author*::
#----------------------------------------------------------------------------
def get_all_merchants_in_page(page)
  # The trick is that before you issue a HTTP request, you MUST rotate_proxy first
  # Todo: For each element of the page that contains the merchant, get that merchant's information.
  # For example:
  breadcrumbs = page.search('#breadcrumbs a')
  breadcrumbsSize = breadcrumbs.size
  state = breadcrumbsSize >= 5 ? breadcrumbs[4].inner_text : ""
  catName = breadcrumbs[breadcrumbsSize-1].inner_text
  page.search('.site-listing').each do |merchant_container|
    merchantInfo = get_merchant_info(merchant_container, page)
    result_record = {
      'global_rank' => merchantInfo['global_rank'],
      'us_rank' => merchantInfo['us_rank'],
      'company_name' => merchantInfo['company_name'],
      'domain' => merchantInfo['domain'],
      'description' => merchantInfo['description'],
      'category_name' => catName,
      'state' => state
    }
    puts result_record
  end
end

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
  # The trick is that before you issue a HTTP request, you MUST rotate_proxy first
  # Todo: Put your code here to get the next page to be scraped

  if has_next_page(page)
    link = get_next_url()
    p "==>" + link.to_s
    
    page = @agent.get(link)
    return page
  else
    return nil
  end
end

##
#get_merchant_info

#Parameters::
# *(merchant_container) *params*: merchant_container
#Return:: The merchant information which contains the list of fields as described on the top of this source file
#*Author*::
#----------------------------------------------------------------------------
def get_merchant_info(merchant_container, page)
  # merchant_container is expected to be with ??? piece of information

  # 0. info_url
  # 1. 
  # 2. 
  # 3. 
  # 4. 
  # 5. 

  # Todo: Put your code to process the merchant_container to get the merchant_info here
  
  container = merchant_container.search('.desc-container')[0]
  company_name = container.at('h2').inner_text
  domain = container.at('span').inner_text
  description = container.search('.description')[0]
  if description.search('.truncate').size > 0
    description = description.inner_text.gsub('... More','')
  else
    description = description.inner_text
  end
  
  detail_url = "/siteinfo/" + domain
  
  detail_page = page.link_with(:href => detail_url).click
  global_rank_container = detail_page.search('#siteStats tbody td')[0]
  if global_rank_container.nil? 
    detail_url = @url + detail_url 
    detail_page = @agent.get(detail_url )
    global_rank_container = detail_page.search('#siteStats tbody td')[0]
  end
  
  puts detail_page.body

  global_rank = clean_whitespace(global_rank_container.at('div').inner_text)
  
  us_rank_container = detail_page.search('#siteStats tbody td')[1]
  if us_rank_container.at('div').nil? 
    us_rank_container = detail_page.search('#siteStats tbody td')[2]
  end
  us_rank = clean_whitespace(us_rank_container.at('div').inner_text)
  record = {
    'global_rank' => global_rank,
    'us_rank' => us_rank,
    'company_name' => company_name,
    'domain' => domain,
    'description' => description
  }
  
  return record  
end


###############################################################################################
# Start of helper functions section
###############################################################################################

##
#----------------------------------------------------------------------------
#clean_whitespace
#Parameters::
# *(tag) *params*: a tag
#Return::a tag
#*Author*::
#----------------------------------------------------------------------------
def clean_whitespace(a)
  a.gsub("\r", ' ').gsub("\n", ' ').squeeze(" ").strip
end

##
#----------------------------------------------------------------------------
#print_ip
#Return:: The IP of the current machine to scrape merchants will be printed out
#*Author*::
#----------------------------------------------------------------------------
def print_ip()
  puts @agent.get("http://squabbel.com/ipxx.php").body.to_s
end


###############################################################################################
# End of helper functions section
###############################################################################################

def recursive_sub_category(page)
  listSubCatUl = page.search('#catList .categories ul')
  if listSubCatUl.size > 0
    listSubCatUl.each do |itemUl|
      listSubCatLi = itemUl.search('li')
      listSubCatLi.each do |itemLi|
        linkSubCat = itemLi.at('a')['href'].to_s
        linkSubCat = @url + linkSubCat
        page = @agent.get(linkSubCat)
        recursive_sub_category(page)
      end
    end
  else
    get_all_merchants(page)
  end
end

###############################################################################################
# The code to scrape will start running here
###############################################################################################

@agent = Mechanize.new

@url = "http://www.alexa.com"

page = @agent.get(STARTING_URL)

get_all_merchants_in_page(page)

#recursive_sub_category(page)

