#############################################################################
# Comma Separated Value (CSV) files are a common way to back up
# large amounts of consistent data.
# Usually there is one record on each line, fields separated by commas.
#############################################################################
require 'open-uri'
require 'fastercsv'

# Here is an example CSV file
url = "https://scraperwiki.com/scrapers/export/tutorial-csv/"

open url do |f|
  while line = f.gets do
    puts line
  end
end

#----------------------------------------------------------------------
# Reading the data is more complicated than just splitting it up by commas
# [e.g. line.split(",") in Ruby, because the fields themselves can
# contain commas, e.g. "Smith, John"
# Fortunately the csv.reader() function solves this problem.
# The headers option treats the first row as header text
# and allows fields to  be referred to
# UNCOMMENT THE NEXT FOUR LINES OF CODE.
#----------------------------------------------------------------------
#open url do |f|
#  csv = FCSV.new(f, :headers => true)       # the headers option treats the first row as header text
#  csv.each { |row| puts "#{row['Name']}, #{row['Phone_number']}" }
#end
#############################################################################
# Comma Separated Value (CSV) files are a common way to back up
# large amounts of consistent data.
# Usually there is one record on each line, fields separated by commas.
#############################################################################
require 'open-uri'
require 'fastercsv'

# Here is an example CSV file
url = "https://scraperwiki.com/scrapers/export/tutorial-csv/"

open url do |f|
  while line = f.gets do
    puts line
  end
end

#----------------------------------------------------------------------
# Reading the data is more complicated than just splitting it up by commas
# [e.g. line.split(",") in Ruby, because the fields themselves can
# contain commas, e.g. "Smith, John"
# Fortunately the csv.reader() function solves this problem.
# The headers option treats the first row as header text
# and allows fields to  be referred to
# UNCOMMENT THE NEXT FOUR LINES OF CODE.
#----------------------------------------------------------------------
#open url do |f|
#  csv = FCSV.new(f, :headers => true)       # the headers option treats the first row as header text
#  csv.each { |row| puts "#{row['Name']}, #{row['Phone_number']}" }
#end
