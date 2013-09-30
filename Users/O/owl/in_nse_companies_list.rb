require 'csv'
require 'mechanize'
# encoding: UTF-8

#puts %x[cd /tmp;wget http://nseindia.com/content/equities/EQUITY_L.csv >/dev/null]
Mechanize.new.get("http://nseindia.com/content/equities/EQUITY_L.csv").save_as("EQUITY_L.csv")
records = []
CSV.foreach("EQUITY_L.csv", :quote_char => '"', :col_sep =>',', :row_sep =>:auto, :headers => true) do |row|
  r = { 'SYMBOL'=>row[0],'COMPANY_NAME'=>row[1],'SERIES'=>row[2],'LISTING_DT'=>row[3],'PAID_UP_VALUE'=>row[4],'MARKET_LOT'=>row[5],'ISIN'=>row[6],'FACE_VALUE'=>row[7],"URL"=>"http://nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=#{row[0]}" }
  records << r unless r['ISIN'].nil? 
end
ScraperWiki.save_sqlite(unique_keys=['ISIN'],records,table_name='SWDATA',verbose=2) unless records.length==0
require 'csv'
require 'mechanize'
# encoding: UTF-8

#puts %x[cd /tmp;wget http://nseindia.com/content/equities/EQUITY_L.csv >/dev/null]
Mechanize.new.get("http://nseindia.com/content/equities/EQUITY_L.csv").save_as("EQUITY_L.csv")
records = []
CSV.foreach("EQUITY_L.csv", :quote_char => '"', :col_sep =>',', :row_sep =>:auto, :headers => true) do |row|
  r = { 'SYMBOL'=>row[0],'COMPANY_NAME'=>row[1],'SERIES'=>row[2],'LISTING_DT'=>row[3],'PAID_UP_VALUE'=>row[4],'MARKET_LOT'=>row[5],'ISIN'=>row[6],'FACE_VALUE'=>row[7],"URL"=>"http://nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=#{row[0]}" }
  records << r unless r['ISIN'].nil? 
end
ScraperWiki.save_sqlite(unique_keys=['ISIN'],records,table_name='SWDATA',verbose=2) unless records.length==0
require 'csv'
require 'mechanize'
# encoding: UTF-8

#puts %x[cd /tmp;wget http://nseindia.com/content/equities/EQUITY_L.csv >/dev/null]
Mechanize.new.get("http://nseindia.com/content/equities/EQUITY_L.csv").save_as("EQUITY_L.csv")
records = []
CSV.foreach("EQUITY_L.csv", :quote_char => '"', :col_sep =>',', :row_sep =>:auto, :headers => true) do |row|
  r = { 'SYMBOL'=>row[0],'COMPANY_NAME'=>row[1],'SERIES'=>row[2],'LISTING_DT'=>row[3],'PAID_UP_VALUE'=>row[4],'MARKET_LOT'=>row[5],'ISIN'=>row[6],'FACE_VALUE'=>row[7],"URL"=>"http://nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=#{row[0]}" }
  records << r unless r['ISIN'].nil? 
end
ScraperWiki.save_sqlite(unique_keys=['ISIN'],records,table_name='SWDATA',verbose=2) unless records.length==0
require 'csv'
require 'mechanize'
# encoding: UTF-8

#puts %x[cd /tmp;wget http://nseindia.com/content/equities/EQUITY_L.csv >/dev/null]
Mechanize.new.get("http://nseindia.com/content/equities/EQUITY_L.csv").save_as("EQUITY_L.csv")
records = []
CSV.foreach("EQUITY_L.csv", :quote_char => '"', :col_sep =>',', :row_sep =>:auto, :headers => true) do |row|
  r = { 'SYMBOL'=>row[0],'COMPANY_NAME'=>row[1],'SERIES'=>row[2],'LISTING_DT'=>row[3],'PAID_UP_VALUE'=>row[4],'MARKET_LOT'=>row[5],'ISIN'=>row[6],'FACE_VALUE'=>row[7],"URL"=>"http://nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=#{row[0]}" }
  records << r unless r['ISIN'].nil? 
end
ScraperWiki.save_sqlite(unique_keys=['ISIN'],records,table_name='SWDATA',verbose=2) unless records.length==0
