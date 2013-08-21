# This scraper is to scrape all car information from craiglist.com
# The information for each car includes:

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

# History: January 08, 2013
# By nhuanvn

# Required libraries

require 'rubygems'
require 'mechanize'
require 'sanitize'
require 'nokogiri'
require 'open-uri'

# The starting URL to get cars from

# Todo: Change the STARTING_URL to reflect your work
STARTING_URL = 'http://sfbay.craigslist.org/eby/cto/'

# some hash for checking ----------------------------
PHONE_PATTERNS = [/\(?\+?\d{2,3}\)?[-. ]?\d{3}[-. ]?\d{4}/]
EMAIL_PATTERN  = /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b/i
PRICE_PATTERNS = [/\$\s*\d+/,/asking\s*\d+/,/pay\s*\d+/,/\s*\$?\s*\d+/,/\$?\d+[-. ]*\$\d+/,
                  /\$?\d+[-. ]*\$\d+/,/\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$/,
                  /\d+[-. ]*\$\d+/,/\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])? obo/] 
YEAR_PATTERNS   = [/[^$]?[12][0-9]{3} /,/\'\s?[0-9]{2}\'? /,/ \s?[0-9]{2}\'/]

# some global variables ------------------------------
@list_locations = []
PRICE_RANGE     = 900..30000

##
#get_all_cars
#Parameters::
# *(Page) *params*:page
#Return:: All cars
#*Author*::
#----------------------------------------------------------------------------
def get_all_cars(page)
  while (is_available(page)) do
    get_all_cars_in_page(page)
    page = get_next_page(page)
  end
end


##
#is_available
#Parameters::
# *(Page) *params*:page
#Return:: Return true if the page is available for scraping cars. Return false otherwise
#*Author*::
#----------------------------------------------------------------------------
def is_available(page)
  # Todo: Return true if the page is available for scraping cars. Return false otherwise

  # return true if page is not null and contains rows
  unless page.nil? 
    return page.search('.row a').count > 0
  end

  return false
end

##
#get_all_cars_in_page

#Parameters::
# *(Page) *params*:page
#Return:: list of cars in page
#*Author*::
#----------------------------------------------------------------------------
def get_all_cars_in_page(page)
  # Todo: For each element of the page that contains the car, get that car's information.
  # For example:

  page.search('.row a').each do |car_container_link|
    car_container = @agent.get(car_container_link[:href])
    p "==>" + car_container_link[:href]
    car_info = get_car_info(car_container)
    save_to_db(car_info)
  end
end

def save_to_db info
  info.each{|key, value|
    #p "-->" + key.to_s
    if value.kind_of?(Hash)
      #p value[:value].to_s + "-" + value[:CF].to_s
    else
      #p value
    end
  }
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
  
  # get href for next_page link
  next_page_link = page.search('p#nextpage a').first
  unless next_page_link.nil? 
    return @agent.get(next_page_link[:href])
  end

  return nil
end

##
#get_car_info

#Parameters::
# *(car_container) *params*:car_container
#Return:: The car information which contains the list of fields as described on the top of this source file
#*Author*::
#----------------------------------------------------------------------------
def get_car_info(car_container)
  # car_container is expected to be with 6 piece of information

  # 0. info_url
  # 1. Date / Time
  # 2. Seller's Email Address
  # 3. Location Prefix
  # 4. Title of the advertisement
  # 5. Advertisement's content

  # get some global variables
  @title = get_title(car_container)
  @content =  get_content(car_container)

  # Todo: Put your code to process the car_container to get the car_info here
  car_info = {}
  car_info[:info_url]        = get_info_url(car_container)
  car_info[:seller_datetime] = get_seller_datetime(car_container)
  car_info[:seller_email]    = get_seller_email(car_container)
  car_info[:location]        = get_location(car_container)
  car_info[:seller_phone]    = get_seller_phone(car_container)
  
  car_info[:year]            = get_year(car_container)
  car_info[:make]            = get_make(car_container)
  car_info[:model]           = get_model(car_container)
  car_info[:trim]            = get_trim(car_container)
  car_info[:miles]           = get_miles(car_container)
  car_info[:price]           = get_price(car_container)

  car_info[:one_owner]       = get_one_owner(car_container)
  car_info[:clean_title]     = get_clean_title(car_container)
  car_info[:clean_carfax]    = get_clean_carfax(car_container)
  car_info[:vin_number]      = get_vin_number(car_container)

  car_info[:engine_size]     = get_engine_size(car_container)
  car_info[:automatic]       = get_automatic(car_container)
  car_info[:wd]              = get_wd(car_container)
  car_info[:moonroof]        = get_moonroof(car_container)
  car_info[:cloth_leather]   = get_cloth_leather(car_container)

  # p car_inf
  return car_info

end


##
#get_price
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_title(car_container)
  # Todo: Put your code here to get the price of the car
  title_node = car_container.search('.postingtitle').first()
  unless title_node.nil? 
    return title_node.inner_text
  end

  return ""
end

##
#get_price
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_content(car_container)
  # Todo: Put your code here to get the price of the car
  text_node = car_container.search('#userbody').first()
  unless text_node.nil? 
    return CGI::unescapeHTML(Sanitize.clean(text_node.inner_text))
  end

  return ""
end

##
#get_price
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_price(car_container)
  # Todo: Put your code here to get the price of the car
  
  return ""
end

##
#get_price
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_info_url(car_container)
  # Todo: Put your code here to get the price of the car
  return car_container.uri.to_s
end

##
#get_price
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_seller_datetime(car_container)
  # Todo: Put your code here to get the price of the car
  date_node = car_container.search('.postingdate').first()
  unless date_node.nil? 
    return date_node.at('time').inner_text
  end

  return ""
end

##
#get_seller_email
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_seller_email(car_container)
  # Todo: Put your code here to get the price of the car
  email_node = car_container.search('.dateReplyBar small a').first()
  unless email_node.nil? 
    return email_node.inner_text
  else 
    return @content.scan(EMAIL_PATTERN).join(", ")
  end

  return ""
end

##
#get_location
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_location(car_container)
  # Todo: Put your code here to get the price of the car
  value = ""
  cf    = 0

  location_prefixs = car_container.search('.bchead a')
  location_prefix  = location_prefixs[1].inner_text + " > " + location_prefixs[2].inner_text

  start_index = @title.rindex("(")
  end_index   = @title.rindex(")")
  if(start_index && end_index) 
     value = @title[start_index+1,end_index-start_index-1].strip
     cf    = @list_locations.include?(value.downcase) ?  100 : 80 
  end

  return {
    :value => location_prefix + " > " + value,
    :CF    => cf
  }
end

##
#get_seller_phone
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_seller_phone(car_container)
  # Todo: Put your code here to get the price of the car
  list= []
  PHONE_PATTERNS.each {|partern|
      @content.scan(partern).each {|item|
         unless list.include?(item)
           list << format_phone(item)
         end
      }
  }
  return list.join(", ")
end

##
#get_year
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_year(car_container)
  # Todo: Put your code here to get the price of the car
  
  titles = @title.split('-')
  title = ""
  titles.each_with_index{|item,index|
    if index < titles.count-1
      title += item
    end
  }

  @title = title
  p title
  year = nil
  YEAR_PATTERNS.each {|pattern|
    unless validate_year(year)
      year = title.scan(pattern).first
    end
  }
  if year.nil? 
    YEAR_PATTERNS.each {|pattern|
      unless validate_year(year) 
        year = @content.scan(pattern).first
      end
    }
  end
  if year
      @title.gsub!(year,'') # remove
  end

  p @title
  p format_year(year)
  
  return year
end

def validate_year year
  return year && year.scan(/[$-&]/).count == 0
end

def format_year year
  if year
    year = year.gsub('\'','').strip
    if year.length == 2
      if year == '00'
        year = '2000'
      else
        year = '19' + year
      end
    end
  end
  return year
end

##
#get_make
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_make(car_container)
  # Todo: Put your code here to get the price of the car
  return ""
end

##
#get_model
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_model(car_container)
  # Todo: Put your code here to get the price of the car
  return ""
end

##
#get_trim
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_trim(car_container)
  # Todo: Put your code here to get the price of the car
  return ""
end

##
#get_miles
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_miles(car_container)
  # Todo: Put your code here to get the price of the car
  return ""
end

##
#get_price
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_price(car_container)
  # Todo: Put your code here to get the price of the car
  titles = @title.split('-')
  title  = titles[titles.count-1]

  list = []
  PRICE_PATTERNS.each {|partern|
      if title
        title.scan(partern).each {|item|
         if !list.include?(item) && !item.kind_of?(Array)
           list << {:price=>'$' + format_price(item),:CF=>rank_price(item,100)}
         end
      }
      end
      @content.scan(partern).each {|item|
         if !list.include?(item) && !item.kind_of?(Array)
           list << {:price=>'$' + format_price(item),:CF=>rank_price(item,80)}
         end
      }
  }

  list.sort! {|x,y| y[:CF] <=> x[:CF] }

  return list.first
end

def validate_price(value)
  return PRICE_RANGE.include?(value.to_f)
end

def format_price(price)
  return price.gsub("$","").gsub("pay","").gsub("asking","")
end

def rank_price(value,rank)
  unless PRICE_RANGE.include?(format_price(value).to_f) 
    return rank - 60
  end
  return rank
end

##
#get_one_owner
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_one_owner(car_container)
  # Todo: Put your code here to get the price of the car
  return ""
end

##
#get_clean_title
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_clean_title(car_container)
  # Todo: Put your code here to get the price of the car
  return ""
end

##
#get_clean_carfax
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_clean_carfax(car_container)
  # Todo: Put your code here to get the price of the car
  return ""
end

##
#get_vin_number
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_vin_number(car_container)
  # Todo: Put your code here to get the price of the car
  return ""
end

##
#get_engine_size
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_engine_size(car_container)
  # Todo: Put your code here to get the price of the car
  return ""
end

##
#get_automatic
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_automatic(car_container)
  # Todo: Put your code here to get the price of the car
  return ""
end

##
#get_wd
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_wd(car_container)
  # Todo: Put your code here to get the price of the car
  return ""
end

##
#get_moonroof
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_moonroof(car_container)
  # Todo: Put your code here to get the price of the car
  return ""
end

##
#get_cloth_leather
#Parameters::
# *(car_container) *params*: car_container
#Return:: the price of the car in text with format '$12,345', or -1 if no price found
#*Author*::
#----------------------------------------------------------------------------
def get_cloth_leather(car_container)
  # Todo: Put your code here to get the price of the car
  return ""
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

def clear_phone_format(a)
  return a.gsub(' ', '').gsub('-','').gsub('(','').gsub(')','').gsub('+','').strip
end

def format_phone(phone)
  phone = clear_phone_format(phone)
  length = phone.length
  phone.insert(length-4,'-')
  phone.insert(length-7,'-')
end

def get_list_of_locations(page)
  page.search('#hoodpicker option').each {|item|
    @list_locations << item.inner_text.strip.downcase
  }
end

###############################################################################################
# End of helper functions section
###############################################################################################



###############################################################################################
# The code to scrape will start running here
###############################################################################################

@agent = Mechanize.new
string = "1964 impala"
string = string.gsub(" ","%20")
search = "http://www.cardomain.com/cars/?key=#{string}&showflags=1"

page = @agent.get(search)
p page

link= page.search('div.resultsColumn a').first[:href]
page = @agent.get(link)
list = page.search(".breadcrumbs a")
p list[1].text
p list[2].text
p list[3].text


p page.form_with(:id=>"Form1")

year =  page.search('#srchStartYear')
p year.text

make =  page.search('#srchMake')
p make.text

model = page.field_with(:id=>'srchModel').value
trim =  page.forms[1].field_with(:id=>'srchTrim').value

p year
p make
p model
p trim
