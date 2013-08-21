# Blank Ruby

require 'open-uri'
require 'nokogiri'

@url_base = "http://www.fairfaxcounty.gov/CREGISTER/ContractDetails.aspx?contractNumber="

@first_contract_number = "4400000001"
@last_contract_number = "4400003554"

(@first_contract_number..@last_contract_number).each do |contract|
  html = open(url).read
end