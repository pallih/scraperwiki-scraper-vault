require 'rubygems'
require 'nokogiri'
require 'pp'
require 'open-uri'
require 'uri'
require 'cgi'


class BrumPoolScraper
  
  attr_reader :pools
  
  def run

    header_mapping = Hash[
        "tbl397id0_0" => "name" ,
        "tbl397id0_1" => "address" ,
        "tbl397id0_2" => "phone"
      ]

    @pools = []
  
    pool_id = 0
  
    doc = Nokogiri::HTML(open("http://www.birmingham.gov.uk/cs/Satellite?c=Page&childpagename=Sport%2FPageLayout&cid=1223349263026&pagename=BCC%2FCommon%2FWrapper%2FWrapper"))

    for row in doc.search("div[@class='main']/table/tbody/tr")
      
      pool = Pool.new(pool_id)
      
      for column in row.search("td")
        attribute = header_mapping[column["headers"]]
        
        case attribute
          when "name"
            link = column.search("a").first
            pool.name = link.inner_text
            puts "scraping #{pool.name}..."
            long_link = link["href"]
            pool.website = long_link
          when "address"
            pool.address = "#{column.inner_text}, Birmingham, UK"
            position = geocode(pool.address)
            pool.lat = position.search("lat").first.inner_text
            pool.long = position.search("lng").first.inner_text
          when "phone"
            pool.phone = "+44 (0)121 #{column.inner_text}"
        end
        
        # scrape_pool_page(pool, long_link)
                  
      end

      pools << pool

      pool_id += 1

    end

    # pp pools
  
  end # run()
  
  def geocode(address)
    encoded_address = address.gsub(' ', '+')
    geocoding_uri = "http://maps.googleapis.com/maps/api/geocode/xml?address=#{encoded_address}&sensor=false"
    response = open(geocoding_uri).read
    response_tree = Nokogiri::XML(response)
    position = response_tree.search("GeocodeResponse/result/geometry/location").first
    return position
  end
  
  def scrape_pool_page(pool, long_link)
    pool_doc = Nokogiri::HTML(open(long_link))
    
    # <p><strong>General Opening Times:</strong> Mon - Fri 9am - 4pm, Weds 9am - 1pm, Sat &amp; Sun Closed</p>
    
    strongs = pool_doc.search("//p/strong")
    for strong in strongs
      text = strong.inner_text
      if (text.match("Opening Times:") || text.match("Opening Hours:"))
        puts "\t<#{strong.inner_text}> <#{strong.parent.inner_text}>"
      end
    end
    
  end
  
end # class BrumPoolScraper

class Pool
  attr_reader :id
  attr_accessor :name, :website, :address, :phone, :lat, :long

  def initialize(id)
    @id = id
  end

  def to_s
    puts "{\n\tid = '#{@id}',\n\tname = '#{@name}',\n\twebsite = '#{@website}',\n\taddress = '#{@address}',\n\lat = '#{@lat}',\n\long = '#{@long}',\n\tphone = '#{@phone}'\n}"
  end
  
end

scraper = BrumPoolScraper.new
scraper.run
scraper.pools.each do |pool|
  data = {
    'id' => pool.id,
    'name' => pool.name,
    'website' => pool.website,
    'address' => pool.address,
    'phone' => pool.phone,
    'lat' => pool.lat,
    'long' => pool.long,
  }
  ScraperWiki.save(unique_keys=['id'], data=data)
end


