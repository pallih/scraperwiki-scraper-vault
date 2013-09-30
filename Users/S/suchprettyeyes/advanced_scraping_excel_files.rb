# spreadsheet is a library for examining and extracting data from Excel spreadsheets
# Documentation is available here:
# http://spreadsheet.rubyforge.org/Spreadsheet.html

require 'open-uri'
require 'spreadsheet'

# Nice example of a spreadsheet with useful data!
url = 'https://spreadsheets.google.com/ccc?key=0AqwaVIkgSiFYdGxjSGZOUlZFcGJ4cVFoZGZJTXl1ZlE&hl=en#gid=4'

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
first_sheet.each do |row|                     # for each row
  if row.first_unused > 0                     # which is actually in use - workaround for possible bug
    (row.first_used...row.first_unused).each do |column|       # for each column within the row
       cell = first_sheet.cell(row.idx,column)
       # Test each cell to see if it's a year range and print each value
       if cell =~ /^$/
         puts "Year: #{cell}"
       end
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
url = 'https://spreadsheets.google.com/ccc?key=0AqwaVIkgSiFYdGxjSGZOUlZFcGJ4cVFoZGZJTXl1ZlE&hl=en#gid=4'

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
first_sheet.each do |row|                     # for each row
  if row.first_unused > 0                     # which is actually in use - workaround for possible bug
    (row.first_used...row.first_unused).each do |column|       # for each column within the row
       cell = first_sheet.cell(row.idx,column)
       # Test each cell to see if it's a year range and print each value
       if cell =~ /^$/
         puts "Year: #{cell}"
       end
       # Here we could then extract the income tax rates by year.
    end
  end
end
