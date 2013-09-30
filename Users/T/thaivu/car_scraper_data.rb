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
require 'builder'

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
    listCar = get_all_cars_in_page(page)
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
  listItem = []
  count = 0
  listBrand = get_list_brand(page)
  listBrand.each do |brand|
    listModel = get_models_by_brand(brand[:brand_id])
    listModel.each do |model|
      listEngine = get_engines_by_model(model[:model_id])
      listEngine.each do |engine|
        listFilterItem = get_filter_items_by_model_and_engine(engine[:engine_id], model[:model_id])
        listFilterItem.each do |filterItem|
          listItemContainer = get_item_container_by_filter(filterItem)
          listItemContainer.each do |page_container|
            itemInfo = get_item_detail_info(page_container)
            itemInfo[:brand] = brand[:brand_name]
            itemInfo[:model] = model[:model_name]
            itemInfo[:engine] = engine[:engine]
            listItem << itemInfo
            count += 1
            puts count
            if count == 10
              return listItem
            end
          end
        end
      end
    end
  end
  
  return listItem
  #page.search('table tbody tr').each do |car_container|
    #get_car_info(car_container)
  #end
end

#Parameters::
# *(Page) *params*:page
#Return:: list of brand in page
#*Author*::
#----------------------------------------------------------------------------
def get_list_brand(page)
  listBrand = []
  brand_container = page.search('#id_master option')
  puts brand_container.size
  for i in 1..brand_container.size-1
    brandObject = {}
    brand = brand_container[i]
    brandObject[:brand_id] = brand['value'].to_i
    brandObject[:brand_name] = brand.inner_text

    listBrand << brandObject
  end     

  return listBrand
end

#Parameters::
# *(brand_id) *params*:brand_id
#Return:: list of model in brand
#*Author*::
#----------------------------------------------------------------------------
def get_models_by_brand(brand_id)
  model_url = "http://wixeurope.com/Ajax/ModelMasterDetailAjaxFiltron.aspx?masterItemId=" + brand_id.to_s + "&languageName=english"
  response = Net::HTTP.get_response(URI.parse(model_url))
  modelString = response.body.to_s
  
  listModel = get_list_models(modelString)

  return listModel
end

#Parameters::
# *(modelString) *params*:modelString
#Return:: list of model in brand
#*Author*::
#----------------------------------------------------------------------------
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

#Parameters::
# *(model_id) *params*:model_id
#Return:: list of engine in model
#*Author*::
#----------------------------------------------------------------------------
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
    engineObject[:engine] = {}
    engineObject[:engine][:engine_name] = listTd[0].inner_text
    engineObject[:engine][:cc] = listTd[1].inner_text
    engineObject[:engine][:no] = listTd[2].inner_text
    engineObject[:engine][:hp] = listTd[3].inner_text

    listEngine << engineObject
  end 

  return listEngine
end

#Parameters::
# *(engine_id, model_id) *params*:engine_id, model_id
#Return:: list of filter item in engine
#*Author*::
#----------------------------------------------------------------------------
def get_filter_items_by_model_and_engine(engine_id, model_id)
  listFilterItem = []
  filter_item_url = "http://wixeurope.com/Ajax/FiltersTableAjaxFiltron.aspx?engineId="+ engine_id.to_s + "&modelId=" + model_id.to_s + "&languageName=english"
  response = Net::HTTP.get_response(URI.parse(filter_item_url ))
  listFilterItemPage = Nokogiri::HTML(response.body)
  
  listTr = listFilterItemPage .search('tr')
  for i in 2..listTr.size-1
    filterItemObject = {}
    listTd = listTr[i].search('td')
    filterItemObject[:year] = listTd[0].inner_text
    filterItemObject[:description] = listTd[1].inner_text
    filterItemObject[:air_id] = listTd[2]['id'].to_i
    filterItemObject[:oil_id] = listTd[3]['id'].to_i
    filterItemObject[:fuel_id] = listTd[4]['id'].to_i
    filterItemObject[:paper_id] = listTd[5]['id'].to_i
    filterItemObject[:carbon_id] = listTd[6]['id'].to_i
    filterItemObject[:other_id] = listTd[7]['id'].to_i

    listFilterItem << filterItemObject 
  end

  return listFilterItem 
