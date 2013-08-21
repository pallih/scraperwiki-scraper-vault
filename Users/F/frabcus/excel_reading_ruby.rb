require 'spreadsheet'
require 'open-uri'
url = "http://www.whatdotheyknow.com/request/82804/response/208592/attach/2/ACCIDENTS%20TRAMS%20Laurderdale.xls"
book = nil
open url do |f|
  book = Spreadsheet.open f
end

sheet = book.worksheet 0
sheet = book.worksheet 'LAUDERDALE AVE'

book.worksheets.each do |sheet|
  puts "Sheet called #{sheet.name} has #{sheet.row_count} rows and #{sheet.column_count} columns"
end

row = sheet.row(4)
require 'pp'
pp row[0]

keys = sheet.row(2)
keys[1] = keys[1].gsub('.', '')


sheet.each_with_index do |row, rownumber|
  # create dictionary of the row values
  data = {}
  row.each_index do |i|
    data[keys[i]] = row[i]
  end
  data['rownumber'] = rownumber

  # remove the empty column (which has a blank heading)
  data.delete(nil)

  # only save if it is a full row (rather than a blank line or a note)
  if data['DATE'] != 'DATE' and data['DATE'] != nil and data['FLEET NO'] != nil
    ScraperWiki.save_sqlite(unique_keys=['rownumber'], data)
  end
end

{
