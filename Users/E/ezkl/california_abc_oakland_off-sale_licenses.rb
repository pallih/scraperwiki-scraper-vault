# encoding: UTF-8
require 'nokogiri'
require 'net/http'
require 'open-uri'

@base_uri   = URI.parse("http://www.abc.ca.gov/datport/AHCityRep.asp")

ROW_PATTERN = "//table[@border='1']//tr[@class='report_column'][position() > 1]"
COL_PATTERN = "td[position() > 1]"

def request(city = "OAKLAND", license = "p_OffSale")
  @city     = city
  @license  = license 
  @response = Net::HTTP.post_form(@base_uri, request_options)
  parse
end

def parse
  doc = Nokogiri::HTML(@response.body)
  
  headers = [ "licensee_number", "status", "license_type", "og_issue_date", "expiry_date", "owner_and_address", "business", "mailing_address", "geocode" ]
  
  doc.xpath(ROW_PATTERN).each do |row|
    row_data = row.xpath(COL_PATTERN).collect do |data|
      (data.text).size ? (data.text).strip : ""
    end
    row = Hash[*headers.zip(row_data).flatten]
    ScraperWiki.save_sqlite(headers, row)
  end
end

private 
#################
def request_options
  { :q_CityLOV => @city, :q_LTLOV => "01", :RPTYPE => @license, :SUBMIT1 => "Continue" }
end


request