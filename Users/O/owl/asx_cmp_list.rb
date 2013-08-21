require 'csv'
require 'mechanize'

Mechanize.new().get("http://www.asx.com.au/asx/research/ASXListedCompanies.csv").save_as('tmp.csv')
csv_data = CSV.read 'tmp.csv'
headers = csv_data[2..-1].shift.map {|i| i.gsub(' ','_').strip.downcase unless i.nil? }
puts csv_data.inspect
puts headers.inspect
string_data = csv_data[3..-1].map {|row| row.map {|cell| cell.to_s } }
list = string_data.map {|row| Hash[*headers.zip(row).flatten]}
list.collect{|a| a.delete_if{|k,v| v.nil? or v.empty?}}
puts list.first.inspect
ScraperWiki.save_sqlite(unique_keys=['asx_code'],list)