###############################################################################
# Scrapes USDA commodity categories for fruit and vegetables
###############################################################################
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.marketnews.usda.gov'

# url to navigate categories
CATEGORY_URL = BASE_URL + '/portal/fv?paf_dm=full&paf_gear_id=1200002&startIndex=1&dr=1&navType=comm&navClass='

categories = Array.[]('FRUITS', 'VEGETABLES', 'ONPO', 'HERBS', 'NUTS', 'ORNAMENTALS')

# url to the XML version of the data rendered in the on-page HTML table
# need to replace &class, &commName and possibly &commAbr
# all three are found in the CATEGORY_URL
XML_URL = BASE_URL + '/gear/usda/report_output_xml.jsp?/portal/fv?&paf_gear_id=1200002&rowDisplayMax=25&repType=termPriceDaily&dr=1&dr=1&class=FRUITS&paf_dm=full&locName=&commName=APPLE+CIDER&startIndex=1&commAbr=APLCID&lastCommodity=&previousVal=&lastLocation=&xml=true'

# create a unique key for each entry
class KeyGenerator
  require "digest/sha1"
  attr_accessor :key
  def self.generate(length = 10)
    key = Digest::SHA1.hexdigest(Time.now.to_s + rand(12341234).to_s)[1..length]
  end
end

# parse the XML source into a new row
class USDACommodityParser < Nokogiri::XML::SAX::Document

  def initialize(commodity, category, source)
    @commodity, @category, @source = commodity, category, source
    @in_date, @in_cityName, @in_originName, @in_lowPriceMin, @in_highPriceMax, @in_itemSize = false
    @h = Hash.new("row")
    @key = 0
  end

  # keep these fields. (there are other fields.)
  def start_element element, attrs = []
    if element == "item"
      @key = Digest::SHA1.hexdigest(Time.now.to_s + rand(12341234).to_s)
      #puts key
      @h["key"] = @key
      @h["commodity"] = @commodity
      @h["category"] = @category
      @h["source"] = @source
    elsif element== "originName"
      @in_originName = true
    elsif element == "lowPriceMin"
      @in_lowPriceMin = true
    elsif element == "highPriceMax"
      @in_highPriceMax = true
    elsif element == "date"
      @in_date = true
    elsif element == "itemSize"
      @in_itemSize = true
    elsif element == "cityName"
      @in_cityName = true
    end
  end

  def end_element element
    @in_date, @in_cityName, @in_originName, @in_lowPriceMin, @in_highPriceMax, @in_itemSize = false
    if element == "item"
     ScraperWiki.save(unique_keys=['key'], data=@h)
     @h.clear
    end
  end

  def characters text
    @h["date"] = text.strip if @in_date
    @h["lowPriceMin"] = text.strip if @in_lowPriceMin
    @h["highPriceMax"] = text.strip if @in_highPriceMax
    
  end

  def cdata_block text
    @h["cityName"] = text.strip if @in_cityName
    @h["itemSize"] = text.strip if @in_itemSize
    @h["originName"] = text.strip if @in_originName
  end

end



def scrape_commodity(category, commodity, url)
  # construct the URL to the commodity XML
  cls = url.match(/&class=[A-Z]+/)
  abbr = url.match(/&commAbr=[A-Z]+/)
  name = url.match(/&commName=(.)+/)

  name = name.to_s

  # replace spaces with plusses (+)
  if name.match(/[ ]/)
    name = name.to_s.gsub!(/[ ]/, '+')
  end

  s = String.new(XML_URL)
  s.gsub!(/&class=[A-Z]+/, cls.to_s)
  s.gsub!(/&commAbr=[A-Z]+/, abbr.to_s)
  s.gsub!(/&commName=(.)+&startIndex/, name + '&startIndex')

  # open XML doc

  doc = USDACommodityParser.new(commodity, category, s)  
  parser = Nokogiri::XML::SAX::Parser.new(doc)
  parser.parse(open(s))

end

# scrape function: gets passed an individual page to scrape
def scrape_category(category)
  url = CATEGORY_URL + category
  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)

  # grab all of the a tags
  doc.search('a').each do |object|
    # get the a tag text, check for nil, empty and skip over the alphabetical anchors, A-B, C-D, etc
    commodity= object.text
   if commodity and not commodity.empty? and not commodity =~ /[A-Z]-[A-Z]/
       url = BASE_URL + object['href']
      scrape_commodity(category, commodity, url)
    end
  end
end


# ---------------------------------------------------------------------------
# "main"
# ---------------------------------------------------------------------------
categories.each { |category| scrape_category(category) }
###############################################################################
# Scrapes USDA commodity categories for fruit and vegetables
###############################################################################
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.marketnews.usda.gov'

