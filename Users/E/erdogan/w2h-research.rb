# init app ######################################
require 'nokogiri'
require 'open-uri'
require 'json'
require 'net/http'
require "date"

# init query basics ######################################
APP_NAME         = "EnginErd-fae1-4521-a655-8f2deafba926"
OPERATION        = "findCompletedItems"
DATA_FORMAT      = "JSON"
KEYWORDS         = "nike sneakers"
SORT_ORDER       = "StartTimeNewest"
CATEGORY_ID      = "11450"   # clothing/fashion
#CATEGORY_ID      = "293"   # electronics
#CATEGORY_ID      = "2984";   # baby
# CATEGORY_ID      = "12576";   // business
# CATEGORY_ID      = "11700";   // home/garden
# CATEGORY_ID      = "267";   // books
# CATEGORY_ID      = "26395";   // health/beauty
# CATEGORY_ID      = "625"         // Cameras & Photo    
# CATEGORY_ID      = "550"         // Art    
# CATEGORY_ID      = "1"         // Collectibles    
ITEMS_PER_PAGE   = "100"
# PAGE_NUMBER      = "33";
COUNTRY          = "US"
END_TIME_FROM    = (Time.now-86400).utc.iso8601
#END_TIME_TO      = (Time.now).utc.iso8601
SELLER_TYPE      = "Private"
CONDITION        = "Used"

p=1
# cycle through each result page where p = page no ######################################
begin
  url = "http://svcs.ebay.com/services/search/FindingService/v1?SECURITY-APPNAME="+APP_NAME+"&GLOBAL-ID=EBAY-US"+"&OPERATION-NAME="+OPERATION+"&SERVICE-VERSION=1.0.0&RESPONSE-DATA-FORMAT="+DATA_FORMAT+"&REST-PAYLOAD&keywords="+KEYWORDS+"&itemFilter.name=LocatedIn&itemFilter.value="+COUNTRY+"&paginationInput.entriesPerPage="+ITEMS_PER_PAGE+"&paginationInput.pageNumber="+p.to_s+"&categoryId="+CATEGORY_ID+"&itemFilter.name=SellerBusinessType&itemFilter.value="+SELLER_TYPE+"&itemFilter.name=Condition&itemFilter.value="+CONDITION+"&outputSelector=SellerInfo"+"&sortOrder="+
SORT_ORDER+"&itemFilter.name=EndTimeFrom&itemFilter.value="+END_TIME_FROM

#+"&itemFilter.name=HideDuplicateItems&itemFilter.value=true"
#"&itemFilter.name=EndTimeTo&itemFilter.value="+END_TIME_TO+
# +"&sellingStatus.sellingState="+SELLING_STATE
# +"&outputSelector=StoreInfo"
  
  resp = Net::HTTP.get_response(URI.parse(URI.encode(url))).body  # get json to string
  result = JSON.parse(resp) # make it ruby readable
  items = result['findCompletedItemsResponse'][0]['searchResult'][0]['item'] || [] # find the nut in the shell
  
  #if p==1 then puts result['findCompletedItemsResponse'][0]['paginationOutput'][0]['totalEntries'].to_s + " items in " + result['findCompletedItemsResponse'][0]['paginationOutput'][0]['totalPages'][0] + " pages" end

  # assign the valuables  ######################################
  (0..items.length-1).each do |i|
    item = items[i]
    if item['listingInfo'][0]['startTime'][0] != item['listingInfo'][0]['endTime'][0]
      data = { 
        'itemId'   => item['itemId'],
        'title'    => item['title'],
  #      'pic'      => item['galleryURL'],
  #      'viewitem' => item['viewItemURL'],
        'startTime'  => item['listingInfo'][0]['startTime'],
        'endTime'  => item['listingInfo'][0]['endTime'],
        'duration' =>Time.iso8601(item['listingInfo'][0]['endTime'][0])-Time.iso8601(item['listingInfo'][0]['startTime'][0]),
        'sellerName'   => item['sellerInfo'][0]['sellerUserName'],
        'sellerScore' => item['sellerInfo'][0]['feedbackScore'][0],
        'sellerRating' => item['sellerInfo'][0]['feedbackRatingStar'],
        'sellingState' => item['sellingStatus'][0]['sellingState'],
        'price'        => item['sellingStatus'][0]['currentPrice'][0]['__value__'],
        #'condition'    => item['condition'][0]['conditionDisplayName'],
        'country'      => item['country'],
        'location'     => item['location'],
        'listingType'  => item['listingInfo'][0]['listingType']
      } 
      #puts "p"+p.to_s+" #"+(i+1).to_s + " | " + Time.iso8601(data['startTime'][0]).to_s + " ~ " + Time.iso8601(data['endTime'][0]).to_s + " | " + data['duration'].to_s

      # Save to datastore  ######################################
      ScraperWiki.save_sqlite unique_keys = ['itemId'], data = data
    end
  end
  p+=1
