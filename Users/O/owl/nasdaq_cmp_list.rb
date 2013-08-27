require 'csv'
require 'mechanize'

Mechanize.new().get("http://www.nasdaq.com/screening/companies-by-name.aspx?letter=%25&pagesize=20000&render=download").save_as('tmp.csv')
csv_data = CSV.read 'tmp.csv'
headers = csv_data.shift.map {|i| i.gsub(' ','_').strip unless i.nil? }
string_data = csv_data.map {|row| row.map {|cell| cell.to_s } }
list = string_data.map {|row| Hash[*headers.zip(row).flatten]}
list.collect{|a| a.delete_if{|k,v| v.empty?}}
ScraperWiki.save_sqlite(unique_keys=['Symbol'],list)require 'csv'
require 'mechanize'

Mechanize.new().get("http://www.nasdaq.com/screening/companies-by-name.aspx?letter=%25&pagesize=20000&render=download").save_as('tmp.csv')
csv_data = CSV.read 'tmp.csv'
headers = csv_data.shift.map {|i| i.gsub(' ','_').strip unless i.nil? }
string_data = csv_data.map {|row| row.map {|cell| cell.to_s } }
list = string_data.map {|row| Hash[*headers.zip(row).flatten]}
list.collect{|a| a.delete_if{|k,v| v.empty?}}
ScraperWiki.save_sqlite(unique_keys=['Symbol'],list)require 'csv'
require 'mechanize'

Mechanize.new().get("http://www.nasdaq.com/screening/companies-by-name.aspx?letter=%25&pagesize=20000&render=download").save_as('tmp.csv')
csv_data = CSV.read 'tmp.csv'
headers = csv_data.shift.map {|i| i.gsub(' ','_').strip unless i.nil? }
string_data = csv_data.map {|row| row.map {|cell| cell.to_s } }
list = string_data.map {|row| Hash[*headers.zip(row).flatten]}
list.collect{|a| a.delete_if{|k,v| v.empty?}}
ScraperWiki.save_sqlite(unique_keys=['Symbol'],list)