# url to navigate categories
CATEGORY_URL = BASE_URL + '/portal/fv?paf_dm=full&paf_gear_id=1200002&startIndex=1&dr=1&navType=comm&navClass='

categories = Array.[]('FRUITS', 'VEGETABLES', 'ONPO', 'HERBS', 'NUTS', 'ORNAMENTALS')

# url to the XML version of the data rendered in the on-page HTML table
# need to replace &class, &commName and possibly &commAbr
# all three are found in the CATEGORY_URL
XML_URL = BASE_URL + '/gear/usda/report_output_xml.jsp?/portal/fv?&paf_gear_id=1200002&rowDisplayMax=25&repType=termPriceDaily&dr=1&dr=1&class=FRUITS&paf_dm=full&locName=&commName=APPLE+CIDER&startIndex=1&commAbr=APLCID&lastCommodity=&previousVal=&lastLocation=&xml=true'

# create a unique key for each entry
class KeyGenerator
  require "digest/sha1"
  attr_accessor :key
  def self.generate(length = 10)
    key = Digest::SHA1.hexdigest(Time.now.to_s + rand(12341234).to_s)[1..length]
  end
end

# parse the XML source into a new row
class USDACommodityParser < Nokogiri::XML::SAX::Document

  def initialize(commodity, category, source)
    @commodity, @category, @source = commodity, category, source
    @in_date, @in_cityName, @in_originName, @in_lowPriceMin, @in_highPriceMax, @in_itemSize = false
    @h = Hash.new("row")
    @key = 0
  end

  # keep these fields. (there are other fields.)
  def start_element element, attrs = []
    if element == "item"
      @key = Digest::SHA1.hexdigest(Time.now.to_s + rand(12341234).to_s)
      #puts key
      @h["key"] = @key
      @h["commodity"] = @commodity
      @h["category"] = @category
      @h["source"] = @source
    elsif element== "originName"
      @in_originName = true
    elsif element == "lowPriceMin"
      @in_lowPriceMin = true
    elsif element == "highPriceMax"
      @in_highPriceMax = true
    elsif element == "date"
      @in_date = true
    elsif element == "itemSize"
      @in_itemSize = true
    elsif element == "cityName"
      @in_cityName = true
    end
  end

  def end_element element
    @in_date, @in_cityName, @in_originName, @in_lowPriceMin, @in_highPriceMax, @in_itemSize = false
    if element == "item"
     ScraperWiki.save(unique_keys=['key'], data=@h)
     @h.clear
    end
  end

  def characters text
    @h["date"] = text.strip if @in_date
    @h["lowPriceMin"] = text.strip if @in_lowPriceMin
    @h["highPriceMax"] = text.strip if @in_highPriceMax
    
  end

  def cdata_block text
    @h["cityName"] = text.strip if @in_cityName
    @h["itemSize"] = text.strip if @in_itemSize
    @h["originName"] = text.strip if @in_originName
  end

end



def scrape_commodity(category, commodity, url)
  # construct the URL to the commodity XML
  cls = url.match(/&class=[A-Z]+/)
  abbr = url.match(/&commAbr=[A-Z]+/)
  name = url.match(/&commName=(.)+/)

  name = name.to_s

  # replace spaces with plusses (+)
  if name.match(/[ ]/)
    name = name.to_s.gsub!(/[ ]/, '+')
  end

  s = String.new(XML_URL)
  s.gsub!(/&class=[A-Z]+/, cls.to_s)
  s.gsub!(/&commAbr=[A-Z]+/, abbr.to_s)
  s.gsub!(/&commName=(.)+&startIndex/, name + '&startIndex')

  # open XML doc

  doc = USDACommodityParser.new(commodity, category, s)  
  parser = Nokogiri::XML::SAX::Parser.new(doc)
  parser.parse(open(s))

end

# scrape function: gets passed an individual page to scrape
def scrape_category(category)
  url = CATEGORY_URL + category
  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)

  # grab all of the a tags
  doc.search('a').each do |object|
    # get the a tag text, check for nil, empty and skip over the alphabetical anchors, A-B, C-D, etc
    commodity= object.text
   if commodity and not commodity.empty? and not commodity =~ /[A-Z]-[A-Z]/
       url = BASE_URL + object['href']
      scrape_commodity(category, commodity, url)
    end
  end
end


# ---------------------------------------------------------------------------
# "main"
# ---------------------------------------------------------------------------
categories.each { |category| scrape_category(category) }
