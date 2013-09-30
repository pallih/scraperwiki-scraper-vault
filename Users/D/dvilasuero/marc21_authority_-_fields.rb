require 'nokogiri'
require 'uri'
require 'cgi'
require 'open-uri'

class MARCField
    def initialize(tag, label, uri)
        @tag = tag
        @label = label
        @uri = uri
       
        
    end
    
    attr_reader :tag, :label, :uri, :desc
    attr_accessor :subfields

    def getSubfields
      
    end
end

base_url = "http://www.loc.gov/marc/authority/"
index_page = "adsummary.html"
index_doc = Nokogiri::HTML(open(base_url + index_page))
mts = []

index_doc.xpath('//div[@class="summarytable"]/table/tr').each do |rows|
  if rows.at_xpath('td[1]').inner_text =~ /\d\d\d/
    marctag = rows.at_xpath('td[1]').inner_text
    marctag_url = base_url + rows.at_xpath('td[2]/a[1]/@href').to_s
    marctag_label = rows.at_xpath("td[2]/text()").inner_text
    mt = MARCField.new(marctag,marctag_label,marctag_url)
    mts.push(mt)
  end
  #marctag_label = rows.xpath('//td[1]').inner_text
  #marctag_urls.push(base_url + marctag_url)
end

mts.each do |mt|
  html = ScraperWiki.scrape(mt.uri)
  doc = Nokogiri::HTML(html)
  marctag_description = ""
  doc.xpath('//body/p').each do |paragh|
    marctag_description += paragh
  end
  ScraperWiki.save(unique_keys=["tag"],data={'tag' => mt.tag,'label' => mt.label, 'description' => marctag_description, 'uri' => mt.uri})
endrequire 'nokogiri'
require 'uri'
require 'cgi'
require 'open-uri'

class MARCField
    def initialize(tag, label, uri)
        @tag = tag
        @label = label
        @uri = uri
       
        
    end
    
    attr_reader :tag, :label, :uri, :desc
    attr_accessor :subfields

    def getSubfields
      
    end
end

base_url = "http://www.loc.gov/marc/authority/"
index_page = "adsummary.html"
index_doc = Nokogiri::HTML(open(base_url + index_page))
mts = []

index_doc.xpath('//div[@class="summarytable"]/table/tr').each do |rows|
  if rows.at_xpath('td[1]').inner_text =~ /\d\d\d/
    marctag = rows.at_xpath('td[1]').inner_text
    marctag_url = base_url + rows.at_xpath('td[2]/a[1]/@href').to_s
    marctag_label = rows.at_xpath("td[2]/text()").inner_text
    mt = MARCField.new(marctag,marctag_label,marctag_url)
    mts.push(mt)
  end
  #marctag_label = rows.xpath('//td[1]').inner_text
  #marctag_urls.push(base_url + marctag_url)
end

mts.each do |mt|
  html = ScraperWiki.scrape(mt.uri)
  doc = Nokogiri::HTML(html)
  marctag_description = ""
  doc.xpath('//body/p').each do |paragh|
    marctag_description += paragh
  end
  ScraperWiki.save(unique_keys=["tag"],data={'tag' => mt.tag,'label' => mt.label, 'description' => marctag_description, 'uri' => mt.uri})
end