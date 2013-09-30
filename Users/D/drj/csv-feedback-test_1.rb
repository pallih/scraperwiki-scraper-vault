data = ScraperWiki.scrape("http://s3-eu-west-1.amazonaws.com/ukhmgdata-cabinetoffice/Spend-data-2010-11-01/Spend-Transactions-with-descriptions-HMT-09-Sep-2010.csv")           

require 'csv'           
csv = CSV.new(data)

csv.each do |row|           
  puts format("%s spent on %s", row[7], row[3])
end

data = ScraperWiki.scrape("http://s3-eu-west-1.amazonaws.com/ukhmgdata-cabinetoffice/Spend-data-2010-11-01/Spend-Transactions-with-descriptions-HMT-09-Sep-2010.csv")           

require 'csv'           
csv = CSV.new(data)

csv.each do |row|           
  puts format("%s spent on %s", row[7], row[3])
end

