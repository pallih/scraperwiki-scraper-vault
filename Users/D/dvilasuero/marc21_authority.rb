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
    
    attr_reader :tag, :label, :uri
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
  doc.xpath('//body').each do |table|
    if table.at_xpath('table[2]/tr[2]/td[1]')
      if table.at_xpath('table[2]/tr[3]').inner_text.include? '$'
        sfs = table.at_xpath('table[2]/tr[3]').inner_text.split('$')
        sfs.each do |sf|
          if sf.strip.length >0
            xs = sf.split('(')
            begin
              ScraperWiki.save(unique_keys=["tag", "subfield"],data={'tag' => mt.tag,'label' => mt.label, 'uri' => mt.uri, 'subfield' => xs[0].strip, 'repeatable' => xs[1].strip.chomp(')')})
            rescue
              puts "Error: " + mt.tag.to_s + ":" + xs[0].to_s
            end
          end
        end
      end
    end
  end
end
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
    
    attr_reader :tag, :label, :uri
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
  doc.xpath('//body').each do |table|
    if table.at_xpath('table[2]/tr[2]/td[1]')
      if table.at_xpath('table[2]/tr[3]').inner_text.include? '$'
        sfs = table.at_xpath('table[2]/tr[3]').inner_text.split('$')
        sfs.each do |sf|
          if sf.strip.length >0
            xs = sf.split('(')
            begin
              ScraperWiki.save(unique_keys=["tag", "subfield"],data={'tag' => mt.tag,'label' => mt.label, 'uri' => mt.uri, 'subfield' => xs[0].strip, 'repeatable' => xs[1].strip.chomp(')')})
            rescue
              puts "Error: " + mt.tag.to_s + ":" + xs[0].to_s
            end
          end
        end
      end
    end
  end
end