end

#Parameters::
# *(filterItem) *params*:filterItem
#Return:: list of item container in filterItem
#*Author*::
#----------------------------------------------------------------------------
def get_item_container_by_filter(filterItem)
  listItemPage = []
  filterItem = filterItem.values
  filterItem.each do |val|
    if val.class == Fixnum
      if val != 0 
        item_url = "http://wixeurope.com/Ajax/FiltersSingleAjaxFiltron.aspx?filterId=" + val.to_s + "&languageName=english&isHdTruck=false"
        response = Net::HTTP.get_response(URI.parse(item_url))
        itemPage = Nokogiri::HTML(response.body)
        listItemPage << itemPage 
      end
    end
  end

  return listItemPage
end

#Parameters::
# *(page_container) *params*:page_container
#Return:: detail info of item container
#*Author*::
#----------------------------------------------------------------------------
def get_item_detail_info(page_container)
  itemInfo = {}
  itemInfo[:texts] = get_item_text(page_container)
  itemInfo[:dimensions] = get_item_dimensions(page_container)
  itemInfo[:using] = get_item_using(page_container)
  itemInfo[:pictures] = get_item_pictures(page_container)

  return itemInfo
end

##
#get_item name
#Parameters::
# *(page_container) *params*: page_container
#Return:: name of the item
#*Author*::
#----------------------------------------------------------------------------
def get_item_text(page_container)
  return page_container.at('span').inner_text
end

##
#get_item dimensions
#Parameters::
# *(page_container) *params*: page_container
#Return:: dimesions of the item
#*Author*::
#----------------------------------------------------------------------------
def get_item_dimensions(page_container)
  dimensions = {}
  table = page_container.at('table')
  listTr = table.search('tr')
  listTd = listTr[0].search('td')
  dimensions[:A] = listTd[0].at('span').inner_text
  dimensions[:B] = listTd[1].at('span').inner_text
  dimensions[:C] = listTd[2].at('span').inner_text
  listTd = listTr[1].search('td')
  dimensions[:D] = listTd[0].at('span').inner_text
  dimensions[:E] = listTd[1].at('span').inner_text
  dimensions[:F] = listTd[2].at('span').inner_text
  listTd = listTr[2].search('td')
  dimensions[:G] = listTd[0].at('span').inner_text
  dimensions[:H] = listTd[1].at('span').inner_text

  return dimensions 
end

##
#get_item using
#Parameters::
# *(page_container) *params*: page_container
#Return:: using of the item
#*Author*::
#----------------------------------------------------------------------------
def get_item_using(page_container)
  using = {}
  listLi = page_container.search('li')
  using[:byPassValve] = listLi[0].at('span').inner_text
  using[:antiDrainValve] = listLi[1].at('span').inner_text
  using[:antiSyphonValve] = listLi[2].at('span').inner_text
  using[:installationGuide] = listLi[3].at('span').inner_text
  using[:applications] = listLi[4].at('span').inner_text

  return using
end

##
#get_item picture
#Parameters::
# *(page_container) *params*: page_container
#Return:: picture of the item
#*Author*::
#----------------------------------------------------------------------------
def get_item_pictures(page_container)
  image = page_container.search('#searchRightSideTopRightFiltron img')[0]
  return !image['src'].nil? ? image['src'] : ""
end

##
#convert to xml format
#Parameters::
# *(listItem) *params*: listItem
#Return:: xml format of listItem
#*Author*::
#----------------------------------------------------------------------------
def convert_to_xml(listItem)
  result = ""

  xml = Builder::XmlMarkup.new(:target => result, :ident => 2)
  
  xml.instruct!
  xml.cars do
    listItem.each do |item|
      xml.item do
        xml.texts item[:texts]
        dimensions = item[:dimensions]
        xml.dimensions do
          xml.A dimensions[:A]
          xml.B dimensions[:B]
          xml.C dimensions[:C]
          xml.D dimensions[:D]
          xml.E dimensions[:E]
          xml.F dimensions[:F]
          xml.G dimensions[:G]
          xml.H dimensions[:H]
        end
        using = item[:using]
        xml.using do
          xml.byPassValve using[:byPassValve]
          xml.antiDrainValve using[:antiDrainValve]
          xml.antiSyphonValve using[:antiSyphonValve]
          xml.installationGuide using[:installationGuide]
          xml.applications using[:applications]
        end
        xml.pictures item[:pictures]
        xml.brand item[:brand]
        xml.model item[:model]
        engine = item[:engine]
        xml.engine do
          xml.engine_name engine[:engine_name]
          xml.cc engine[:cc]
          xml.no engine[:no]
          xml.hp engine[:hp]
        end
      end
    end
  end
  return result
