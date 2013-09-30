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
require 'nokogiri'

# The starting URL to get cars from

# Todo: Change the STARTING_URL to reflect your work
STARTING_URL = 'http://wixeurope.com/passenger-car,370.html'

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
  
  return !page.nil? 
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
  
  listBrand = get_list_brand(page)
  listBrand.each do |brand|
    listModel = get_models_by_brand(brand[:brand_id])
    listModel.each do |model|
      listEngine = get_engines_by_model(model[:model_id])
      listEngine.each do |engine|
        listItem = get_items_by_model_and_engine(engine[:engine_id], model[:model_id])
        puts listItem
      end
    end
  end

  #page.search('table tbody tr').each do |car_container|
    #get_car_info(car_container)
  #end
end

def get_list_brand(page)
  listBrand = []
  brand_container = page.search('#id_master option')
  for i in 1..brand_container.size-1
    brandObject = {}
    brand = brand_container[i]
    brandObject[:brand_id] = brand['value'].to_i
    brandObject[:brand_name] = brand.inner_text

    listBrand << brandObject
  end     

  return listBrand
end

def get_models_by_brand(brand_id)
  model_url = "http://wixeurope.com/Ajax/ModelMasterDetailAjaxFiltron.aspx?masterItemId=" + brand_id.to_s + "&languageName=english"
  response = Net::HTTP.get_response(URI.parse(model_url))
  modelString = response.body.to_s
  
  listModel = get_list_models(modelString)

  return listModel
end

def get_list_models(modelString)
  listModel = []
  listModelStr = modelString.split(';')
  for i in 1..listModelStr.size-2
    model = {}
    model[:model_name] = listModelStr[i].split('|')[0]
    model[:model_id] = listModelStr[i].split('|')[1].to_i
    listModel << model
  end

  return listModel
end

def get_engines_by_model(model_id)
  listEngine = []
  engine_url = "http://wixeurope.com/Ajax/EngineMasterDetailAjaxFiltron.aspx?masterItemId=" + model_id.to_s + "&languageName=english"
  response = Net::HTTP.get_response(URI.parse(engine_url))
  listEnginePage = Nokogiri::HTML(response.body)
  
  listTr = listEnginePage.search('tr')
  listTr.each do |tr|
    engineObject = {}
    engine_id_str = tr['id']
    engineObject[:engine_id] = engine_id_str.gsub('engineSelect-','').to_i
    listTd = tr.search('td')
    engineObject[:engine_name] = listTd[0].inner_text
    engineObject[:cc] = listTd[1].inner_text
    engineObject[:no] = listTd[2].inner_text
    engineObject[:hp] = listTd[3].inner_text

    listEngine << engineObject
  end 

  return listEngine
end

def get_items_by_model_and_engine(engine_id, model_id)
  listItem = []
  item_url = "http://wixeurope.com/Ajax/FiltersTableAjaxFiltron.aspx?engineId="+ engine_id.to_s + "&modelId=" + model_id.to_s + "&languageName=english"
  response = Net::HTTP.get_response(URI.parse(item_url))
  listItemPage = Nokogiri::HTML(response.body)
  
  listTr = listItemPage.search('tr')
  for i in 2..listTr.size-1
    itemObject = {}
    listTd = listTr[i].search('td')
    itemObject[:year] = listTd[0].inner_text
    itemObject[:description] = listTd[1].inner_text
    itemObject[:airObj] = get_item_info_object(listTd[2])
    itemObject[:oilObj] = get_item_info_object(listTd[3])
    itemObject[:fuelObj] = get_item_info_object(listTd[4])
    itemObject[:paperObj] = get_item_info_object(listTd[5])
    itemObject[:carbonObj] = get_item_info_object(listTd[6])
    itemObject[:other] = listTd[7].inner_text

    listItem << itemObject
  end

  return listItem
end

def get_item_info_object(td)  resultObj = {}
  resultObj[:id] = td['id']
  resultObj[:value] = td.inner_text

  return resultObj
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

  # Todo: Put your code to process the car_container to get the car_info here
  car_info.seller_datetime = get_seller_datetime(car_container)
  car_info.seller_email    = get_seller_email(car_container)
  car_info.location        = get_location(car_container)
  car_info.seller_phone    = get_seller_phone(car_container)
  
  car_info.year            = get_year(car_container)
  car_info.make            = get_make(car_container)
  car_info.model           = get_model(car_container)
  car_info.trim            = get_trim(car_container)
  car_info.miles           = get_miles(car_container)
  car_info.price           = get_price(car_container)

  car_info.one_owner       = get_one_owner(car_container)
  car_info.clean_title     = get_clean_title(car_container)
  car_info.clean_carfax    = get_clean_carfax(car_container)
  car_info.vin_number      = get_vin_number(car_container)

  car_info.engine_size     = get_engine_size(car_container)
  car_info.automatic       = get_automatic(car_container)
  car_info.wd              = get_wd(car_container)
  car_info.moonroof        = get_moonroof(car_container)
  car_info.cloth_leather   = get_cloth_leather(car_container)
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

agent = Mechanize.new
page = agent.get(STARTING_URL)

#get_all_cars(page)
get_all_cars_in_page(page)
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
require 'nokogiri'

