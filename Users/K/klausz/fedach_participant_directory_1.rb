require 'net/http'
require 'uri'

url = URI.parse('http://www.fededirectory.frb.org/FedACHdir.txt')
req = Net::HTTP::Get.new(url.path)
res = Net::HTTP.start(url.host, url.port) { |http| http.request(req) }

res.body.split("\n").each do |route|
  record = Hash.new
  record['routing_number']          = route[0,9]
  record['office_code']             = route[9,1]
  record['servicing_frb_number']    = route[10,9]
  record['record_type_code']        = route[19,1]
  record['change_date']             = route[20,6]
  record['new_routing_number']      = route[26,9]
  record['customer_name']           = route[35,36]
  record['address']                 = route[71,36]
  record['city']                    = route[107,20]
  record['state_code']              = route[127,2]
  record['zipcode']                 = route[129,5]
  record['zipcode_extension']       = route[134,4]
  record['telephone_area_code']     = route[138,3]
  record['telephone_prefix_number'] = route[141,3]
  record['telephone_suffix_number'] = route[144,4]
  record['institution_status_code'] = route[148,1]
  record['data_view_code']          = route[149,1]
  record['filler']                  = route[150,5]
  #puts record
  begin
     ScraperWiki.save_sqlite(unique_keys=['routing_number'], record)
  rescue Exception => e
     puts "Exception (#{e.inspect}) raised saving record #{record.inspect}"
  end 
end
require 'net/http'
require 'uri'

url = URI.parse('http://www.fededirectory.frb.org/FedACHdir.txt')
req = Net::HTTP::Get.new(url.path)
res = Net::HTTP.start(url.host, url.port) { |http| http.request(req) }

res.body.split("\n").each do |route|
  record = Hash.new
  record['routing_number']          = route[0,9]
  record['office_code']             = route[9,1]
  record['servicing_frb_number']    = route[10,9]
  record['record_type_code']        = route[19,1]
  record['change_date']             = route[20,6]
  record['new_routing_number']      = route[26,9]
  record['customer_name']           = route[35,36]
  record['address']                 = route[71,36]
  record['city']                    = route[107,20]
  record['state_code']              = route[127,2]
  record['zipcode']                 = route[129,5]
  record['zipcode_extension']       = route[134,4]
  record['telephone_area_code']     = route[138,3]
  record['telephone_prefix_number'] = route[141,3]
  record['telephone_suffix_number'] = route[144,4]
  record['institution_status_code'] = route[148,1]
  record['data_view_code']          = route[149,1]
  record['filler']                  = route[150,5]
  #puts record
  begin
     ScraperWiki.save_sqlite(unique_keys=['routing_number'], record)
  rescue Exception => e
     puts "Exception (#{e.inspect}) raised saving record #{record.inspect}"
  end 
end
