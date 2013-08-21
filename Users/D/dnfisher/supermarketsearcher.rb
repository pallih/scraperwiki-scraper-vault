require 'open-uri'
require 'nokogiri'

def string_to_float(string)
  string.gsub!(/[^\d.,]/,'')          # Replace all Currency Symbols, Letters and -- from the string

  if string =~ /^.*[\.,]\d{1}$/       # If string ends in a single digit (e.g. ,2)
    string = string + "0"             # make it ,20 in order for the result to be in "cents"
  end
    
  unless string =~ /^.*[\.,]\d{2}$/   # If does not end in ,00 / .00 then
    string = string + "00"            # add trailing 00 to turn it into cents
  end

  string.gsub!(/[\.,]/,'')            # Replace all (.) and (,) so the string result becomes in "cents"  
  string.to_f / 100                   # Let to_float do the rest
end

def GrabUrlData(urlToScrape, store, timeStamp)
  # get the page
  doc = Nokogiri::HTML(open(urlToScrape))

  # get the list of products
  doc.css("li#CellContainer").each do |product|

    # get the element that contains the details
    productDetails = product.css("div#CellBottom")

    ## get the different product attributes

    #fix the price
    fixedPrice = string_to_float(productDetails.css("span[itemprop=price]").text)
    
    # compose the data
    data = {
      "id" => productDetails.css("a#ProductName").attribute("value").text,
      "name" => productDetails.css("a#ProductName").at_css("span").text,
      "brand" => productDetails.css("span#Brand").text,
      "description" => productDetails.css("span#Description").text,
      "price" => fixedPrice,
      "priceValidUntil" => productDetails.css("span[itemprop=priceValidUntil]").text,
      "cheapest_store" => store,
      "lastUpdate" => timeStamp,
      "price_" + store => fixedPrice
    }

    checktableexists = ScraperWiki.table_info("swdata")
    
    if checktableexists.count > 0
      # see if there is a product already stored with the same id
      retrieved = ScraperWiki.select("* from swdata where id = :a", [data["id"]])

      # if it isn't found, then add it
      if retrieved.count == 0
        # this could possibly be a way to indicate new products... need a separate table to list found product ids so we can check against it
        ScraperWiki.save_sqlite(unique_keys=['id'], data=data)
      else
        # see what the timeStamp of the item is
        lastUpdate = retrieved[0]["lastUpdate"]      

        # if the lastUpdate < timeStamp (.i.e. now), then overwrite it without prejudice
        if (lastUpdate <=> timeStamp) == 1
          ScraperWiki.save_sqlite(unique_keys=['id'], data=data)
        else
          puts "fresh record found...current_store=" + store + ";record=" + retrieved[0].to_s

          # see if this is a duplicate (in the same store)
          #puts retrieved[0]["price_" + store].class
          #puts "duplicate:" + retrieved[0]["description"] unless retrieved[0]["price_" + store] == nil
              
          # update the record to indicate the price for the current store
          retrieved[0]["price_" + store] = fixedPrice

          # the timestamp is the same, so check whether the price is lower and save the details of the lowest price
          cheapestPrice = retrieved[0]["price"]
          if cheapestPrice > fixedPrice
            retrieved[0]["cheapest_store"] = store
            retrieved[0]["price"] = fixedPrice
            retrieved[0]["priceValidUntil"] = data["priceValidUntil"]
          end

          # update
          ScraperWiki.save_sqlite(unique_keys=['id'], data=retrieved[0])
        end
      end
    else
      # the table doesnt exist yet so create it by inserting the first row
      ScraperWiki.save_sqlite(unique_keys=['id'], data=data)
    end
  end
end

def EnsureDatabase()
  ScraperWiki.sqliteexecute("drop table if exists swdata")
  ScraperWiki.sqliteexecute("
    CREATE TABLE `swdata` (
      `id` integer,
      `name` text,
      `brand` text,
      `description` text,
      `price` real,
      `priceValidUntil` text,
      `cheapest_store` text,
      `lastUpdate` date,
      `price_Asda` real,
      `price_Sainsburys` real,
      `price_Tesco` real,
      `price_Waitrose` real,
      `price_Ocado` real)")
end

def Scrape()
  # get the data for the following:
  sources = [
    ['Sainsburys', "http://www.mysupermarket.co.uk/#/shelves/Fresh_Milk_in_Sainsburys.html"],
    ['Tesco','http://www.mysupermarket.co.uk/#/shelves/Fresh_Milk_in_Tesco.html'],
    ['Asda','http://www.mysupermarket.co.uk/#/shelves/Fresh_Milk_in_ASDA.html'],
    ['Waitrose','http://www.mysupermarket.co.uk/#/shelves/Fresh_Milk_in_Waitrose.html'],
    ['Ocado','http://www.mysupermarket.co.uk/#/shelves/Fresh_Milk_in_Ocado.html']
  ]
  timeStamp = Time.now
  sources.each { |source|
    GrabUrlData(source[1], source[0], timeStamp)
  }

  # delete records which have not been updated.
 
end

#################################
# Program Execution Starts Here
#################################
#EnsureDatabase()
Scrape()
 
# numbers to try 38860, 105393
#retrieved = ScraperWiki.select("* from swdata where id = ?", 155575)
#puts retrieved[0]["lastUpdate"]



#puts ScraperWiki.show_tables()
#puts ScraperWiki.table_info("swdata")
#puts ScraperWiki.select("* from swdata")
#ScraperWiki.sqliteexecute("drop table if exists prices")
#ScraperWiki.sqliteexecute("create table prices (id int, name varchar(255), brand varchar(50), description varchar(1024), price real, priceValidUntil date, lastupdate date)")
#puts ScraperWiki.sqliteexecute("select * from prices") #[{'yy'=> 'hello', 'xx'=> 9}, {'yy'=>'again', 'xx'=>10}]