# The starting URL to get cars from

# Todo: Change the STARTING_URL to reflect your work
STARTING_URL = 'http://wixeurope.com/passenger-car,370.html'

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
  
  return !page.nil? 
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
  
  listBrand = get_list_brand(page)
  listBrand.each do |brand|
    listModel = get_models_by_brand(brand[:brand_id])
    listModel.each do |model|
      listEngine = get_engines_by_model(model[:model_id])
      listEngine.each do |engine|
        listItem = get_items_by_model_and_engine(engine[:engine_id], model[:model_id])
        puts listItem
      end
    end
  end

  #page.search('table tbody tr').each do |car_container|
    #get_car_info(car_container)
  #end
end

def get_list_brand(page)
  listBrand = []
  brand_container = page.search('#id_master option')
  for i in 1..brand_container.size-1
    brandObject = {}
    brand = brand_container[i]
    brandObject[:brand_id] = brand['value'].to_i
    brandObject[:brand_name] = brand.inner_text

    listBrand << brandObject
  end     

  return listBrand
end

def get_models_by_brand(brand_id)
  model_url = "http://wixeurope.com/Ajax/ModelMasterDetailAjaxFiltron.aspx?masterItemId=" + brand_id.to_s + "&languageName=english"
  response = Net::HTTP.get_response(URI.parse(model_url))
  modelString = response.body.to_s
  
  listModel = get_list_models(modelString)

  return listModel
end

def get_list_models(modelString)
  listModel = []
  listModelStr = modelString.split(';')
  for i in 1..listModelStr.size-2
    model = {}
    model[:model_name] = listModelStr[i].split('|')[0]
    model[:model_id] = listModelStr[i].split('|')[1].to_i
    listModel << model
  end

  return listModel
end

def get_engines_by_model(model_id)
  listEngine = []
  engine_url = "http://wixeurope.com/Ajax/EngineMasterDetailAjaxFiltron.aspx?masterItemId=" + model_id.to_s + "&languageName=english"
  response = Net::HTTP.get_response(URI.parse(engine_url))
  listEnginePage = Nokogiri::HTML(response.body)
  
  listTr = listEnginePage.search('tr')
  listTr.each do |tr|
    engineObject = {}
    engine_id_str = tr['id']
    engineObject[:engine_id] = engine_id_str.gsub('engineSelect-','').to_i
    listTd = tr.search('td')
    engineObject[:engine_name] = listTd[0].inner_text
    engineObject[:cc] = listTd[1].inner_text
    engineObject[:no] = listTd[2].inner_text
    engineObject[:hp] = listTd[3].inner_text

    listEngine << engineObject
  end 

  return listEngine
end

def get_items_by_model_and_engine(engine_id, model_id)
  listItem = []
  item_url = "http://wixeurope.com/Ajax/FiltersTableAjaxFiltron.aspx?engineId="+ engine_id.to_s + "&modelId=" + model_id.to_s + "&languageName=english"
  response = Net::HTTP.get_response(URI.parse(item_url))
  listItemPage = Nokogiri::HTML(response.body)
  
  listTr = listItemPage.search('tr')
  for i in 2..listTr.size-1
    itemObject = {}
    listTd = listTr[i].search('td')
    itemObject[:year] = listTd[0].inner_text
    itemObject[:description] = listTd[1].inner_text
    itemObject[:airObj] = get_item_info_object(listTd[2])
    itemObject[:oilObj] = get_item_info_object(listTd[3])
    itemObject[:fuelObj] = get_item_info_object(listTd[4])
    itemObject[:paperObj] = get_item_info_object(listTd[5])
    itemObject[:carbonObj] = get_item_info_object(listTd[6])
    itemObject[:other] = listTd[7].inner_text

    listItem << itemObject
  end

  return listItem
end

def get_item_info_object(td)  resultObj = {}
  resultObj[:id] = td['id']
  resultObj[:value] = td.inner_text

  return resultObj
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

  # Todo: Put your code to process the car_container to get the car_info here
  car_info.seller_datetime = get_seller_datetime(car_container)
  car_info.seller_email    = get_seller_email(car_container)
  car_info.location        = get_location(car_container)
  car_info.seller_phone    = get_seller_phone(car_container)
  
  car_info.year            = get_year(car_container)
  car_info.make            = get_make(car_container)
  car_info.model           = get_model(car_container)
  car_info.trim            = get_trim(car_container)
  car_info.miles           = get_miles(car_container)
  car_info.price           = get_price(car_container)

  car_info.one_owner       = get_one_owner(car_container)
  car_info.clean_title     = get_clean_title(car_container)
  car_info.clean_carfax    = get_clean_carfax(car_container)
  car_info.vin_number      = get_vin_number(car_container)

  car_info.engine_size     = get_engine_size(car_container)
  car_info.automatic       = get_automatic(car_container)
  car_info.wd              = get_wd(car_container)
  car_info.moonroof        = get_moonroof(car_container)
  car_info.cloth_leather   = get_cloth_leather(car_container)
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

agent = Mechanize.new
page = agent.get(STARTING_URL)

#get_all_cars(page)
get_all_cars_in_page(page)
