require 'rubygems'
require 'open-uri'
require 'csv'

csv = open("http://local.direct.gov.uk/Data/local_authority_contact_details.csv")

CSV.parse(csv) do |row|
  details = {}

  unless row[0] == "Name"

    details[:name] = row[0]
    details[:url] = row[1]
    details[:contacturl] = row[2]
    details[:snac] = row[3]
    details[:address1] = row[4]
    details[:address2] = row[5]
    details[:town] = row[6]
    details[:city] = row[7]
    details[:county] = row[8]
    details[:postcode] = row[9]
    details[:tel1desc] = row[10]
    details[:tel1] = row[11]
    details[:tel2desc] = row[12]
    details[:tel2] = row[13]
    details[:tel3desc] = row[14]
    details[:tel3] = row[15]
    details[:fax] = row[16]
    details[:email] = row[17]
    details[:hours] = row[18]
  
    ScraperWiki.save([:snac], details)
  
  end
end
require 'rubygems'
require 'open-uri'
require 'csv'

csv = open("http://local.direct.gov.uk/Data/local_authority_contact_details.csv")

CSV.parse(csv) do |row|
  details = {}

  unless row[0] == "Name"

    details[:name] = row[0]
    details[:url] = row[1]
    details[:contacturl] = row[2]
    details[:snac] = row[3]
    details[:address1] = row[4]
    details[:address2] = row[5]
    details[:town] = row[6]
    details[:city] = row[7]
    details[:county] = row[8]
    details[:postcode] = row[9]
    details[:tel1desc] = row[10]
    details[:tel1] = row[11]
    details[:tel2desc] = row[12]
    details[:tel2] = row[13]
    details[:tel3desc] = row[14]
    details[:tel3] = row[15]
    details[:fax] = row[16]
    details[:email] = row[17]
    details[:hours] = row[18]
  
    ScraperWiki.save([:snac], details)
  
  end
end
