require 'nokogiri'
require 'open-uri'

BASE_URL = "http://www.hybel.no/bolig-til-leie/annonser/"
EXTENSION_URL = "oslo?side="

class Item

  attr_accessor :id
  attr_accessor :link
  attr_accessor :title
  attr_accessor :price
  attr_accessor :address
  attr_accessor :house
  attr_accessor :createdAt
  attr_accessor :mapUrl
  attr_accessor :imageUrl

end

# Used to save data
def saveData(data)
  data.each do |item|
    record = {
      Id: item.id,
      Link: item.link,
      Title: item.title,
      Price: item.price,
      Address: item.address,
      House: item.house,
      CreatedAt: item.createdAt,
      MapUrl: item.mapUrl,
      ImageUrl: item.imageUrl
    }
    ScraperWiki.save_sqlite([:Id], record)
  end
end


def scrape_page(page)
  
  # Used to store all items before save
  items = Array.new

  # Get the items
  page.search('li').each do |item|

    newItem = Item.new
  
    p "ID: #{item["id"]}"
    newItem.id = item["id"]

    if newItem.id != nil

      newItem.link = item.search('a')[0]["href"]
      p "LINK: #{newItem.link}"

      newItem.title = item.search('h3').text
      p "TITLE: #{newItem.title}"

      newItem.price = item.search('div[class="price"]').text
      p "PRICE: #{newItem.price}"

      newItem.address = item.search('div[class="address"]').text
      p "ADDRESS: #{newItem.address}"

      newItem.house = item.search('div[class="house"]').text
      p "HOUSE: #{newItem.house}"

      newItem.createdAt = item.search('div[class="created"]').text
      p "CREATED_AT: #{newItem.createdAt}"

      newItem.mapUrl = item.search('div[class="map-link"] a')[0]["href"]
      p "MAP_URL: #{newItem.mapUrl}"

      newItem.imageUrl = item.search('div[class="image"] img')[0]["src"]
      p "IMAGE_URL: #{newItem.imageUrl}"

      items << newItem

    end

  end

  saveData(items)

end

def scrape_and_look_for_next_link(url)
  page = Nokogiri::HTML(open(url))
  scrape_page(page)

  next_link = BASE_URL + EXTENSION_URL + "1"
  if next_link 
    p next_link
    next_url = BASE_URL + next_link['href']
    p next_url
    scrape_and_look_for_next_link(next_url)
  end
end

# Start scraper
starting_url = BASE_URL + EXTENSION_URL + "1"
scrape_and_look_for_next_link(starting_url)require 'nokogiri'
require 'open-uri'

BASE_URL = "http://www.hybel.no/bolig-til-leie/annonser/"
EXTENSION_URL = "oslo?side="

class Item

  attr_accessor :id
  attr_accessor :link
  attr_accessor :title
  attr_accessor :price
  attr_accessor :address
  attr_accessor :house
  attr_accessor :createdAt
  attr_accessor :mapUrl
  attr_accessor :imageUrl

end

# Used to save data
def saveData(data)
  data.each do |item|
    record = {
      Id: item.id,
      Link: item.link,
      Title: item.title,
      Price: item.price,
      Address: item.address,
      House: item.house,
      CreatedAt: item.createdAt,
      MapUrl: item.mapUrl,
      ImageUrl: item.imageUrl
    }
    ScraperWiki.save_sqlite([:Id], record)
  end
end


def scrape_page(page)
  
  # Used to store all items before save
  items = Array.new

  # Get the items
  page.search('li').each do |item|

    newItem = Item.new
  
    p "ID: #{item["id"]}"
    newItem.id = item["id"]

    if newItem.id != nil

      newItem.link = item.search('a')[0]["href"]
      p "LINK: #{newItem.link}"

      newItem.title = item.search('h3').text
      p "TITLE: #{newItem.title}"

      newItem.price = item.search('div[class="price"]').text
      p "PRICE: #{newItem.price}"

      newItem.address = item.search('div[class="address"]').text
      p "ADDRESS: #{newItem.address}"

      newItem.house = item.search('div[class="house"]').text
      p "HOUSE: #{newItem.house}"

      newItem.createdAt = item.search('div[class="created"]').text
      p "CREATED_AT: #{newItem.createdAt}"

      newItem.mapUrl = item.search('div[class="map-link"] a')[0]["href"]
      p "MAP_URL: #{newItem.mapUrl}"

      newItem.imageUrl = item.search('div[class="image"] img')[0]["src"]
      p "IMAGE_URL: #{newItem.imageUrl}"

      items << newItem

    end

  end

  saveData(items)

end

def scrape_and_look_for_next_link(url)
  page = Nokogiri::HTML(open(url))
  scrape_page(page)

  next_link = BASE_URL + EXTENSION_URL + "1"
  if next_link 
    p next_link
    next_url = BASE_URL + next_link['href']
    p next_url
    scrape_and_look_for_next_link(next_url)
  end
end

# Start scraper
starting_url = BASE_URL + EXTENSION_URL + "1"
scrape_and_look_for_next_link(starting_url)