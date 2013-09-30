# Blank Ruby
require 'mechanize'

def getLinks(localURL, localDomain, localLinksHash)

  agent = Mechanize.new
  agent.redirect_ok=true # We only want to follow permanent re-directs
  agent.agent.http.verify_mode = OpenSSL::SSL::VERIFY_NONE # This is not ideal!!

  puts "**************"
  puts "Reading page: " + localURL

  page = agent.get(localURL)

  pageLinks = Nokogiri::HTML(page.body).css('a') 
  pageLinks.each do |link| 
    # Build a well-formed URL
    if link["href"] != nil
      linkHREF = link["href"]
      if linkHREF[0] == "/" # Link in the same domain.
        linkHREF = "http://" + localDomain + linkHREF #http is required by scraperwiki
      end

      if linkHREF.match(/\A(http:\/\/|https:\/\/)?((\w)+\.)?#{localDomain}/i)
        # Means this is a link in the same domain, so push it to the database.
        # Skip HTTPS links
        if linkHREF.match("https") == nil
          currentTime = DateTime.now
          # Let's see if the link exists already in the database, if it does, then don't add it
          if localLinksHash[linkHREF] == nil
              # Link doesn't exist yet; add it
              ScraperWiki::save_sqlite(unique_keys=["url"], data={"domain"=>localDomain, "url"=>linkHREF,
               "last_crawled"=>currentTime, "last_parsed"=>nil, "status"=>"1"}, table_name="links")
              # Status: 1 - New; 2- Crawled; 3- Parsed
          else
            currentHashRow = localLinksHash[linkHREF]
            if Date.parse(currentHashRow["last_crawled"]) + 1 < DateTime.now
              # only add if it has been more than one day since last add
                ScraperWiki::save_sqlite(unique_keys=["url"], data={"domain"=>localDomain, "url"=>linkHREF,
                 "last_crawled"=>currentTime, "last_parsed"=>nil, "status"=>"1"}, table_name="links")           
            # else
            #  puts "Less than a day since last extraction for this URL" 
            end  
          end
        else
          # This is an https link, apparently 
        end
      end
    end
  end
end


# Get the internal links for the top-level domain
thisURL = "http://express.com/"
thisDOMAIN = "express.com"

linksHash = Hash.new
getLinks(thisURL, thisDOMAIN, linksHash)

selectStatement = "* from links where domain='" + thisDOMAIN + "'"  
linkTable = ScraperWiki::select(selectStatement)

# Create a hash table that has the URL of the page as key
linkTable.each do |linkTableRow|
  linksHash[linkTableRow.fetch("url")] = linkTableRow 
end

puts "linksHash Size = " + linksHash.size.to_s

count = 0

linkTable.each do |linkTableRow|
 getLinks(linkTableRow.fetch("url"), thisDOMAIN, linksHash)
 puts "count = " + count.to_s + " linksHash Size = " + linksHash.size.to_s
 count += 1
end
#print linkTable






__END__

# From here on - process a single product page

# html = ScraperWiki::scrape("http://www.express.com/mesh-sleeve-sweater-dress-49937-953/control/page/2/show/3/index.pro")           
agent = Mechanize.new

#test 1: Multiple color
#URL = "http://www.express.com/the-original-long-sleeve-essential-shirt-49883-1051/control/show/3/index.pro#jsLink"
url = 'http://www.express.com/fitted-long-sleeve-essential-shirt-45651-721/control/page/14/show/3/index.pro?relatedItem=true&showBreadcrumb=true#jsLink'


#test 2: single color
#URL = 'http://www.express.com/striped-rolled-sleeve-cover-up-sweater-50122-215/control/page/6/show/3/index.pro' 


#Clean URL of parameters
puts url
url[/\?/]? url[/\?.*/] = '' : true
url[/#/]? url[/#.*/] = '' : true
puts url;

page = agent.get(url)

itemTitle = Nokogiri::HTML(page.body).css('#cat-pro-con-detail h1')
puts "Item title: " + itemTitle.text

itemPrice = Nokogiri::HTML(page.body).css('li.cat-pro-price')
puts "Item price: " + itemPrice.text

itemDesc = Nokogiri::HTML(page.body).css('li.cat-pro-desc')
puts "Item description: " + itemDesc.text

#A: This section breaks out individual list items
#itemIndiv = Nokogiri::HTML(page.body).css('li.cat-pro-desc ul li')
#puts "Item bullets: " 
#itemIndiv.each do |item|
#  puts item.text
#end
#A:

colorsO = Nokogiri::HTML(page.body).css('img.cat-pro-swatch')
itemColors = "" 
colorsO.each do |item|
  itemColors.length > 0 ? itemColors = itemColors + ", " + item["alt"] : itemColors = itemColors + item["alt"]
end
puts itemColors

ScraperWiki::save_sqlite(unique_keys=["url"], data={"url"=>URL, "title"=>itemTitle.text,
     "price"=>itemPrice.text, "description"=>itemDesc.text, "colors"=>itemColors} )# Blank Ruby
require 'mechanize'

def getLinks(localURL, localDomain, localLinksHash)

  agent = Mechanize.new
  agent.redirect_ok=true # We only want to follow permanent re-directs
  agent.agent.http.verify_mode = OpenSSL::SSL::VERIFY_NONE # This is not ideal!!

  puts "**************"
  puts "Reading page: " + localURL

  page = agent.get(localURL)

  pageLinks = Nokogiri::HTML(page.body).css('a') 
  pageLinks.each do |link| 
    # Build a well-formed URL
    if link["href"] != nil
      linkHREF = link["href"]
      if linkHREF[0] == "/" # Link in the same domain.
        linkHREF = "http://" + localDomain + linkHREF #http is required by scraperwiki
      end

      if linkHREF.match(/\A(http:\/\/|https:\/\/)?((\w)+\.)?#{localDomain}/i)
        # Means this is a link in the same domain, so push it to the database.
        # Skip HTTPS links
        if linkHREF.match("https") == nil
          currentTime = DateTime.now
          # Let's see if the link exists already in the database, if it does, then don't add it
          if localLinksHash[linkHREF] == nil
              # Link doesn't exist yet; add it
              ScraperWiki::save_sqlite(unique_keys=["url"], data={"domain"=>localDomain, "url"=>linkHREF,
               "last_crawled"=>currentTime, "last_parsed"=>nil, "status"=>"1"}, table_name="links")
              # Status: 1 - New; 2- Crawled; 3- Parsed
          else
            currentHashRow = localLinksHash[linkHREF]
            if Date.parse(currentHashRow["last_crawled"]) + 1 < DateTime.now
              # only add if it has been more than one day since last add
                ScraperWiki::save_sqlite(unique_keys=["url"], data={"domain"=>localDomain, "url"=>linkHREF,
                 "last_crawled"=>currentTime, "last_parsed"=>nil, "status"=>"1"}, table_name="links")           
            # else
            #  puts "Less than a day since last extraction for this URL" 
            end  
          end
        else
          # This is an https link, apparently 
        end
      end
    end
  end
end


# Get the internal links for the top-level domain
thisURL = "http://express.com/"
thisDOMAIN = "express.com"

linksHash = Hash.new
getLinks(thisURL, thisDOMAIN, linksHash)

selectStatement = "* from links where domain='" + thisDOMAIN + "'"  
linkTable = ScraperWiki::select(selectStatement)

# Create a hash table that has the URL of the page as key
linkTable.each do |linkTableRow|
  linksHash[linkTableRow.fetch("url")] = linkTableRow 
end

puts "linksHash Size = " + linksHash.size.to_s

count = 0

linkTable.each do |linkTableRow|
 getLinks(linkTableRow.fetch("url"), thisDOMAIN, linksHash)
 puts "count = " + count.to_s + " linksHash Size = " + linksHash.size.to_s
 count += 1
end
#print linkTable






__END__

# From here on - process a single product page

# html = ScraperWiki::scrape("http://www.express.com/mesh-sleeve-sweater-dress-49937-953/control/page/2/show/3/index.pro")           
agent = Mechanize.new

#test 1: Multiple color
#URL = "http://www.express.com/the-original-long-sleeve-essential-shirt-49883-1051/control/show/3/index.pro#jsLink"
url = 'http://www.express.com/fitted-long-sleeve-essential-shirt-45651-721/control/page/14/show/3/index.pro?relatedItem=true&showBreadcrumb=true#jsLink'


#test 2: single color
#URL = 'http://www.express.com/striped-rolled-sleeve-cover-up-sweater-50122-215/control/page/6/show/3/index.pro' 


#Clean URL of parameters
puts url
url[/\?/]? url[/\?.*/] = '' : true
url[/#/]? url[/#.*/] = '' : true
puts url;

page = agent.get(url)

itemTitle = Nokogiri::HTML(page.body).css('#cat-pro-con-detail h1')
puts "Item title: " + itemTitle.text

itemPrice = Nokogiri::HTML(page.body).css('li.cat-pro-price')
puts "Item price: " + itemPrice.text

itemDesc = Nokogiri::HTML(page.body).css('li.cat-pro-desc')
puts "Item description: " + itemDesc.text

#A: This section breaks out individual list items
#itemIndiv = Nokogiri::HTML(page.body).css('li.cat-pro-desc ul li')
#puts "Item bullets: " 
#itemIndiv.each do |item|
#  puts item.text
#end
#A:

colorsO = Nokogiri::HTML(page.body).css('img.cat-pro-swatch')
itemColors = "" 
colorsO.each do |item|
  itemColors.length > 0 ? itemColors = itemColors + ", " + item["alt"] : itemColors = itemColors + item["alt"]
end
puts itemColors

ScraperWiki::save_sqlite(unique_keys=["url"], data={"url"=>URL, "title"=>itemTitle.text,
     "price"=>itemPrice.text, "description"=>itemDesc.text, "colors"=>itemColors} )