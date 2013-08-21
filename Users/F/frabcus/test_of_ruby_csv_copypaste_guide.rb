data = ScraperWiki.scrape("http://s3-eu-west-1.amazonaws.com/ukhmgdata-cabinetoffice/Spend-data-2010-11-01/Spend-Transactions-with-descriptions-HMT-09-Sep-2010.csv")

require 'fastercsv'
fcsv = FCSV.new(data, :headers => true)


for row in fcsv
  row['Amount'] = row['Amount'].to_f
  if row['Transaction Number']
    ScraperWiki.save_sqlite(unique_keys=['Transaction Number', 'Expense Type', 'Expense Area'], row.to_hash)
  end
end



