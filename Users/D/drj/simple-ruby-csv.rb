# A simple example of CSV parsing, using Ruby.
require 'csv'

data = ScraperWiki.scrape("http://s3-eu-west-1.amazonaws.com/ukhmgdata-cabinetoffice/Spend-data-2010-11-01/Spend-Transactions-with-descriptions-HMT-09-Sep-2010.csv")           

csv = CSV.new(data)

csv.each do |row|
  doc.css('div.featured a').each do |link|           
    puts link.class
end
end