end

##
#write to xml file
#Parameters::
# *(xmlContent) *params*: xmlContent
#Return:: a file with xml format
#*Author*::
#----------------------------------------------------------------------------
def write_to_xml_file(xmlContent)
  # Create a new file and write to it  
  File.open('carDataXml.xml', 'w') do |item|  
    # use "\n" for two lines of text  
    item.puts xmlContent  
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
  #car_info.seller_datetime = get_seller_datetime(car_container)
  #car_info.seller_email    = get_seller_email(car_container)
  #car_info.location        = get_location(car_container)
  #car_info.seller_phone    = get_seller_phone(car_container)
  
  #car_info.year            = get_year(car_container)
  #car_info.make            = get_make(car_container)
  #car_info.model           = get_model(car_container)
  #car_info.trim            = get_trim(car_container)
  #car_info.miles           = get_miles(car_container)
  #car_info.price           = get_price(car_container)

  #car_info.one_owner       = get_one_owner(car_container)
  #car_info.clean_title     = get_clean_title(car_container)
  #car_info.clean_carfax    = get_clean_carfax(car_container)
  #car_info.vin_number      = get_vin_number(car_container)

  #car_info.engine_size     = get_engine_size(car_container)
  #car_info.automatic       = get_automatic(car_container)
  #car_info.wd              = get_wd(car_container)
  #car_info.moonroof        = get_moonroof(car_container)
  #car_info.cloth_leather   = get_cloth_leather(car_container)
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
listCar = get_all_cars_in_page(page)
xmlContent = convert_to_xml(listCar)
xmlFile = write_to_xml_file(xmlContent)
puts xmlContent # This scraper is to scrape all car information from craiglist.com
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
require 'builder'

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
    listCar = get_all_cars_in_page(page)
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
  listItem = []
  count = 0
  listBrand = get_list_brand(page)
  listBrand.each do |brand|
    listModel = get_models_by_brand(brand[:brand_id])
    listModel.each do |model|
      listEngine = get_engines_by_model(model[:model_id])
      listEngine.each do |engine|
        listFilterItem = get_filter_items_by_model_and_engine(engine[:engine_id], model[:model_id])
        listFilterItem.each do |filterItem|
          listItemContainer = get_item_container_by_filter(filterItem)
          listItemContainer.each do |page_container|
            itemInfo = get_item_detail_info(page_container)
            itemInfo[:brand] = brand[:brand_name]
            itemInfo[:model] = model[:model_name]
            itemInfo[:engine] = engine[:engine]
            listItem << itemInfo
            count += 1
            puts count
            if count == 10
              return listItem
            end
          end
        end
      end
    end
  end
  
  return listItem
  #page.search('table tbody tr').each do |car_container|
    #get_car_info(car_container)
  #end
end

#Parameters::
# *(Page) *params*:page
#Return:: list of brand in page
#*Author*::
#----------------------------------------------------------------------------
def get_list_brand(page)
  listBrand = []
  brand_container = page.search('#id_master option')
  puts brand_container.size
  for i in 1..brand_container.size-1
    brandObject = {}
    brand = brand_container[i]
    brandObject[:brand_id] = brand['value'].to_i
    brandObject[:brand_name] = brand.inner_text

    listBrand << brandObject
  end     

  return listBrand
end

#Parameters::
# *(brand_id) *params*:brand_id
#Return:: list of model in brand
#*Author*::
#----------------------------------------------------------------------------
def get_models_by_brand(brand_id)
  model_url = "http://wixeurope.com/Ajax/ModelMasterDetailAjaxFiltron.aspx?masterItemId=" + brand_id.to_s + "&languageName=english"
  response = Net::HTTP.get_response(URI.parse(model_url))
  modelString = response.body.to_s
  
  listModel = get_list_models(modelString)

  return listModel
