# spreadsheet is a library for examining and extracting data from Excel spreadsheets
# Documentation is available here:
# http://spreadsheet.rubyforge.org/Spreadsheet.html
require 'open-uri'
require 'spreadsheet'

# Nice example of a spreadsheet with useful data!
url = 'http://www.hmrc.gov.uk/stats/tax_structure/incometaxrates_1974to1990.xls'

# Open the spreadsheet from an url
book = nil
open url do |f|
  book = Spreadsheet.open f
end

# We can find out information about the workbook - number of sheets
puts "Workbook has #{book.worksheets.length} sheet(s)"

# Loop over each sheet, print name, and number of rows (which appears to have a bug) /columns
book.worksheets.each do |sheet|
  puts "Sheet called #{sheet.name} has #{sheet.row_count} rows and #{sheet.column_count} columns"
end

# You can also access each worksheet by its index
first_sheet = book.worksheet 0

# You can loop over all the cells in the worksheet
first_sheet.each do |row|
  if row.first_unused > 0 # which is actually in use - workaround for possible bug
    (row.first_used...row.first_unused).each do |column| # for each column within the row
       cell = first_sheet.cell(row.idx,column)

       # Test each cell to see if it's a year range and print each value
       puts "Year: #{cell}" if cell =~ /^\d{4}-\d{2,4}$/

       # Here we could then extract the income tax rates by year.
    end
  end
end
# spreadsheet is a library for examining and extracting data from Excel spreadsheets
# Documentation is available here:
# http://spreadsheet.rubyforge.org/Spreadsheet.html
require 'open-uri'
require 'spreadsheet'

# Nice example of a spreadsheet with useful data!
url = 'http://www.hmrc.gov.uk/stats/tax_structure/incometaxrates_1974to1990.xls'

# Open the spreadsheet from an url
book = nil
open url do |f|
  book = Spreadsheet.open f
end

# We can find out information about the workbook - number of sheets
puts "Workbook has #{book.worksheets.length} sheet(s)"

# Loop over each sheet, print name, and number of rows (which appears to have a bug) /columns
book.worksheets.each do |sheet|
  puts "Sheet called #{sheet.name} has #{sheet.row_count} rows and #{sheet.column_count} columns"
end

# You can also access each worksheet by its index
first_sheet = book.worksheet 0

# You can loop over all the cells in the worksheet
first_sheet.each do |row|
  if row.first_unused > 0 # which is actually in use - workaround for possible bug
    (row.first_used...row.first_unused).each do |column| # for each column within the row
       cell = first_sheet.cell(row.idx,column)

       # Test each cell to see if it's a year range and print each value
       puts "Year: #{cell}" if cell =~ /^\d{4}-\d{2,4}$/

       # Here we could then extract the income tax rates by year.
    end
  end
end