end while p <= result['findCompletedItemsResponse'][0]['paginationOutput'][0]['totalPages'][0].to_i  # ceiling page # init app ######################################
require 'nokogiri'
require 'open-uri'
require 'json'
require 'net/http'
require "date"

# init query basics ######################################
APP_NAME         = "EnginErd-fae1-4521-a655-8f2deafba926"
OPERATION        = "findCompletedItems"
DATA_FORMAT      = "JSON"
KEYWORDS         = "nike sneakers"
SORT_ORDER       = "StartTimeNewest"
CATEGORY_ID      = "11450"   # clothing/fashion
#CATEGORY_ID      = "293"   # electronics
#CATEGORY_ID      = "2984";   # baby
# CATEGORY_ID      = "12576";   // business
# CATEGORY_ID      = "11700";   // home/garden
# CATEGORY_ID      = "267";   // books
# CATEGORY_ID      = "26395";   // health/beauty
# CATEGORY_ID      = "625"         // Cameras & Photo    
# CATEGORY_ID      = "550"         // Art    
# CATEGORY_ID      = "1"         // Collectibles    
ITEMS_PER_PAGE   = "100"
# PAGE_NUMBER      = "33";
COUNTRY          = "US"
END_TIME_FROM    = (Time.now-86400).utc.iso8601
#END_TIME_TO      = (Time.now).utc.iso8601
SELLER_TYPE      = "Private"
CONDITION        = "Used"

p=1
# cycle through each result page where p = page no ######################################
begin
  url = "http://svcs.ebay.com/services/search/FindingService/v1?SECURITY-APPNAME="+APP_NAME+"&GLOBAL-ID=EBAY-US"+"&OPERATION-NAME="+OPERATION+"&SERVICE-VERSION=1.0.0&RESPONSE-DATA-FORMAT="+DATA_FORMAT+"&REST-PAYLOAD&keywords="+KEYWORDS+"&itemFilter.name=LocatedIn&itemFilter.value="+COUNTRY+"&paginationInput.entriesPerPage="+ITEMS_PER_PAGE+"&paginationInput.pageNumber="+p.to_s+"&categoryId="+CATEGORY_ID+"&itemFilter.name=SellerBusinessType&itemFilter.value="+SELLER_TYPE+"&itemFilter.name=Condition&itemFilter.value="+CONDITION+"&outputSelector=SellerInfo"+"&sortOrder="+
SORT_ORDER+"&itemFilter.name=EndTimeFrom&itemFilter.value="+END_TIME_FROM

#+"&itemFilter.name=HideDuplicateItems&itemFilter.value=true"
#"&itemFilter.name=EndTimeTo&itemFilter.value="+END_TIME_TO+
# +"&sellingStatus.sellingState="+SELLING_STATE
# +"&outputSelector=StoreInfo"
  
  resp = Net::HTTP.get_response(URI.parse(URI.encode(url))).body  # get json to string
  result = JSON.parse(resp) # make it ruby readable
  items = result['findCompletedItemsResponse'][0]['searchResult'][0]['item'] || [] # find the nut in the shell
  
  #if p==1 then puts result['findCompletedItemsResponse'][0]['paginationOutput'][0]['totalEntries'].to_s + " items in " + result['findCompletedItemsResponse'][0]['paginationOutput'][0]['totalPages'][0] + " pages" end

  # assign the valuables  ######################################
  (0..items.length-1).each do |i|
    item = items[i]
    if item['listingInfo'][0]['startTime'][0] != item['listingInfo'][0]['endTime'][0]
      data = { 
        'itemId'   => item['itemId'],
        'title'    => item['title'],
  #      'pic'      => item['galleryURL'],
  #      'viewitem' => item['viewItemURL'],
        'startTime'  => item['listingInfo'][0]['startTime'],
        'endTime'  => item['listingInfo'][0]['endTime'],
        'duration' =>Time.iso8601(item['listingInfo'][0]['endTime'][0])-Time.iso8601(item['listingInfo'][0]['startTime'][0]),
        'sellerName'   => item['sellerInfo'][0]['sellerUserName'],
        'sellerScore' => item['sellerInfo'][0]['feedbackScore'][0],
        'sellerRating' => item['sellerInfo'][0]['feedbackRatingStar'],
        'sellingState' => item['sellingStatus'][0]['sellingState'],
        'price'        => item['sellingStatus'][0]['currentPrice'][0]['__value__'],
        #'condition'    => item['condition'][0]['conditionDisplayName'],
        'country'      => item['country'],
        'location'     => item['location'],
        'listingType'  => item['listingInfo'][0]['listingType']
      } 
      #puts "p"+p.to_s+" #"+(i+1).to_s + " | " + Time.iso8601(data['startTime'][0]).to_s + " ~ " + Time.iso8601(data['endTime'][0]).to_s + " | " + data['duration'].to_s

      # Save to datastore  ######################################
      ScraperWiki.save_sqlite unique_keys = ['itemId'], data = data
    end
  end
  p+=1
end while p <= result['findCompletedItemsResponse'][0]['paginationOutput'][0]['totalPages'][0].to_i  # ceiling page 