end

#Parameters::
# *(modelString) *params*:modelString
#Return:: list of model in brand
#*Author*::
#----------------------------------------------------------------------------
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

#Parameters::
# *(model_id) *params*:model_id
#Return:: list of engine in model
#*Author*::
#----------------------------------------------------------------------------
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
    engineObject[:engine] = {}
    engineObject[:engine][:engine_name] = listTd[0].inner_text
    engineObject[:engine][:cc] = listTd[1].inner_text
    engineObject[:engine][:no] = listTd[2].inner_text
    engineObject[:engine][:hp] = listTd[3].inner_text

    listEngine << engineObject
  end 

  return listEngine
end

#Parameters::
# *(engine_id, model_id) *params*:engine_id, model_id
#Return:: list of filter item in engine
#*Author*::
#----------------------------------------------------------------------------
def get_filter_items_by_model_and_engine(engine_id, model_id)
  listFilterItem = []
  filter_item_url = "http://wixeurope.com/Ajax/FiltersTableAjaxFiltron.aspx?engineId="+ engine_id.to_s + "&modelId=" + model_id.to_s + "&languageName=english"
  response = Net::HTTP.get_response(URI.parse(filter_item_url ))
  listFilterItemPage = Nokogiri::HTML(response.body)
  
  listTr = listFilterItemPage .search('tr')
  for i in 2..listTr.size-1
    filterItemObject = {}
    listTd = listTr[i].search('td')
    filterItemObject[:year] = listTd[0].inner_text
    filterItemObject[:description] = listTd[1].inner_text
    filterItemObject[:air_id] = listTd[2]['id'].to_i
    filterItemObject[:oil_id] = listTd[3]['id'].to_i
    filterItemObject[:fuel_id] = listTd[4]['id'].to_i
    filterItemObject[:paper_id] = listTd[5]['id'].to_i
    filterItemObject[:carbon_id] = listTd[6]['id'].to_i
    filterItemObject[:other_id] = listTd[7]['id'].to_i

    listFilterItem << filterItemObject 
  end

  return listFilterItem 
end

#Parameters::
# *(filterItem) *params*:filterItem
#Return:: list of item container in filterItem
#*Author*::
#----------------------------------------------------------------------------
def get_item_container_by_filter(filterItem)
  listItemPage = []
  filterItem = filterItem.values
  filterItem.each do |val|
    if val.class == Fixnum
      if val != 0 
        item_url = "http://wixeurope.com/Ajax/FiltersSingleAjaxFiltron.aspx?filterId=" + val.to_s + "&languageName=english&isHdTruck=false"
        response = Net::HTTP.get_response(URI.parse(item_url))
        itemPage = Nokogiri::HTML(response.body)
        listItemPage << itemPage 
      end
    end
  end

  return listItemPage
end

#Parameters::
# *(page_container) *params*:page_container
#Return:: detail info of item container
#*Author*::
#----------------------------------------------------------------------------
def get_item_detail_info(page_container)
  itemInfo = {}
  itemInfo[:texts] = get_item_text(page_container)
  itemInfo[:dimensions] = get_item_dimensions(page_container)
  itemInfo[:using] = get_item_using(page_container)
  itemInfo[:pictures] = get_item_pictures(page_container)

  return itemInfo
end

##
#get_item name
#Parameters::
# *(page_container) *params*: page_container
#Return:: name of the item
#*Author*::
#----------------------------------------------------------------------------
def get_item_text(page_container)
  return page_container.at('span').inner_text
end

##
#get_item dimensions
#Parameters::
# *(page_container) *params*: page_container
#Return:: dimesions of the item
#*Author*::
#----------------------------------------------------------------------------
def get_item_dimensions(page_container)
  dimensions = {}
  table = page_container.at('table')
  listTr = table.search('tr')
  listTd = listTr[0].search('td')
  dimensions[:A] = listTd[0].at('span').inner_text
  dimensions[:B] = listTd[1].at('span').inner_text
  dimensions[:C] = listTd[2].at('span').inner_text
  listTd = listTr[1].search('td')
  dimensions[:D] = listTd[0].at('span').inner_text
  dimensions[:E] = listTd[1].at('span').inner_text
  dimensions[:F] = listTd[2].at('span').inner_text
  listTd = listTr[2].search('td')
  dimensions[:G] = listTd[0].at('span').inner_text
  dimensions[:H] = listTd[1].at('span').inner_text

  return dimensions 
