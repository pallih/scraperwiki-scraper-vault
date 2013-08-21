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
STARTING_URL = 'easy.co.il'

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

  page.search('table tbody tr').each do |merchant_container|
    get_merchant_info(merchant_container)
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
end

##
#get_merchant_info

#Parameters::
# *(merchant_container) *params*: merchant_container
#Return:: The merchant information which contains the list of fields as described on the top of this source file
#*Author*::
#----------------------------------------------------------------------------
def get_merchant_info(merchant_container)
  # merchant_container is expected to be with ??? piece of information

  # 0. info_url
  # 1. 
  # 2. 
  # 3. 
  # 4. 
  # 5. 

  # Todo: Put your code to process the merchant_container to get the merchant_info here

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


##
#----------------------------------------------------------------------------
#rotate_proxy
#Return:: The IP of the current machine to scrape merchants will be printed out
#*Author*::
#----------------------------------------------------------------------------
def rotate_proxy()
  # Returned value: "ROTATE:proxy.seo-proxies.com:39800:68.71.149.154"
  @agent.get("http://seo-proxies.com/api.php?api=1&uid=6633&pwd=1140f2ab99b7967698f8f68c807250f2&cmd=rotate")
end









###############################################################################################
# End of helper functions section
###############################################################################################



###############################################################################################
# The code to scrape will start running here
###############################################################################################

@agent = Mechanize.new

#Equip ourselves with a proxy
@agent.set_proxy("proxy.seo-proxies.com", 39800)

page = @agent.get(STARTING_URL)

get_all_merchants(page)