end

##
#get_item using
#Parameters::
# *(page_container) *params*: page_container
#Return:: using of the item
#*Author*::
#----------------------------------------------------------------------------
def get_item_using(page_container)
  using = {}
  listLi = page_container.search('li')
  using[:byPassValve] = listLi[0].at('span').inner_text
  using[:antiDrainValve] = listLi[1].at('span').inner_text
  using[:antiSyphonValve] = listLi[2].at('span').inner_text
  using[:installationGuide] = listLi[3].at('span').inner_text
  using[:applications] = listLi[4].at('span').inner_text

  return using
end

##
#get_item picture
#Parameters::
# *(page_container) *params*: page_container
#Return:: picture of the item
#*Author*::
#----------------------------------------------------------------------------
def get_item_pictures(page_container)
  image = page_container.search('#searchRightSideTopRightFiltron img')[0]
  return !image['src'].nil? ? image['src'] : ""
end

##
#convert to xml format
#Parameters::
# *(listItem) *params*: listItem
#Return:: xml format of listItem
#*Author*::
#----------------------------------------------------------------------------
def convert_to_xml(listItem)
  result = ""

  xml = Builder::XmlMarkup.new(:target => result, :ident => 2)
  
  xml.instruct!
  xml.cars do
    listItem.each do |item|
      xml.item do
        xml.texts item[:texts]
        dimensions = item[:dimensions]
        xml.dimensions do
          xml.A dimensions[:A]
          xml.B dimensions[:B]
          xml.C dimensions[:C]
          xml.D dimensions[:D]
          xml.E dimensions[:E]
          xml.F dimensions[:F]
          xml.G dimensions[:G]
          xml.H dimensions[:H]
        end
        using = item[:using]
        xml.using do
          xml.byPassValve using[:byPassValve]
          xml.antiDrainValve using[:antiDrainValve]
          xml.antiSyphonValve using[:antiSyphonValve]
          xml.installationGuide using[:installationGuide]
          xml.applications using[:applications]
        end
        xml.pictures item[:pictures]
        xml.brand item[:brand]
        xml.model item[:model]
        engine = item[:engine]
        xml.engine do
          xml.engine_name engine[:engine_name]
          xml.cc engine[:cc]
          xml.no engine[:no]
          xml.hp engine[:hp]
        end
      end
    end
  end
  return result
end

##
#write to xml file
#Parameters::
# *(xmlContent) *params*: xmlContent
#Return:: a file with xml format
#*Author*::
#----------------------------------------------------------------------------
def write_to_xml_file(xmlContent)
  # Create a new file and write to it  
  File.open('carDataXml.xml', 'w') do |item|  
    # use "\n" for two lines of text  
    item.puts xmlContent  
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
  #car_info.seller_datetime = get_seller_datetime(car_container)
  #car_info.seller_email    = get_seller_email(car_container)
  #car_info.location        = get_location(car_container)
  #car_info.seller_phone    = get_seller_phone(car_container)
  
  #car_info.year            = get_year(car_container)
  #car_info.make            = get_make(car_container)
  #car_info.model           = get_model(car_container)
  #car_info.trim            = get_trim(car_container)
  #car_info.miles           = get_miles(car_container)
  #car_info.price           = get_price(car_container)

  #car_info.one_owner       = get_one_owner(car_container)
  #car_info.clean_title     = get_clean_title(car_container)
  #car_info.clean_carfax    = get_clean_carfax(car_container)
  #car_info.vin_number      = get_vin_number(car_container)

  #car_info.engine_size     = get_engine_size(car_container)
  #car_info.automatic       = get_automatic(car_container)
  #car_info.wd              = get_wd(car_container)
  #car_info.moonroof        = get_moonroof(car_container)
  #car_info.cloth_leather   = get_cloth_leather(car_container)
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
listCar = get_all_cars_in_page(page)
xmlContent = convert_to_xml(listCar)
xmlFile = write_to_xml_file(xmlContent)
puts xmlContent 